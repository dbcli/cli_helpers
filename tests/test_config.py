# -*- coding: utf-8 -*-
"""Test the cli_helpers.config module."""

from __future__ import unicode_literals
import os
import sys

from mock import MagicMock
import pytest

from cli_helpers.compat import MAC, text_type, WIN
from cli_helpers.config import (Config, ConfigValidationError,
                                get_system_config_dirs, get_user_config_dir,
                                _pathify)
from .utils import with_temp_dir

APP_NAME, APP_AUTHOR = 'Test', 'Acme'
TEST_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG = {
    'section':  {
        'test_boolean_default': 'True',
        'test_string_file': '~/myfile',
        'test_option': 'foobar'
    }
}
DEFAULT_VALID_CONFIG = {
    'section':  {
        'test_boolean_default': True,
        'test_string_file': '~/myfile',
        'test_option': 'foobar'
    }
}


def _mocked_user_config(temp_dir, *args, **kwargs):
    config = Config(*args, **kwargs)
    config.user_config_file = MagicMock(return_value=os.path.join(
        temp_dir, config.filename))
    return config


def test_user_config_dir():
    """Test that the config directory is a string with the app name in it."""
    if 'XDG_CONFIG_HOME' in os.environ:
        del os.environ['XDG_CONFIG_HOME']
    config_dir = get_user_config_dir(APP_NAME, APP_AUTHOR)
    assert isinstance(config_dir, text_type)
    assert (config_dir.endswith(APP_NAME) or
            config_dir.endswith(_pathify(APP_NAME)))


def test_sys_config_dirs():
    """Test that the sys config directories are returned correctly."""
    if 'XDG_CONFIG_DIRS' in os.environ:
        del os.environ['XDG_CONFIG_DIRS']
    config_dirs = get_system_config_dirs(APP_NAME, APP_AUTHOR)
    assert isinstance(config_dirs, list)
    assert (config_dirs[0].endswith(APP_NAME) or
            config_dirs[0].endswith(_pathify(APP_NAME)))


@pytest.mark.skipif(not WIN, reason="requires Windows")
def test_windows_user_config_dir_no_roaming():
    """Test that Windows returns the user config directory without roaming."""
    config_dir = get_user_config_dir(APP_NAME, APP_AUTHOR, roaming=False)
    assert isinstance(config_dir, text_type)
    assert config_dir.endswith(APP_NAME)
    assert 'Local' in config_dir


@pytest.mark.skipif(not MAC, reason="requires macOS")
def test_mac_user_config_dir_no_xdg():
    """Test that macOS returns the user config directory without XDG."""
    config_dir = get_user_config_dir(APP_NAME, APP_AUTHOR, force_xdg=False)
    assert isinstance(config_dir, text_type)
    assert config_dir.endswith(APP_NAME)
    assert 'Library' in config_dir


@pytest.mark.skipif(not MAC, reason="requires macOS")
def test_mac_system_config_dirs_no_xdg():
    """Test that macOS returns the system config directories without XDG."""
    config_dirs = get_system_config_dirs(APP_NAME, APP_AUTHOR, force_xdg=False)
    assert isinstance(config_dirs, list)
    assert config_dirs[0].endswith(APP_NAME)
    assert 'Library' in config_dirs[0]


def test_config_reading_raise_errors():
    """Test that instantiating Config will raise errors when appropriate."""
    with pytest.raises(ValueError):
        Config(APP_NAME, APP_AUTHOR, 'test_config', write_default=True)

    with pytest.raises(ValueError):
        Config(APP_NAME, APP_AUTHOR, 'test_config', validate=True)

    with pytest.raises(TypeError):
        Config(APP_NAME, APP_AUTHOR, 'test_config', default=b'test')


def test_config_reading_default_dict():
    """Test that the Config constructor will read in defaults from a dict."""
    default = {'main': {'foo': 'bar'}}
    config = Config(APP_NAME, APP_AUTHOR, 'test_config', default=default)
    assert config.data == default


def test_config_reading_no_default():
    """Test that the Config constructor will work without any defaults."""
    config = Config(APP_NAME, APP_AUTHOR, 'test_config')
    assert config.data == {}


def test_config_reading_default_file():
    """Test that the Config constructor will work with a default file."""
    config = Config(APP_NAME, APP_AUTHOR, 'test_config',
                    default=os.path.join(TEST_DIR, 'configrc'))
    assert config.data == DEFAULT_CONFIG


def test_config_reading_configspec():
    """Test that the Config constructor will work with a configspec."""
    config = Config(APP_NAME, APP_AUTHOR, 'test_config', validate=True,
                    default=os.path.join(TEST_DIR, 'configspecrc'))
    assert config.data == DEFAULT_VALID_CONFIG


def test_config_reading_configspec_with_error():
    """Test that reading an invalid configspec raises and exception."""
    with pytest.raises(ConfigValidationError):
        Config(APP_NAME, APP_AUTHOR, 'test_config', validate=True,
               default=os.path.join(TEST_DIR, 'invalid_configspecrc'))


@with_temp_dir
def test_write_and_read_default_config(temp_dir=None):
    config_file = 'test_config'
    default_file = os.path.join(TEST_DIR, 'configrc')
    temp_config_file = os.path.join(temp_dir, config_file)

    config = _mocked_user_config(temp_dir, APP_NAME, APP_AUTHOR, config_file,
                                 default=default_file)
    config.write_default_config()

    user_config = _mocked_user_config(temp_dir, APP_NAME, APP_AUTHOR,
                                      config_file, default=default_file)
    user_config.read()
    assert temp_config_file in user_config.config_filenames
    assert user_config == config

    with open(temp_config_file) as f:
        contents = f.read()
    assert '# Test file comment' in contents
    assert '# Test section comment' in contents
    assert '# Test field comment' in contents
    assert '# Test field commented out' in contents


@with_temp_dir
def test_write_and_read_default_config_from_configspec(temp_dir=None):
    config_file = 'test_config'
    default_file = os.path.join(TEST_DIR, 'configspecrc')
    temp_config_file = os.path.join(temp_dir, config_file)

    config = _mocked_user_config(temp_dir, APP_NAME, APP_AUTHOR, config_file,
                                 default=default_file, validate=True)
    config.write_default_config()

    user_config = _mocked_user_config(temp_dir, APP_NAME, APP_AUTHOR,
                                      config_file, default=default_file,
                                      validate=True)
    user_config.read()
    assert temp_config_file in user_config.config_filenames
    assert user_config == config

    with open(temp_config_file) as f:
        contents = f.read()
    assert '# Test file comment' in contents
    assert '# Test section comment' in contents
    assert '# Test field comment' in contents
    assert '# Test field commented out' in contents


@with_temp_dir
def test_overwrite_default_config_from_configspec(temp_dir=None):
    config_file = 'test_config'
    default_file = os.path.join(TEST_DIR, 'configspecrc')
    temp_config_file = os.path.join(temp_dir, config_file)

    config = _mocked_user_config(temp_dir, APP_NAME, APP_AUTHOR, config_file,
                                 default=default_file, validate=True)
    config.write_default_config()

    with open(temp_config_file, 'a') as f:
        f.write('--APPEND--')

    config.write_default_config()

    with open(temp_config_file) as f:
        assert '--APPEND--' in f.read()

    config.write_default_config(overwrite=True)

    with open(temp_config_file) as f:
        assert '--APPEND--' not in f.read()
