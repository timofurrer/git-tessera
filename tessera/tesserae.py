# -*- coding: utf-8 -*-

import os
from shutil import copyfile
from gittle import Gittle
from glob import glob

from tessera import Tessera
from tesseraexceptions import TesseraError, TesseraNotFoundError


class Tesserae(object):
    CONFIG_FOLDER = "/home/tuxtimo/work/git-tessera2/templates/config"
    ROOT_DIRECTORY = ".tesserae"

    LS_HEADER = ("Id", "Title", "Status", "Type", "Author", "Last updated")

    def __init__(self, path):
        self._git = Gittle(path)
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def tesseraepath(self):
        return os.path.join(os.path.dirname(self._git.git_dir), Tesserae.ROOT_DIRECTORY)

    def _is_tesserae_repo(self):
        """
            Checks whether the path is a tesserae repository or not.
        """
        try:
            return os.path.exists(self.tesseraepath)
        except Gittle.NoGitRepository:
            return False

    def _verify_path(self):
        """
            Verifys if the tesserae path is a valid tesserae repository.
            Throws an exception on error or returns true.
        """
        if not self._is_tesserae_repo():
            print("error: not a git tessera repository")
            return False
        return True

    def _exists(self, tessera_id):
        """
            Returns wheter a tessera with the given id exists or not.
        """
        return os.path.exists(os.path.join(self.tesseraepath, tessera_id))

    def _get_real_tessera_id(self, tessera_id):
        """
            Returns the real tessera id.
            This method evaluates the full tessera id of a short tessera id.
        """
        return glob(os.path.join(self.tesseraepath, tessera_id + "*"))[0]

    def _get_all_tesserae(self):
        """
            Returns all tesserae.
        """
        tesserae = []
        for tessera_id in os.listdir(self.tesseraepath):
            path = os.path.join(self.tesseraepath, tessera_id)
            if not os.path.isdir(path):
                continue

            tesserae.append(Tessera(tessera_id, path))
        return tesserae

    def init(self):
        """
            Initialize empty git tesserae repository inside git repository.
        """
        try:
            self._git.is_working
        except Gittle.NoGitRepository:
            print("error: not a git repository")
            return False

        if self._is_tesserae_repo():
            print("error: already initialized tesserae repository here")
            return False

        os.makedirs(self.tesseraepath)
        copyfile(Tesserae.CONFIG_FOLDER, os.path.join(self.tesseraepath, "config"))

        print("Initialized empty git tesserae repository in %s" % self.tesseraepath)
        return True

    def show(self, tessera_id):
        """
            Shows a specific tessera by passing the tessera_id parameter.
        """
        tessera_id = self._get_real_tessera_id(tessera_id)

        if not self._exists(tessera_id):
            raise TesseraNotFoundError(tessera_id)

        t = Tessera(tessera_id, os.path.join(self.tesseraepath, tessera_id))
        print(t.raw_tessera_file_content)
        return True

    def ls(self, order_by, order_type):
        """
            Lists all tesserae and show basic information.
        """
        if not self._verify_path():
            return False

        tesserae = self._get_all_tesserae()
        rows = [(t.short_id, t.title, ", ".join(t.keywords.get("status", ["unknown"])), ", ".join(t.keywords.get("type", ["unknown"])), t.metadata.get("author", ["unknown"]), t.metadata.get("updated")) for t in tesserae]

        if order_by:
            order_by = order_by.lower()
            headers = [x.lower() for x in Tesserae.LS_HEADER]
            try:
                index = headers.index(order_by)
            except ValueError:
                raise TesseraError("cannot order by '%s' because this columns does not exist. Available colums are: '%s'" % (order_by, headers))

            rows = sorted(rows, key=lambda r: r[index], reverse=order_type == "desc")

        rows.insert(0, Tesserae.LS_HEADER)
        widths = [max(map(len, column)) for column in zip(*rows)]
        for n, r in enumerate(rows):
            print("  ".join(data.ljust(width) for data, width in zip(r, widths)))
            if n == 0:
                print("=" * (sum(widths) + 2 * len(widths)))

    def create(self, title):
        """
            Creates a new tessera.
        """
        if not self._verify_path():
            return False

        tessera = Tessera.create(self.tesseraepath, title)
