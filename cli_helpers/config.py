# -*- coding: utf-8 -*-
"""Read an app's config file.

Goal: single interface to reading all your app's config files

Write default file

"""

from __future__ import unicode_literals
import io
import logging
import os

from configobj import ConfigObj, ConfigObjError
from validate import ValidateError, Validator

from .compat import MAC, text_type, UserDict, WIN

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Base class for exceptions in this module."""
    pass


class ConfigValidationError(ConfigError):
    pass


class Config(UserDict, object):
    """Config class.

    :param str app_name: The application's name.
    :param str app_author: The application author/organization.
    :param str filename: The config filename to look for.
    :param dict/str default: The default config values or config file path.
    :param bool validate: Whether or not to validate the config file.
    :param bool write_default: Whether or not to write the default config
                               file to the user config directory if it doesn't
                               already exist.
    :param tuple additional_dirs: Additional directories to check for a config
                                  file.
    :raises ConfigValidationError: There was a validation error with the
                                   *default* file.
    """

    def __init__(self, app_name, app_author, filename, default=None,
                 validate=False, write_default=False, additional_dirs=()):
        super(self.__class__, self).__init__()

        self.default = {}
        self.default_file = self.default_config = None
        self.config_filenames = []

        self.app_name, self.app_author = app_name, app_author
        self.filename = filename
        self.write_default = write_default
        self.validate = validate
        self.additional_dirs = additional_dirs

        if isinstance(default, dict):
            self.default = default
            self.update(default)
        elif isinstance(default, text_type):
            self.default_file = default
        elif default is not None:
            raise TypeError(
                '"default" must be a dict or {}, not {}'.format(
                    text_type.__name__, type(default)))

        if self.write_default and not self.default_file:
            raise ValueError('Cannot use "write_default" without specifying '
                             'a default file.')

        if self.validate and not self.default_file:
            raise ValueError('Cannot use "validate" without specifying a '
                             'default file.')

        if self.default_file:
            self.read_default_config()

    def read_default_config(self):
        if self.validate:
            self.default_config = ConfigObj(configspec=self.default_file,
                                            list_values=False, _inspec=True,
                                            encoding='utf8')
            valid = self.default_config.validate(Validator(), copy=True,
                                                 preserve_errors=True)
            if valid is not True:
                for name, section in valid.items():
                    if section is True:
                        continue
                    for key, value in section.items():
                        if isinstance(value, ValidateError):
                            raise ConfigValidationError(
                                'section [{}], key "{}": {}'.format(
                                    name, key, value))
        elif self.default_file:
            self.default_config, _ = self.read_config_file(self.default_file)

        self.update(self.default_config)

    def read(self):
        return self.read_config_files(self.all_config_files())

    def user_config_file(self):
        return os.path.join(
            get_user_config_dir(self.app_name, self.app_author),
            self.filename)

    def system_config_files(self):
        return [os.path.join(f, self.filename) for f in get_system_config_dirs(
            self.app_name, self.app_author)]

    def additional_files(self):
        return [os.path.join(f, self.filename) for f in self.additional_dirs]

    def all_config_files(self):
        return (self.additional_files() + self.system_config_files() +
                [self.user_config_file()])

    def write_default_config(self, overwrite=False):
        destination = os.path.expanduser(self.user_config_file())
        if not overwrite and os.path.exists(destination):
            return

        with io.open(destination, mode='wb') as f:
            self.default_config.write(f)

    def read_config_file(self, f, **kwargs):
        """Read a config file."""
        configspec = self.default_file if self.validate else None
        try:
            config = ConfigObj(infile=f, configspec=configspec,
                               interpolation=False, encoding='utf8')
        except ConfigObjError as e:
            logger.warning(
                'Unable to parse line {} of config file {}'.format(
                    e.line_number, f))
            config = e.config

        valid = True
        if self.validate:
            valid = config.validate(Validator(), preserve_errors=True,
                                    copy=True)
        if bool(config):
            self.config_filenames.append(config.filename)

        return config, valid

    def read_config_files(self, files):
        """Read a list of config files."""
        errors = {}
        for _file in files:
            config, valid = self.read_config_file(_file)
            self.update(config)
            if valid is not True:
                errors[_file] = valid
        return errors or True


def get_user_config_dir(app_name, app_author, roaming=True, force_xdg=True):
    """Returns the config folder for the application.  The default behavior
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
      ``C:\\Users\<user>\AppData\Roaming\Acme\Foo Bar``
    Win 7 (not roaming):
      ``C:\\Users\<user>\AppData\Local\Acme\Foo Bar``

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
    if MAC and not force_xdg:
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
    if MAC and not force_xdg:
        return [os.path.join('/Library/Application Support', app_name)]
    dirs = os.environ.get('XDG_CONFIG_DIRS', '/etc/xdg')
    paths = [os.path.expanduser(x) for x in dirs.split(os.pathsep)]
    return [os.path.join(d, _pathify(app_name)) for d in paths]


def _pathify(s):
    """Convert spaces to hyphens and lowercase a string."""
    return '-'.join(s.split()).lower()
