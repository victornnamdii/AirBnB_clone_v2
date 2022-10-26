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
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir versions")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("tar -zvcf {} web_static".format(filename))
    if result.failed:
        return None
    return result
