class VulcanAPIException(Exception):
    pass


class InvalidTokenException(VulcanAPIException):
    pass


class InvalidPINException(VulcanAPIException):
    pass


class InvalidSymbolException(VulcanAPIException):
    pass


class ExpiredTokenException(VulcanAPIException):
    pass


class UnauthorizedCertificateException(VulcanAPIException):
    pass


class InvalidSignatureValuesException(VulcanAPIException):
    pass
