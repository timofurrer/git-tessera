# -*- coding: utf-8 -*-

import os
from shutil import copyfile
from gittle import Gittle
from glob import glob

from git import Git
from tessera import Tessera
from tesseraexceptions import TesseraError, NoTesseraRepoError, TesseraNotFoundError
from config import TesseraConfig
from editor import Editor


def verify_tessera_path(func):
    def _wrapper(self, *args, **kwargs):
        """
            Verifys if the tesserae path is a valid tesserae repository.
            Throws an exception on error or returns true.
        """
        if not self._is_tesserae_repo():
            raise NoTesseraRepoError()
        return func(self, *args, **kwargs)
    return _wrapper


def check_tessera_id(func):
    def _wrapper(self, tessera_id, *args, **kwargs):
        """
            Checks if the tessera id exists and returns resolve's the short ids not full ones.
        """
        tessera_id = self._get_real_tessera_id(tessera_id)
        return func(self, tessera_id, *args, **kwargs)
    return _wrapper


class Tesserae(object):
    CONFIG_TEMPLATE = "/home/tuxtimo/work/git-tessera2/templates/config"
    ROOT_DIRECTORY = ".tesserae"

    LS_HEADER = ("Id", "Title", "Status", "Type", "Priority", "Author", "Last updated")

    def __init__(self, path):
        self._git = Git(path)
        self._path = path
        self._configpath = os.path.join(self.tesseraepath, "config")

    @property
    def path(self):
        return self._path

    @property
    def tesseraepath(self):
        return os.path.join(os.path.dirname(self._git.git_dir), Tesserae.ROOT_DIRECTORY)

    @property
    def configpath(self):
        return self._configpath

    def _is_tesserae_repo(self):
        """
            Checks whether the path is a tesserae repository or not.
        """
        try:
            return os.path.exists(self.tesseraepath)
        except Gittle.NoGitRepository:
            return False

    def _get_real_tessera_id(self, tessera_id):
        """
            Returns the real tessera id.
            This method evaluates the full tessera id of a short tessera id.
        """
        try:
            return os.path.basename(glob(os.path.join(self.tesseraepath, tessera_id + "*"))[0])
        except IndexError:
            raise TesseraNotFoundError(tessera_id)

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
            self._git.is_working()
        except Gittle.NoGitRepository:
            print("error: not a git repository")
            return False

        if self._is_tesserae_repo():
            print("error: already initialized tesserae repository here")
            return False

        os.makedirs(self.tesseraepath)
        copyfile(Tesserae.CONFIG_TEMPLATE, self._configpath)

        self._git.commit_repo(self, "tesserae initialized")
        print("Initialized empty git tesserae repository in %s" % self.tesseraepath)
        return True

    @verify_tessera_path
    @check_tessera_id
    def show(self, tessera_id):
        """
            Shows a specific tessera by passing the tessera_id parameter.
        """
        t = Tessera(tessera_id, os.path.join(self.tesseraepath, tessera_id))
        print(t.raw_tessera_file_content)
        return True

    @verify_tessera_path
    def ls(self, order_by, order_type, filter_types):
        """
            Lists all tesserae and show basic information.
        """
        tesserae = self._get_all_tesserae()

        if not tesserae:
            print("no tesserae created yet. Use git tessera create 'title' to create a new tessera")
            return True

        rows = [(t.short_id, t.title, ", ".join(t.keywords.get("status", ["unknown"])), ", ".join(t.keywords.get("type", ["unknown"])), t.keywords.get("priority", ["0"])[0], t.metadata.get("author", ["unknown"]), t.metadata.get("updated"))
                for t in tesserae if not filter_types or filter_types.intersection(t.keywords.get("type"))]

        if not rows:
            print("no tesserae found which matched your query")
            return True

        if order_by:
            order_by = order_by.lower()
            headers = [x.lower() for x in Tesserae.LS_HEADER]
            try:
                index = headers.index(order_by)
            except ValueError:
                raise TesseraError("cannot order by '%s' because this columns does not exist. Available colums are: '%s'" % (order_by, headers))

            rows = sorted(rows, key=lambda r: float(r[index]) if r[index].isdigit() else r[index], reverse=order_type == "desc")

        rows.insert(0, Tesserae.LS_HEADER)
        widths = [max(map(len, column)) for column in zip(*rows)]
        for n, r in enumerate(rows):
            print("  ".join(data.ljust(width) for data, width in zip(r, widths)))
            if n == 0:
                print("=" * (sum(widths) + 2 * len(widths)))
        return True

    @verify_tessera_path
    def create(self, title):
        """
            Creates a new tessera.
        """
        tessera = Tessera.create(self.tesseraepath, title)

        if not Editor.open(tessera.tessera_file, TesseraConfig(self._configpath)):
            tessera.remove()
            return False

        if not self._git.add_tessera(tessera):
            print("error: cannot commit new tessera")
            tessera.remove()
            return False

        print("Created new tessera with id %s" % tessera.id)
        return True

    @verify_tessera_path
    @check_tessera_id
    def remove(self, tessera_id):
        """
            Removes a tessera by it's id.
        """
        tessera = Tessera(tessera_id, os.path.join(self.tesseraepath, tessera_id))
        tessera.remove()

        if not self._git.rm_tessera(tessera):
            print("error: cannot remove tessera")
            return False

        print("Removed tessera with id '%s'" % tessera.id)
        return True

    @verify_tessera_path
    @check_tessera_id
    def edit(self, tessera_id):
        """
            Edits a tessera by it's id.
        """
        tessera = Tessera(tessera_id, os.path.join(self.tesseraepath, tessera_id))

        if not Editor.open(tessera.tessera_file, TesseraConfig(self._configpath)):
            print("error: cannot updated tessera")
            return False

        tessera.update()

        if not self._git.update_tessera(tessera):
            print("error: cannot commit updated tessera")
            return False

        print("Updated tessera with id %s" % tessera.id)
        return True
