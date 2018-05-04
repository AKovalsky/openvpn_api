from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from .custom_actions import CreateSSLCertificate, RevokeSSLCertificate
from django.utils.crypto import get_random_string

class CreateCertificateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        name = get_random_string(length=16)
        certificate_name, key_name, csr_name, serial_name = CreateSSLCertificate(name)
        serializer.save(basename=name, certificate=certificate_name, key=key_name, csr=csr_name, serial=serial_name)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

class RevokeCertificateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        name = instance.basename
        status = instance.revoked
        print(status)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, name)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, name, status):
        if status != True:
            RevokeSSLCertificate(name)
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RetrieveCertificateModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.test = "test"
 #       instance.config = lambda: None
#        setattr(instance.config, 'test', 'test')
        serializer = self.get_serializer(instance)
#        serializer.data.config = 'test'
        print(serializer.data)
       # serializer.context = {"test": "test"}
        return Response(serializer.data)
