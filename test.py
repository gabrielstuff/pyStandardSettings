#!/usr/bin/env python
import unittest
import sys, os
from mock import patch

testargs = ['test', '--settings', 'settings/settings.custom.json', '--server.port', '5555']

class TestStandardSettings(unittest.TestCase):

    def test_argv_param_present(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import settings
          self.assertEqual(settings.server.port, 5555)

    def test_argv_deep_merge(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import settings
          self.assertEqual(settings.server.host, 'localhost')

    def test_file_settings_default_json__param_not_overwritten_with_none(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import settings
          self.assertEqual(settings.service.spacebro.host, 'spacebro.space')

    def test_file_settings_json__param_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import settings
          self.assertEqual(settings.defaultUrl, 'http://10.60.60.1/')

    def test_file_settings_custom_json_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import settings
          self.assertEqual(settings.service.spacebro.client.name, 'custom')

    def test_settings_param_loaded(self):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import settings
          self.assertEqual(settings.settings, 'settings/settings.custom.json')
    def test_env(self):
      with patch.dict(os.environ, {'FOLDER_OUTPUT': '/home/'}):
        with patch.object(sys, 'argv', testargs):
          from pyStandardSettings import getSettings
          self.assertEqual(getSettings().folder.output, '/home/')


class TestStandardSettingsNoArgv(unittest.TestCase):

    def test_no_argv(self):
        with patch.object(sys, 'argv', ['test']):
          from pyStandardSettings import getSettings
          self.assertEqual(getSettings().server.port, 6090)


if __name__ == '__main__':
    unittest.main()
