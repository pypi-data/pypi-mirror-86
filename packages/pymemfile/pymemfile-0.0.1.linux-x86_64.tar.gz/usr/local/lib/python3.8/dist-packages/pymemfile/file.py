import os
import io


class FileAlreadyOpenError(Exception):
    pass


class FileNotOpenError(Exception):
    pass


class FileReadOnlyError(Exception):
    pass


class MemFile(object):
    def __init__(self, fnam, mode="r+b"):

        self._fnam = fnam
        self._mode = mode
        self._open = False

        self._is_readonly = self._chk_readonly()
        self._is_binary = "b" in self._mode
        self._is_overwrite = "w" in self._mode
        self._is_append = "a" in self._mode

        self._create_stream()

    def __repr__(self):
        return (
            self.__class__.__name__
            + "( path='"
            + self._fnam
            + "' open="
            + str(self._open)
            + " )"
        )

    def _create_stream(self):
        if self._is_binary:
            self._b = io.BytesIO()
        else:
            self._b = io.StringIO()

    def _raise_open(self):
        if not self._open:
            raise FileNotOpenError()

    def _chk_readonly(self):
        if "+" in self._mode:
            return False
        if "w" in self._mode:
            return False
        return True

    def open(self):
        if self._open:
            raise FileAlreadyOpenError()

        self._open = True

        if self._is_overwrite:
            self._create_stream()
        if self._is_append:
            self.seek(0, os.SEEK_END)
        else:
            self.seek(0)

        return self

    def close(self):
        self._open = False

    def write(self, data):
        self._raise_open()
        if self._is_readonly:
            raise FileReadOnlyError()
        return self._b.write(data)

    def read(self, count=-1):
        self._raise_open()
        data = self._b.read(count)
        return data

    def seek(self, offset, whence=os.SEEK_SET):
        self._raise_open()
        return self._b.seek(offset, whence)

    def tell(self):
        self._raise_open()
        return self.seek(0, os.SEEK_CUR)

    def fileno(self):
        self._raise_open()
        return self._b

    def __enter__(self):
        self.open()

    def __exit__(self, t, v, tb):
        self.close()
