#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder
    """
    local("mkdir -p versions")
    path = ("versions/web_static_{}.tgz"
            .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    result = local("tar -cvzf {} web_static"
                   .format(path))

    if result.failed:
        return None
    return path
