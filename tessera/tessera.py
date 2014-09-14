# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from dulwich.config import StackedConfig
from uuid import uuid1 as generate_uniq_id

from tesseraexceptions import TesseraKeywordNotFoundError


class Tessera(object):
    NEW_TESSERA_TEMPLATE = "/home/tuxtimo/work/git-tessera2/templates/new_tessera"

    TESSERA_FILENAME = "tessera"
    INFO_FILENAME = "info"

    KEYWORDS = ["status", "type", "priority", "tags"]

    @classmethod
    def create(cls, basepath, title):
        t_id = str(generate_uniq_id())
        t_path = os.path.join(basepath, t_id)
        t_file = os.path.join(t_path, Tessera.TESSERA_FILENAME)
        t_info = os.path.join(t_path, Tessera.INFO_FILENAME)

        os.makedirs(t_path)

        with open(Tessera.NEW_TESSERA_TEMPLATE, "r") as fin:
            with open(t_file, "w+") as fout:
                for l in fin.readlines():
                    if l == "@title@\n":
                        l = "# %s\n" % title
                    fout.write(l)

        with open(t_info, "w+") as f:
            c = StackedConfig(StackedConfig.default_backends())
            f.write("author: %s\n" % c.get("user", "name"))
            f.write("email: %s\n" % c.get("user", "email"))
            f.write("updated: %s\n" % datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

        t = Tessera(t_id, t_path)
        return t

    def __init__(self, tessera_id, tessera_path):
        self._id = tessera_id
        self._short_id = tessera_id.split("-", 1)[0]
        self._path = tessera_path
        self._tessera_file = os.path.join(tessera_path, Tessera.TESSERA_FILENAME)
        self._info_file = os.path.join(tessera_path, Tessera.INFO_FILENAME)

        self._title = None
        self._description = ""
        self._metadata = {}
        self._keywords = {}

        self._raw_tessera_file_content = ""
        self._raw_info_file_content = ""

        self._parse_tessera_file()
        self._parse_info_file()

    @property
    def id(self):
        """
            Returns the tessera id.
            This is an uniq number created with uuid.
        """
        return self._id

    @property
    def short_id(self):
        """
            Returns the short id of the tessera.
        """
        return self._short_id

    @property
    def path(self):
        """
            Returns the tessera's basepath.
        """
        return self._path

    @property
    def title(self):
        """
            Returns the tessera's title from the tessera file.
        """
        return self._title

    @property
    def description(self):
        """
            Returns the tessera's description from the tessera file.
        """
        return self._description

    @property
    def metadata(self):
        """
            Returns the tessera's metadata.
        """
        return self._metadata

    @property
    def keywords(self):
        """
            Returns the tessera's keywords and it's values.
        """
        return self._keywords

    @property
    def tessera_file(self):
        """
            Returns the tessera's file path.
        """
        return self._tessera_file

    @property
    def info_file(self):
        """
            Returns the tessera's info file path.
        """
        return self._info_file

    @property
    def raw_tessera_file_content(self):
        """
            Returns the raw tessera file content.
        """
        return self._raw_tessera_file_content

    @property
    def raw_info_file_content(self):
        """
            Returns the raw info file content.
        """
        return self._raw_info_file_content

    def _parse_tessera_file(self):
        """
            Parses the tessera file.
        """
        with open(self._tessera_file, "r") as f:
            for n, l in enumerate(f.read().splitlines()):
                self._raw_tessera_file_content += l + "\n"
                l = l.strip()
                if l.startswith("//"):  # line is a comment
                    continue

                if n == 0:  # title must be on first line
                    self._title = l.replace("#", "").strip()
                if l.startswith("@"):  # line contains a keyword
                    keyword, values = l[1:].split(" ", 1)
                    if keyword not in Tessera.KEYWORDS:
                        raise TesseraKeywordNotFoundError(keyword, Tessera.KEYWORDS)
                    self._keywords[keyword] = [x.strip() for x in values.split(",")]
                else:
                    self._description += l + "\n"

    def _parse_info_file(self):
        """
            Parses the info file.
        """
        with open(self._info_file, "r") as f:
            for l in f.read().splitlines():
                self._raw_info_file_content += l + "\n"
                key, value = l.split(":", 1)
                self._metadata[key.strip()] = value.strip()

    def _write_info_file(self):
        """
            Writes the info file.
        """
        with open(self._info_file, "w+") as f:
            for k, v in self._metadata.iteritems():
                f.write("%s: %s\n" % (k, v))

    def update(self):
        """
            Updates the timestamp of this tessera.
        """
        self._metadata["updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self._write_info_file()

    def remove(self):
        """
            Removes this tessera.
        """
        shutil.rmtree(self._path)
