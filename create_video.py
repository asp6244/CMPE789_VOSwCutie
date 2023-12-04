# New file by asp6244

import os
import cv2
import numpy as np
from PIL import Image

output_dir = "output/default/generic/Annotations/"

img_dir_name = "../test_data/JPEGImages/runner"
img_names_img = np.sort(os.listdir(img_dir_name))
img_out_path = os.path.join(output_dir, "runner.mp4")

mask_dir_name = "output/default/generic/Annotations/runner"
mask_names_img = np.sort(os.listdir(img_dir_name))
mask_out_path = os.path.join(output_dir, "runner_mask.mp4")

img0 = cv2.imread(os.path.join(img_dir_name, img_names_img[0]))
width = img0.shape[1]
height = img0.shape[0]

img_out = cv2.VideoWriter(img_out_path ,cv2.VideoWriter_fourcc(*'MJPG'), 30, (width, height))
mask_out = cv2.VideoWriter(mask_out_path ,cv2.VideoWriter_fourcc(*'MJPG'), 30, (width, height))

for img_name in img_names_img:
    img = cv2.imread(os.path.join(img_dir_name, img_name))

    mask = cv2.imread(os.path.join(mask_dir_name, img_name[:-4] + ".png"))
    # Split the image into its RGB channels
    b, g, r = cv2.split(mask)
    # Set green and red channels to zero
    zeros = np.zeros_like(b)
    blue_channel_only = cv2.merge([b, zeros, zeros])

    blended_image = cv2.addWeighted(img, 1.0, blue_channel_only, 0.8, 0)

    img_out.write(blended_image)
    mask_out.write(mask)

    i = int(img_name[:-4])
    if i % 100 == 0:
        print("Saving frame " + str(i))

img_out.release()
mask_out.release()
print("Done saving to " + img_out_path)
print("Done saving to " + mask_out_path)