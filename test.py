#!/usr/bin/env python
from pyStandardSettings import settings

print('server port', settings.server.port)
print('server host', settings.server.host)
print('spacebro name', settings['service']['spacebro']['client']['name'])
print('spacebro host', settings['service']['spacebro']['host'])
print('settings file', settings.settings)
