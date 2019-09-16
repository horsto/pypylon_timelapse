import sys
from pypylon import pylon
#from matplotlib import pyplot as plt
import time
from datetime import datetime
from dj_schemas import *

# Retrieve settings
settings = Settings.fetch1() # Only one setting allowed!

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_RGB8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

now = datetime.now()
if (now.hour < settings['start_hour_morning']) or (now.hour >= settings['stop_hour_evening']):
      print('Time outside the set range')
      sys.exit()

print('{} Starting grabbing'.format(now))

numberOfImagesToGrab = settings['no_images']

for image_no in range(numberOfImagesToGrab):
    camera.StartGrabbingMax(1)
    camera.GainAuto = settings['camera_gain_auto']
    camera.ExposureTime = settings['camera_exposure_time']
    camera.ExposureAuto = settings['camera_exposure_auto'] # Might reset that setting
    camera.BalanceWhiteAuto = settings['camera_balance_white_auto']
    camera.ReverseY = 'true'
    camera.ReverseX = 'true'

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            print('Processing picture {}/{}'.format(image_no+1,numberOfImagesToGrab))
            # Access the image data.
            image = converter.Convert(grabResult)
            img = image.GetArray()

            # Write to Datajoint
            TimeLapse.insert1({
                        'picture':  img,
                        'mean_r' :  np.mean(img[:, :, 0]),
                        'mean_g' :  np.mean(img[:, :, 1]),
                        'mean_b' :  np.mean(img[:, :, 2])
                        })
            #print(img.shape)
        grabResult.Release()
    if image_no < numberOfImagesToGrab-1:
        time.sleep(settings['time_between_images'])
