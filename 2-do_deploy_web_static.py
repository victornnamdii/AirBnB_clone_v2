#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static folder, using
a function do_pack.

Distributes an archive to my web servers, using the function do_deploy
"""

from fabric.api import local, put, run, env
from datetime import datetime
import os
env.hosts = ['3.235.25.172', '54.164.176.89']


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


def do_deploy(archive_path):
    """
    Distributes an archive to my web servers.
    """
    if not os.path.exists(archive_path):
        return False
    archive_name = archive_path.split('/')[-1]
    no_ext = archive_name.split('.')[0]
    path = '/data/web_static/releases/'
    put(archive_path, "/tmp/")
    try:
        run("mkdir -p {}{}".format(path, no_ext))
        run("tar -xvf /tmp/{} -C {}{}/".format(archive_name,
                                               path, no_ext))
        run("rm /tmp/{}".format(archive_name))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))
        run("rm -rf {}{}/web_static".format(path, no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{} /data/web_static/current".format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False
