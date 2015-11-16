#coding:utf-8
import errno
import fcntl
import os


class LockError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.args[0]) + ')'


class LocalMutex(object):
    def __init__(self, path, wait = False, remove = True):
        object.__init__(self)
        self._path = path
        self._fd = None
        self._remove = remove

        while self._fd is None:
            # Open the file
            fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0666)
            try:
                # Acquire an exclusive lock
                if wait:
                    fcntl.lockf(fd, fcntl.LOCK_EX)
                else:
                    try:
                        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except IOError, e:
                        if e.errno in (errno.EACCES, errno.EAGAIN):
                            raise LockError(
                                'Lock file is held by another process: '
                                + repr(self._path))
                        else:
                            raise

                try:
                    stat1 = os.stat(path)
                except OSError, e:
                    if e.errno != errno.ENOENT:
                        raise
                else:
                    stat2 = os.fstat(fd)
                    if stat1.st_dev == stat2.st_dev \
                        and stat1.st_ino == stat2.st_ino:

                        self._fd = fd

            finally:
                # Close the file if it is not the required one
                if self._fd is None:
                    os.close(fd)

    def __enter__(self):
        if self._fd is None:
            raise ValueError('This lock is released')

        return self

    def __repr__(self):
        repr_str = '<'
        if self._fd is None:
            repr_str += 'released'
        else:
            repr_str += 'acquired'

        repr_str += ' lock file ' + repr(self._path) + '>'
        return repr_str

    def get_path(self):
        if self._fd is None:
            raise ValueError('This lock file is released')

        return self._path

    def fileno(self):
        if self._fd is None:
            raise ValueError('This lock file is released')

        return self._fd

    def release(self):
        if self._fd is None:
            raise ValueError('This lock file is already released')

        try:
            if self._remove:
                os.remove(self._path)
        finally:
            try:
                os.close(self._fd)
            finally:
                self._fd = None

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
