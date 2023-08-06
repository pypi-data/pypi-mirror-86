from twisted.internet import defer, protocol
from twisted.web import resource
from exifproxy.web import ExtractionReverseProxyResource
import os
import tempfile
import uuid


class ExiftoolJSONMetadataExtraction:

    def __init__(self, exiftool):
        self._exiftool = exiftool

    @defer.inlineCallbacks
    def extract(self, filename):
        exf_proto = yield self._exiftool.whenConnected()
        meta = yield exf_proto.execute("-j", "-g", "-a", "-struct", filename)
        return meta, b"application/json"


class ExiftoolXMPMetadataExtraction:

    def __init__(self, exiftool):
        self._exiftool = exiftool

    @defer.inlineCallbacks
    def extract(self, filename):
        exf_proto = yield self._exiftool.whenConnected()

        with tempfile.TemporaryDirectory() as workspace:
            outfile = os.path.join(workspace, f"{uuid.uuid4()}.xmp")
            yield exf_proto.execute(
                    "-o", outfile,
                    filename)

            with open(outfile, "rb") as stream:
                return stream.read(), b"application/rdf+xml"


class ExiftoolPreviewExtraction:

    def __init__(self, exiftool):
        self._exiftool = exiftool

    @defer.inlineCallbacks
    def extract(self, filename):
        exf_proto = yield self._exiftool.whenConnected()

        with tempfile.TemporaryDirectory() as workspace:
            outfile = os.path.join(workspace, str(uuid.uuid4()))
            yield exf_proto.execute(
                    "-preview:all",
                    "-b",
                    "-W", outfile,
                    filename)

            with open(outfile, "rb") as stream:
                return stream.read(), b"image/jpeg"


class ExiftoolPageimageMetadataExtraction:

    def __init__(self, exiftool, page):
        self._exiftool = exiftool
        self._page = page

    @defer.inlineCallbacks
    def extract(self, filename):
        exf_proto = yield self._exiftool.whenConnected()

        with tempfile.TemporaryDirectory() as workspace:
            outfile = os.path.join(workspace, str(uuid.uuid4()))
            yield exf_proto.execute(
                    "-PageImage",
                    "-b",
                    "-W", outfile,
                    "-listItem", str(self._page),
                    filename)

            with open(outfile, "rb") as stream:
                return stream.read(), b"image/jpeg"


class ExiftoolProtocolFactory(protocol.ClientFactory):

    def __init__(self, buffersize):
        self.buffersize = buffersize

    def buildProtocol(self, addr):
        proto = protocol.ClientFactory.buildProtocol(self, addr)
        proto.MAX_LENGTH = self.buffersize
        return proto


class ExiftoolJSONMetadataReverseProxyResource(ExtractionReverseProxyResource):

    def __init__(self, exiftool, backend, hostport, path):
        extraction = ExiftoolJSONMetadataExtraction(exiftool)
        super().__init__(extraction, backend, hostport, path)


class ExiftoolXMPMetadataReverseProxyResource(ExtractionReverseProxyResource):

    def __init__(self, exiftool, backend, hostport, path):
        extraction = ExiftoolXMPMetadataExtraction(exiftool)
        super().__init__(extraction, backend, hostport, path)


class ExiftoolPreviewReverseProxyResource(ExtractionReverseProxyResource):

    def __init__(self, exiftool, backend, hostport, path):
        extraction = ExiftoolPreviewExtraction(exiftool)
        super().__init__(extraction, backend, hostport, path)


class ExiftoolPageimagesReverseProxyResource(resource.Resource):

    def __init__(self, exiftool, backend, hostport, path):
        super().__init__()
        self._exiftool = exiftool
        self._backend = backend
        self._hostport = hostport
        self._path = path

    def getChild(self, page, request):
        extraction = ExiftoolPageimageMetadataExtraction(
            self._exiftool, int(page))
        return ExtractionReverseProxyResource(
            extraction, self._backend, self._hostport, self._path)
