from .. import defaults
from tempfile import NamedTemporaryFile as _ntf
from functools import wraps
from codecs import getwriter
import locale

if defaults.IS_PY2 or defaults.WINDOWS:
    locale.setlocale(locale.LC_CTYPE, '')

ENCODING = locale.getlocale()[1] or 'ascii'

if defaults.IS_PY2:
    @wraps(_ntf)
    def NamedTemporaryFile(mode):
        return getwriter(ENCODING)(_ntf(mode))

    def to_unicode(x):
        return x.decode(ENCODING)
else:
    NamedTemporaryFile = _ntf
    to_unicode = str