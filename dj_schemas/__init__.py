# Initialize database connection
import os, sys
import datajoint as dj
import configparser
from datetime import datetime

config = configparser.ConfigParser()
authcfg = os.path.join(os.path.dirname(__file__), '..', 'auth.cfg')
config.read(authcfg)

#### CONNECTION #############################################

dj_ip = config['dj_auth']['ip']
dj_user = config['dj_auth']['user']
dj_pass = config['dj_auth']['password']

dj.config['database.host'] = dj_ip
dj.config['database.user'] = dj_user
dj.config['database.password'] = dj_pass

#### DATABASES ##############################################
db_prefix = ''
dj.config['dj_timelapse.database'] = db_prefix + 'group_imaging_timelapse1'

#### DRIVES #################################################
# Load drives connected to this computer
config = configparser.ConfigParser()
drivecfg = os.path.join(os.path.dirname(__file__), '..', 'network_drives.cfg')

config.read(drivecfg)
#print('drivconfig', dir(config))

dj.config['drives'] = config['network_drives']
dj.config['stores'] = {
    'timelapsestore': {
        'protocol': 'file',
        # 'location': dj.config['drives']['Datajoint']
        'location': os.path.join(dj.config['drives']['Datajoint'], 'timelapsestore')
    }}
dj.config['safemode'] = False


from .timelapse import *
