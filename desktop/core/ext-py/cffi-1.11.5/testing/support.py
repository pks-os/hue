import sys

if sys.version_info < (3,):
    __all__ = ['u']

    class U(object):
        def __add__(self, other):
            return eval('u'+repr(other).replace(r'\\u', r'\u')
                                       .replace(r'\\U', r'\U'))
    u = U()
    long = long     # for further "from testing.support import long"
    assert u+'a\x00b' == eval(r"u'a\x00b'")
    assert u+'a\u1234b' == eval(r"u'a\u1234b'")
    assert u+'a\U00012345b' == eval(r"u'a\U00012345b'")

else:
    __all__ = ['u', 'unicode', 'long']
    u = ""
    unicode = str
    long = int


class StdErrCapture(object):
    """Capture writes to sys.stderr (not to the underlying file descriptor)."""
    def __enter__(self):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO
        self.old_stderr = sys.stderr
        sys.stderr = f = StringIO()
        return f
    def __exit__(self, *args):
        sys.stderr = self.old_stderr


class FdWriteCapture(object):
    """xxx limited to capture at most 512 bytes of output, according
    to the Posix manual."""

    def __init__(self, capture_fd=2):    # stderr by default
        if sys.platform == 'win32':
            import py
            py.test.skip("seems not to work, too bad")
        self.capture_fd = capture_fd

    def __enter__(self):
        import os
        self.read_fd, self.write_fd = os.pipe()
        self.copy_fd = os.dup(self.capture_fd)
        os.dup2(self.write_fd, self.capture_fd)
        return self

    def __exit__(self, *args):
        import os
        os.dup2(self.copy_fd, self.capture_fd)
        os.close(self.copy_fd)
        os.close(self.write_fd)
        self._value = os.read(self.read_fd, 512)
        os.close(self.read_fd)

    def getvalue(self):
        return self._value
