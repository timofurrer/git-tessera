# -*- coding: utf-8 -*-

import os
import dulwich
from gittle import Gittle

from tesseraexceptions import NoTesseraRepoError


class Git(object):
    @classmethod
    def is_dir_git_repo(cls, directory):
        return os.system("git rev-parse --is-inside-work-tree") == 0

    def __init__(self, gitpath):
        self._gitpath = gitpath
        try:
            self._gittle = Gittle(gitpath)
        except dulwich.errors.NotGitRepository:
            raise NoTesseraRepoError()

    @property
    def git_dir(self):
        """
            Returns the git dir.
        """
        return self._gittle.git_dir

    def is_working(self):
        """
            Checks if git is working
        """
        return self._gittle.is_working


    def commit_repo(self, tesserae, message):
        """
            Commits the git tessera files.
        """
        return self._gittle.commit(message=message, files=[os.path.relpath(tesserae.configpath, self._gitpath)])

    def add_tessera(self, tessera):
        """
            Commits a Tessera created by the create() method to the repository.
        """
        return self._gittle.commit(message="tessera created: %s" % tessera.title, files=[os.path.relpath(tessera.tessera_file, self._gitpath), os.path.relpath(tessera.info_file, self._gitpath)])

    def rm_tessera(self, tessera):
        """
            Removes a tessera and commits to git repository.
        """
        files = [str(os.path.relpath(tessera.tessera_file, self._gitpath)), str(os.path.relpath(tessera.info_file, self._gitpath))]
        self._gittle.rm(files)
        return self._gittle.commit(message="tessera removed: %s" % tessera.title, files=files)
