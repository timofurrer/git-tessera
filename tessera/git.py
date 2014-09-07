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

    def commit(self, tessera, message):
        """
            commits a Tessera created by the create() method to the repository.
        """
        return self._gittle.commit(message=message, files=[os.path.relpath(tessera.tessera_file, self._gitpath), os.path.relpath(tessera.info_file, self._gitpath)])
