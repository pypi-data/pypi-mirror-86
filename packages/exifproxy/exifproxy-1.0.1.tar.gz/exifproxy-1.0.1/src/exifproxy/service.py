from twisted.application import internet, service, strports
from twisted.internet import endpoints, reactor
from twisted.python import usage
from twisted.web import resource, server
from exifproxy.exiftool import \
    ExiftoolJSONMetadataReverseProxyResource, \
    ExiftoolPageimagesReverseProxyResource, \
    ExiftoolPreviewReverseProxyResource, \
    ExiftoolProtocolFactory, \
    ExiftoolXMPMetadataReverseProxyResource
from txexiftool import ExiftoolProtocol
from urllib.parse import urlsplit


class Options(usage.Options):
    optParameters = [
        ["backend", "-b", "http://localhost",
            "Url to backend, no trailing slash"],
        ["listen", "-l", "tcp:8080",
            "Listen port (strports syntax)"],
    ]


def makeService(options):
    parts = urlsplit(options["backend"])
    host = parts.hostname
    path = parts.path.encode("utf-8")

    if parts.scheme == "http":
        port = int(parts.port) if parts.port is not None else 80
        backend_strports = f"tcp:{host}:{port}"
    else:
        port = int(parts.port) if parts.port is not None else 443
        backend_strports = f"ssl:{host}:{port}"

    hostport = (f"{host}:{port}" if parts.port else f"{host}").encode("ascii")

    s = service.MultiService()

    ext = internet.ClientService(
        endpoints.clientFromString(reactor, "exiftool"),
        ExiftoolProtocolFactory.forProtocol(ExiftoolProtocol, 2**22)
    )
    ext.setServiceParent(s)

    backend = endpoints.clientFromString(reactor, backend_strports)
    root = resource.Resource()
    root.putChild(b"json", ExiftoolJSONMetadataReverseProxyResource(
        ext, backend, hostport, path))
    root.putChild(b"xmp", ExiftoolXMPMetadataReverseProxyResource(
        ext, backend, hostport, path))
    root.putChild(b"preview", ExiftoolPreviewReverseProxyResource(
        ext, backend, hostport, path))
    root.putChild(b"pageimage", ExiftoolPageimagesReverseProxyResource(
        ext, backend, hostport, path))
    srv = strports.service(options["listen"], server.Site(root))
    srv.setServiceParent(s)

    return s
