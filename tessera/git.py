# -*- coding: utf-8 -*-

import os
from gittle import Gittle


class Git(object):
    @classmethod
    def is_dir_git_repo(cls, directory):
        return os.system("git rev-parse --is-inside-work-tree") == 0
