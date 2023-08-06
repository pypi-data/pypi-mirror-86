Exifproxy
=========

.. image:: https://travis-ci.com/znerol/exifproxy.svg?branch=master
    :target: https://travis-ci.com/znerol/exifproxy


Metadata extraction reverse proxy based on twisted_ and exiftool_.

.. _exiftool: http://www.sno.phy.queensu.ca/~phil/exiftool/
.. _twisted: https://twistedmatrix.com/


Installation
------------

::

   python3 -m pip install exifproxy


Usage
-----

::

   twist exifproxy --help
   Usage: twist [options] plugin [plugin_options] exifproxy [options]
   Options:
         --backend=  Url to backend, no trailing slash [default: http://localhost]
         --help      Display this help and exit.
         --listen=   Listen port (strports syntax) [default: tcp:8080]
         --version   Display Twisted version and exit.


Requests to one of the proxy endpoints will be forwarded to the backend. When a
successful result is returned from the backend, content is extracted from the
body and sent to the client. The following proxy endpoints are available:

/json
  All metadata is extracted from the backend response using
  ``exiftool -j -g -a -struct`` and returned to the client with
  ``Content-Type`` header set to ``application/json``.
/xmp
  The ``xmp`` packet is extracted from the response and returned to the client
  with ``Content-Type`` header set to ``application/rdf+xml``.
/preview
  The first preview image is extracted from the backend response and returned
  to the client as a JPEG image.
/pageimage/{N}
  The Nth page image is extracted from the backend response and returned to the
  client as a JPEG image. Index starts from ``0``.


Tryout
------

Run ``twist exifproxy --backend=https://raw.githubusercontent.com/exiftool/exiftool/master/t/images``

Then use ``curl`` to access any of the exiftool example images_ through one of the proxy endpoints:

::

   curl http://localhost/xmp/Photoshop.psd
   curl http://localhost/json/GIMP.xcf

.. _images: https://github.com/exiftool/exiftool/tree/master/t/images


License
-------

The software is subject to the AGPLv3_ or later license.


.. _AGPLv3: https://www.gnu.org/licenses/agpl-3.0.en.html
