# -*- coding: utf-8 -*-

from subprocess import Popen
from os import getenv


class Editor(object):
    """
        This class represents an editor.
        It can load a template file and or a file on the filesystem and open it in the configured editor of the system.
        The editor which is used for the files is choosen by this pattern:
            1. core.editor is defined in config file
            2. if sensible-editor command is available
            3. if $EDITOR environment variable is set
            4. no editor found
    """
    @staticmethod
    def open(files, config):
        """
            Opens the file.
        """
        if isinstance(files, basestring):
            files = [files]

        # choose the right editor
        try:
            p = Popen([config.get("core", "editor")] + files)
        except TesseraError:
            try:
                p = Popen(["sensible-editor"] + files)
            except Exception:
                editor = getenv("EDITOR")
                if editor is None:
                    raise TesseraError("no editor found to open files. Please configure core.editor in your git configuration")
                p = Popen([editor] + files)
        return p.wait()
