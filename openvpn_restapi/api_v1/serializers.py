from openvpn_restapi.api_v1.models import User, Group, Certificate
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'group', 'password', 'online', 'enabled', 'start_date', 'end_date', 'created_at', 'updated_at')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', 'created_at', 'updated_at')


class CertificateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Certificate
        fields = ('url', 'certificate', 'key', 'csr', 'created_at', 'updated_at')
