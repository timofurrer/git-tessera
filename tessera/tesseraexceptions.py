# -*- coding: utf-8 -*-


class TesseraError(Exception):
    pass


class ArgumentError(TesseraError):
    pass


class ConfigFileNotFoundError(TesseraError):
    def __init__(self, path):
        TesseraError.__init__(self, "cannot find config file at '%s'" % path)


class ConfigSectionNotFoundError(TesseraError):
    def __init__(self, section, path):
        TesseraError.__init__(self, "cannot find section %s in config file %s" % (section, path))


class ConfigOptionNotFoundError(TesseraError):
    def __init__(self, attribute, section, path):
        TesseraError.__init__(self, "cannot find option '%s' in section '%s' in config file '%s'" % (attribute, section, path))


class TesseraNotFoundError(TesseraError):
    def __init__(self, tessera_id):
        TesseraError.__init__(self, "cannot find tessera with id '%s'" % tessera_id)


class TesseraKeywordNotFoundError(TesseraError):
    def __init__(self, keyword, keywords):
        TesseraError.__init__(self, "tessera keyword '%s' does not exist. Use one keyword from '%s'" % (keyword, keywords))
