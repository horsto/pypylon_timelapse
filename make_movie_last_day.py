# Make a timelapse video from the last day

from datetime import datetime,timedelta
from dj_schemas import *
import imageio
from PIL import Image, ImageFont, ImageDraw

similarity_threshold = .93
mse_threshold = 7000
output_basefolder = '/mnt/N/horsto/timelapses'

if __name__ == "__main__":
    print('############ Make movie ############')
    # Collect output from the last day
    restrictor = (timelapse.TimeLapse * timelapse.Similarity & 'ssim < {}'.format(similarity_threshold) & 'mse < {}'.format(mse_threshold)\
                  & 'entry_time_picture > "{}"'.format(datetime.today() - timedelta(days=1)))
    print('Found {} images. Making movie ... '.format(len(restrictor)))
    yesterday = datetime.strftime(datetime.today() - timedelta(days=1),'%d_%m_%Y') # For movie filename

    # Write mp4 file
    with imageio.get_writer('{}/{}.mp4'.format(output_basefolder, yesterday), fps=15) as writer:
        for pic in restrictor:
            img = Image.fromarray(pic['picture']) # Transform into PIL object
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype('Fernando.otf', 115)
            draw.text((50,50),'{}'.format(datetime.strftime(pic['entry_time_picture'],'%d.%m.%Y')),(255,255,255),font=font)
            draw.text((50,150),'{}'.format(datetime.strftime(pic['entry_time_picture'],'%H:%M:%S')),(255,255,255),font=font)
            writer.append_data(np.asarray(img))
    print('Success!')
