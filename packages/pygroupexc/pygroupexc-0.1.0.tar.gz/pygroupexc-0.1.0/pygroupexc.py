"""
Small library for providing unique identifier to similar exceptions

1) we check just filename and function name
2) we don't check line numbers because they often change e.g. by unrelated changes
3) we check exception type but not message as the message can often differ for similar problems

the code is public-domain
written by Frantisek Jahoda
"""

import os
import re
import sys
import hashlib


EXC_MAPPING = {
    AttributeError: r"'(\w+)' object has no attribute '(\w+)'",
}

def _get_exception_attributes(exc_class, exc):
    regex = EXC_MAPPING.get(exc_class)
    if not regex:
        return []
    match = re.fullmatch(regex, str(exc))
    if not match:
        return []
    return match.groups()



def format_exception(exc_info=None, root=None):
    if not exc_info:
        exc_info = sys.exc_info()
    exc_class, exc, traceback = exc_info
    rows = []
    while traceback:
        code = traceback.tb_frame.f_code
        filename = code.co_filename
        if root:
            filename = os.path.relpath(filename, root)
        if not rows or rows[-1] != (filename, code.co_name):
            rows.append((filename, code.co_name))
        traceback = traceback.tb_next
    rows.append(exc_class.__name__)
    attributes = _get_exception_attributes(exc_class, exc)
    rows.extend(attributes)
    return rows


def exception_id(**kwargs):
    return hashlib.md5(str(format_exception(**kwargs)).encode()).hexdigest()

