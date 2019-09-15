from pypylon import pylon
from matplotlib import pyplot as plt


camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

numberOfImagesToGrab = 1
camera.StartGrabbingMax(numberOfImagesToGrab)

camera.GainAuto = 'Off'
camera.ExposureAuto = 'Off'
camera.ExposureTime = 10000
camera.BalanceWhiteAuto = 'Once'

converter = pylon.ImageFormatConverter()
# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_RGB8packed
#converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


print('Starting grabbing')
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        image = converter.Convert(grabResult)
        img = image.GetArray()
        print(img.shape)
        plt.imshow(img)
        plt.show()
        #print("Gray value of first pixel: ", img[0, 0])

    grabResult.Release()
