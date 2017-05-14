# -*- coding: utf-8 -*-
"""Test the cli_helpers.config module."""

import os
import sys

import pytest

from cli_helpers.compat import text_type, WIN
from cli_helpers.config import (get_system_config_dirs, get_user_config_dir,
                                _pathify)


def test_user_config_dir():
    """Test that the config directory is a string with the app name in it."""
    if 'XDG_CONFIG_HOME' in os.environ:
        del os.environ['XDG_CONFIG_HOME']
    app_name, app_author = 'Test', 'Acme'
    config_dir = get_user_config_dir(app_name, app_author)
    assert isinstance(config_dir, text_type)
    assert (config_dir.endswith(app_name) or
            config_dir.endswith(_pathify(app_name)))


def test_sys_config_dirs():
    """Test that the sys config directories are returned correctly."""
    if 'XDG_CONFIG_DIRS' in os.environ:
        del os.environ['XDG_CONFIG_DIRS']
    app_name, app_author = 'Test', 'Acme'
    config_dirs = get_system_config_dirs(app_name, app_author)
    assert isinstance(config_dirs, list)
    assert (config_dirs[0].endswith(app_name) or
            config_dirs[0].endswith(_pathify(app_name)))


@pytest.mark.skipif(not WIN, reason="requires Windows")
def test_windows_user_config_dir_no_roaming():
    """Test that Windows returns the user config directory without roaming."""
    app_name, app_author = 'Test', 'Acme'
    config_dir = get_user_config_dir(app_name, app_author, roaming=False)
    assert isinstance(config_dir, text_type)
    assert config_dir.endswith(app_name)
    assert 'Local' in config_dir


@pytest.mark.skipif(sys.platform != 'darwin', reason="requires macOS")
def test_mac_user_config_dir_no_xdg():
    """Test that macOS returns the user config directory without XDG."""
    app_name, app_author = 'Test', 'Acme'
    config_dir = get_user_config_dir(app_name, app_author, force_xdg=False)
    assert isinstance(config_dir, text_type)
    assert config_dir.endswith(app_name)
    assert 'Library' in config_dir


@pytest.mark.skipif(sys.platform != 'darwin', reason="requires macOS")
def test_mac_system_config_dirs_no_xdg():
    """Test that macOS returns the system config directories without XDG."""
    app_name, app_author = 'Test', 'Acme'
    config_dirs = get_system_config_dirs(app_name, app_author, force_xdg=False)
    assert isinstance(config_dirs, list)
    assert config_dirs[0].endswith(app_name)
    assert 'Library' in config_dirs[0]
