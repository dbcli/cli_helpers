# -*- coding: utf-8 -*-
"""Read an app's config file."""

from __future__ import unicode_literals
import os
import sys

from .compat import WIN


def get_user_config_dir(app_name, app_author, roaming=True, force_xdg=True):
    r"""Returns the config folder for the application.  The default behavior
    is to return whatever is most appropriate for the operating system.

    To give you an idea, for an app called ``"Foo Bar"`` by ``"Acme"``,
    something like the following folders could be returned:

    macOS (non-XDG):
      ``~/Library/Application Support/Foo Bar``
    Mac OS X (XDG):
      ``~/.config/foo-bar``
    Unix:
      ``~/.config/foo-bar``
    Win 7 (roaming):
      ``C:\Users\<user>\AppData\Roaming\Acme\Foo Bar``
    Win 7 (not roaming):
      ``C:\Users\<user>\AppData\Local\Acme\Foo Bar``

    :param app_name: the application name. This should be properly capitalized
                     and can contain whitespace.
    :param app_author: The app author's name (or company). This should be
                       properly capitalized and can contain whitespace.
    :param roaming: controls if the folder should be roaming or not on Windows.
                    Has no effect on non-Windows systems.
    :param force_xdg: if this is set to `True`, then on macOS the XDG Base
                      Directory Specification will be followed. Has no effect
                      on non-macOS systems.

    """

    if WIN:
        key = 'APPDATA' if roaming else 'LOCALAPPDATA'
        folder = os.path.expanduser(os.environ.get(key, '~'))
        return os.path.join(folder, app_author, app_name)
    if sys.platform == 'darwin' and not force_xdg:
        return os.path.join(os.path.expanduser(
            '~/Library/Application Support'), app_name)
    return os.path.join(
        os.path.expanduser(os.environ.get('XDG_CONFIG_HOME', '~/.config')),
        _pathify(app_name))


def get_system_config_dirs(app_name, app_author, force_xdg=True):
    r"""Returns a list of system-wide config folders for the application.

    To give you an idea, for an app called ``"Foo Bar"`` by ``"Acme"``,
    something like the following folders could be returned:

    macOS (non-XDG):
      ``['/Library/Application Support/Foo Bar']``
    Mac OS X (XDG):
      ``['/etc/xdg/foo-bar']``
    Unix:
      ``['/etc/xdg/foo-bar']``
    Win 7:
      ``['C:\ProgramData\Acme\Foo Bar']``

    :param app_name: the application name. This should be properly capitalized
                     and can contain whitespace.
    :param app_author: The app author's name (or company). This should be
                       properly capitalized and can contain whitespace.
    :param force_xdg: if this is set to `True`, then on macOS the XDG Base
                      Directory Specification will be followed. Has no effect
                      on non-macOS systems.

    """
    if WIN:
        folder = os.environ.get('PROGRAMDATA')
        return [os.path.join(folder, app_author, app_name)]
    if sys.platform == 'darwin' and not force_xdg:
        return [os.path.join('/Library/Application Support', app_name)]
    dirs = os.environ.get('XDG_CONFIG_DIRS', '/etc/xdg')
    paths = [os.path.expanduser(x) for x in dirs.split(os.pathsep)]
    return [os.path.join(d, _pathify(app_name)) for d in paths]


def _pathify(s):
    """Convert spaces to hyphens and lowercase a string."""
    return '-'.join(s.split()).lower()
