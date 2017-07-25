#!/usr/bin/env python
import unittest
import sys, os
from os import path
from mock import patch

testargs = ['test', '--settings', 'settings/settings.custom.json', '--server.port', '5555']

class TestStandardSettingsArgv(unittest.TestCase):

    def test_argv_param_present(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.server.port, 5555)

    def test_argv_deep_merge_dont_overwrite_with_none(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.server.host, 'localhost')

    def test_settings_param_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.settings, 'settings/settings.custom.json')

class TestStandardSettingsNoArgv(unittest.TestCase):

    def test_no_argv(self):
        with patch.object(sys, 'argv', ['test']):
          from pyStandardSettings.pyStandardSettings import getSettings
          self.assertEqual(getSettings().server.port, 6090)


class TestStandardSettingsFiles(unittest.TestCase):
    def test_file_default_settings_json__param_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.server.host, 'localhost')

    def test_file_default_settings_json__found_from_cwd(self):
        with patch('os.getcwd', return_value=(path.dirname(sys.modules['__main__'].__file__))):
          with patch.object(sys.modules['__main__'], '__file__', path.abspath(path.join(os.getcwd(), '../', 'test.py'))):
            with patch.object(sys, 'argv', testargs):
              from pyStandardSettings.pyStandardSettings import getSettings
              self.assertEqual(getSettings().server.host, 'localhost')

    def test_file_settings_default_json__param_not_overwritten_with_none(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.service.spacebro.host, 'spacebro.space')

    def test_file_settings_json__param_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.defaultUrl, 'http://10.60.60.1/')

    def test_file_settings_custom_json_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import settings
          self.assertEqual(settings.service.spacebro.client.name, 'custom')

    def test_file_settings_custom_json_loaded_from_cwd(self):
        with patch.object(sys, 'argv', ['test', '--settings', 'tests/settings/settings.custom.json']):
          from pyStandardSettings.pyStandardSettings import getSettings
          self.assertEqual(getSettings().service.spacebro.client.name, 'custom')

    def test_file_settings_custom_json_loaded_abs_path(self):
        with patch.object(sys, 'argv', ['test', '--settings', path.abspath(path.join(os.getcwd(), 'tests/settings/settings.custom.json'))]):
          from pyStandardSettings.pyStandardSettings import getSettings
          self.assertEqual(getSettings().service.spacebro.client.name, 'custom')

class TestStandardSettingsEnv(unittest.TestCase):

    def test_env(self):
      with patch.dict(os.environ, {'FOLDER_OUTPUT': '/home/'}):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import getSettings
          self.assertEqual(getSettings().folder.output, '/home/')

    def test_env_with_dont_override_type(self):
      with patch.dict(os.environ, {'NOTOBJECT': 'myvalue', 'NOTOBJECT_IS_OBJECT': 'no'}):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import getSettings
          self.assertEqual(getSettings().notobject, 'myvalue')

    def test_env_with_dont_override_type_both_order(self):
      with patch.dict(os.environ, {'NOTOBJECT_IS_OBJECT': 'no', 'NOTOBJECT': 'myvalue'}):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings.pyStandardSettings import getSettings
          self.assertEqual(getSettings().notobject, 'myvalue')

if __name__ == '__main__':
    unittest.main()
