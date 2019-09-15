import datajoint as dj
import cv2
from skimage.measure import compare_ssim

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


@schema
class Similarity(dj.Computed):
    definition = """
    # Similarity metrics calculated between adjacent timelapse images
    -> TimeLapse
    ---
    entry_time_picture_prev : datetime # Entry time of previous timelapse entry
    mse                     : float    # Mean squared error
    ssim                    : float    # Structural similarity
    """
    def mse(self, imageA, imageB):
        ''' https://www.pyimagesearch.com/2014/09/15/python-compare-two-images '''
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    def make(self, key):
        timelapse_entry = (TimeLapse & key).fetch1()

        last_pic_entry = (TimeLapse & 'entry_time_picture < "{}"'.format(timelapse_entry['entry_time_picture']))\
                     .fetch(order_by='entry_time_picture DESC', limit=1, as_dict=True)[0]
        key['entry_time_picture_prev'] = last_pic_entry['entry_time_picture']
        picture = cv2.cvtColor(timelapse_entry['picture'], cv2.COLOR_BGR2GRAY)
        picture_prev = cv2.cvtColor(last_pic_entry['picture'], cv2.COLOR_BGR2GRAY)

        key['mse']  = self.mse(picture,picture_prev)
        key['ssim'] = compare_ssim(picture,picture_prev)
        self.insert1(key)

