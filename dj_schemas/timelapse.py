import datajoint as dj
schema = dj.schema(dj.config['dj_timelapse.database'])

import numpy as np
np.warnings.filterwarnings('ignore')

@schema
class Settings(dj.Lookup):
    definition = """
    # Timelapse camera settings (Only one allowed for now!)
    settings_id                    : char(1)          # Parameter set ID, starting with A
    ---
    no_images                      : int              # How many images should be recorded per one loop?
    time_between_images            : int              # Time between images in seconds
    camera_gain_auto               : enum('Off', 'On')
    camera_exposure_auto           : enum('Off','On')
    camera_exposure_time           : int              # Exposure time in microseconds
    camera_balance_white_auto      : varchar(12)
    start_hour_morning             : smallint         # Hour number in the morning when timelapse should start (24h format)
    stop_hour_evening              : smallint         # Hour number in the evening when timelapse should stop (24h format)
    """
    contents = [
          ['A', 3, 15, 'Off', 'Off', 40000, 'Once', 9, 22]
               ]


@schema
class TimeLapse(dj.Manual):
    definition = """
    # Base table for timelapse images
    entry_time_picture   = CURRENT_TIMESTAMP : timestamp           # Auto created timestamp
    ---
    mean_r          :  float
    mean_g          :  float
    mean_b          :  float
    picture = NULL  :  blob@timelapsestore
    """
