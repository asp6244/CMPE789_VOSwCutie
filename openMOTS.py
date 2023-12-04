# New file by asp6244

import os
import numpy as np
import cv2
from pycocotools.mask import decode

files = ["MOTS20-02", "MOTS20-05", "MOTS20-09", "MOTS20-11"]
train_dir = "../MOTS/train"

def save_frame(list_of_RLE_dicts, list_of_tracks, track_colors, past_frame_num, fname):
	# New frame, save the past one
	mask_data = decode(list_of_RLE_dicts)

	# Create an index for the list of colors
	mask_data = mask_data*[i+1 for i in range(len(list_of_tracks)-1)]
	mask_data = np.max(mask_data, axis=2)

	# Get colors for each pixel
	mask_colors = [track_colors[track] for track in list_of_tracks]
	mask = np.array([[mask_colors[class_idx] for class_idx in row] for row in mask_data], dtype=np.uint8)

	if np.max(mask_data) == 0:
		print("No objects in frame " + str(past_frame_num))

	# Save mask
	if past_frame_num % 10 == 0:
		print("Saving image " + os.path.join(fname, str(past_frame_num).zfill(6) + ".png"))
	cv2.imwrite(os.path.join(train_dir, "Annotations", fname, str(past_frame_num).zfill(6) + ".png"), mask)

	past_frame_num = frame_num

for fname in files:
	list_of_RLE_dicts = []
	list_of_tracks = [0]
	track_colors = {0: [0, 0, 0]}
	past_frame_num = 1
	with open(os.path.join(train_dir, fname + "_gt.txt"), mode='r') as file:
		for line in file:
			# Split the line into values
			values = line.strip().split(' ')

			frame_num = int(values[0])
			track_id = int(values[1])

			if frame_num != past_frame_num:
				save_frame(list_of_RLE_dicts, list_of_tracks, track_colors, past_frame_num, fname)
				list_of_RLE_dicts = []
				list_of_tracks = [0]


			if track_id != 10000:
				list_of_tracks.append(track_id)

				if track_id not in track_colors:
					# New random color
					track_colors[track_id] = [np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)]

				RLE_dict = {'size': [int(values[3]), int(values[4])], \
							'counts': values[5]}
				list_of_RLE_dicts.append(RLE_dict)
		
		save_frame(list_of_RLE_dicts, list_of_tracks, track_colors, past_frame_num, fname)
