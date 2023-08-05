
def _match_prop(opts, prop, val):
    return prop in opts and opts[prop] == val


class AnalyserOptions:
    def __init__(self, includeCopyright=False, filterFiles=True):
        self.includeCopyright = includeCopyright
        self.filterFiles = filterFiles

    def match(self, opts: dict):
        return opts and \
               _match_prop(opts, 'includeCopyright', self.includeCopyright) and \
               _match_prop(opts, 'filterFiles', self.filterFiles)


class FileAnalyser(object):
    def __call__(self, path, opts=AnalyserOptions()):
        return self.analyse(path, opts) if self.accepts(path, opts) else None

    def accepts(self, path, opts=AnalyserOptions()):
        if path.is_file() and self.match(path, opts):
            return True
        else:
            return False

    def match(self, path, opts):
        raise NotImplementedError()

    def analyse(self, path, opts):
        raise NotImplementedError()
