import os
import errno
from shutil import rmtree
from stat import S_IWUSR
from tempfile import mkstemp, mkdtemp

class TempFile(object):
    def _create(self):
        self._fd, self._path = mkstemp()
        return self._path
    def _delete(self):
        os.close(self._fd)
        os.remove(self._path)
    def __enter__(self):
        return self._create()
    def __exit__(self, type, value, traceback):
        self._delete()

class _Unreadable(object):
    ''' Trait to make resources unreadable. Assume self._path is available in the mixin. '''
    def _save_chmod(self):
        self._chmod  = os.stat(self._path).st_mode
    def _make_unreadable(self):
        self._save_chmod()
        os.chmod(self._path, S_IWUSR)
    def _make_readable(self):
        os.chmod(self._path, self._chmod)

class UnreadableTempFile(TempFile, _Unreadable):
    def __enter__(self):
        self._create()
        self._make_unreadable()
        return self._path
    def __exit__(self, type, value, traceback):
        self._make_readable()
        self._delete()

class TempDir(TempFile):
    def _create(self):
        self._path = mkdtemp()
        return self._path
    def _delete(self):
        try:
            rmtree(self._path)
        except OSError as e:
            if e.errno != errno.ENOENT:  # Other error than 'No such file or directory'.
                raise

class UnreadableTempDir(TempDir, _Unreadable):
    def __enter__(self):
        self._create()
        self._make_unreadable()
        return self._path
    def __exit__(self, type, value, traceback):
        self._make_readable()
        self._delete()
