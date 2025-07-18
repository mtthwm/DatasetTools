import argparse
import sys
import os
import cv2
from pathlib import Path

def get_cli_options ():
    parser = argparse.ArgumentParser(
        prog="frame extracter",
    )

    parser.add_argument('-i', '--input')
    parser.add_argument('-s', '--stride', required=False)

    return parser.parse_args(sys.argv[1:])

opts = get_cli_options()


video_path = Path(opts.input)
video_location = video_path.parent
output_folder = video_location.joinpath('frames-' + video_path.name)
os.makedirs(output_folder, exist_ok=True)

stride = 1
if opts.stride:
    stride = int(opts.stride)

cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % stride == 0:
        frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
    frame_count += 1

cap.release()