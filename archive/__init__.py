import os, tarfile, zipfile, gzip


"""
Un-archiver


How-to unarchive:
`Archive('arch.zip').extract()` will extract files in current directory
`Archive('arch.zip').extract('/path/to')` will extract files in directory /path/to
"""


READ_BLOCKS = 2048

class Archive(object):

    def __init__(self, path, ext=None):

        if ext is None:
            ext = self._guess_extension(path)
        elif not ext.startswith('.'):
            ext = '.%s' % ext

        if ext is None or ext == '':
            raise ValueError('Archive extension not recognized. Rename your file properly with a valid extension or provide the extension as a parameter.')

        _archive_class = extensions_map.get(ext, None)

        if _archive_class is None:
            for k, v in extensions_map.iteritems():
                if ext.lower().endswith(k): _archive_class = v
            if _archive_class is None: raise ValueError('Extension %s is a not recognized archive format for this module.' % ext)

        self._archive = _archive_class(path)

    def _guess_extension(self, path):
        """
        Guess the extension of the inputted file by looking at it's path.
        """
        base, current = os.path.splitext(path)
        ext = current
        while current != '':
            base, current = os.path.splitext(base)
            ext = current + ext
        return ext

    def list(self):
        """
        List all supported extensions.
        """
        return ', '.join([key for key in _extensions_map.keys()])


    def extract(self, out=None):
        """
        Extract archive to the current directory or to the out specified.
        """
        self._inside(out)
        return self._archive.extract(out)

    def _inside(self, path=None):
        """
        Check if all elements from the tar archive are `inside` the path (That archive do not contains file with `..`
        that can reference possible system files outside the path).
        """
        if path is None:
            path = os.getcwd()
        path = os.path.normpath(path)
        for fname in self.names():
            out = os.path.normpath(os.path.join(path, fname))
            if not out.startswith(path):
                raise Exception("Unsafe archive : archive member (%s) will be un-archived outside the target (%s) at %s" % (fname, path, out))

    def names(self):
        """
        Retrieve the archive members by names
        """
        return self._archive.names()







class TarArchive(Archive):

    def __init__(self, path):
        self._archive = tarfile.open(path)

    def extract(self, out=None):
        self._archive.extractall(path=out)

    def names(self):
        return self._archive.getnames()


class ZipArchive(Archive):

    def __init__(self, path):
        self._archive = zipfile.ZipFile(path)

    def extract(self, out=None):
        self._archive.extractall(path=out)

    def names(self):
        return self._archive.namelist()

class GzipArchive(Archive):

    def __init__(self, path):
        self.path = path

    def extract(self, out=None):
        if out is None: out = os.path.join('.', '')
        out = os.path.join(out, self.names()[0])
        with open(out, 'wb') as outf:
            with gzip.open(self.path, 'rb') as inf:
                while True:
                    data = inf.read(READ_BLOCKS)
                    if len(data) == 0 : break
                    outf.write(data)

    def names(self):
        return [os.path.split(self.path[:-3])[-1]]




extensions_map = {
    '.tar.gz' : TarArchive,
    '.tgz': TarArchive,
    '.tar' : TarArchive,
    '.bz2' : TarArchive,
    '.zip' : ZipArchive,
    '.gz' : GzipArchive,
}