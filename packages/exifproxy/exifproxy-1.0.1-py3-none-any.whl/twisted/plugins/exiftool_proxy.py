from twisted.application.service import ServiceMaker

ExiftoolProxyService = ServiceMaker(
    "Exiftool Proxy Service",
    "exifproxy.service",
    "Metadata extraction reverse proxy based on exiftool",
    "exifproxy")
