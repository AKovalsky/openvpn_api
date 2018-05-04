from openvpn_restapi.api_v1.models import User, Group, Certificate
from rest_framework import serializers
from .custom_actions import CreateConfigFile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'group', 'password', 'online', 'enabled', 'start_date', 'end_date', 'created_at', 'updated_at')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name', 'created_at', 'updated_at')


class CertificateSerializer(serializers.HyperlinkedModelSerializer):
    config = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = ('id', 'url', 'user', 'basename', 'certificate', 'key', 'csr', 'revoked', 'serial', 'created_at', 'updated_at', 'config')
        read_only_fields = ('basename', 'certificate', 'key', 'csr', 'serial')

    def get_config(self, obj):
        data = CreateConfigFile(obj.basename, obj.basename, obj.user, obj.certificate, obj.key)
        return data
