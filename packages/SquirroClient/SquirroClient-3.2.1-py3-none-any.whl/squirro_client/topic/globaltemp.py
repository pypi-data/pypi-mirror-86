from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import os
from builtins import object

from squirro_client.exceptions import NotFoundError, UnknownError


class GlobalTempMixin(object):
    def new_tempfile_from_localfile(self, filename):
        """Stores the file identified by `file_name` on Squirro's global temp
        folder.

        :param filename: Name of the file on local filesystem to be uploaded to
            the server
        """
        if not os.path.exists(filename):
            raise ValueError("Can not find file {}".format(filename))

        data = open(filename, "rb").read()
        return self.new_tempfile(data=data)

    def new_tempfile(self, data):
        """Stores the `data` in a temp file.

        :param data: data to be stored in the temp file
        """

        url = "%(ep)s/v0/%(tenant)s/temp" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
        }
        headers = {}
        res = self._perform_request("post", url, files={"file": data}, headers=headers)
        return self._process_response(res, [201])

    def get_tempfile(self, filename):
        """Returns the content of the temp file with the name `filename`.

        :param filename: File name
        """

        url = "%(ep)s/v0/%(tenant)s/temp" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
        }
        res = self._perform_request("get", url, params={"filename": filename})
        if res.status_code == 404:
            raise NotFoundError(res.status_code, "Not found")
        elif res.status_code != 200:
            raise UnknownError(res.status_code, "")
        else:
            return res.content
