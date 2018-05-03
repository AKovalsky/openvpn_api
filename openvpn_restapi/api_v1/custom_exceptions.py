from rest_framework.exceptions import APIException

class CreateSSLCertificateException(APIException):
    status_code = 500
    default_detail = 'Unable to create certificate'
    default_code = 'service_unavailable'

