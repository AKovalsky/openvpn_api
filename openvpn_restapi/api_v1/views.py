from openvpn_restapi.api_v1.models import User, Group, Certificate
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from .custom_mixins import CreateCertificateModelMixin, RevokeCertificateModelMixin, RetrieveCertificateModelMixin
from openvpn_restapi.api_v1.serializers import UserSerializer, GroupSerializer, CertificateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'email', 'discord_username')


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAdminUser,)


class CertificateViewSet(CreateCertificateModelMixin,
                         RevokeCertificateModelMixin,
                         RetrieveCertificateModelMixin,
    #                     mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet
                        ):
    """
    API endpoint that allows certificates to be viewed or edited.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('basename', 'user')
