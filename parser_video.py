import zipfile
import shutil
import os
import cv2
import argparse
import json


"""
Basic usage: 
  python3 video_parser.py -i INPUT_DIR -o OUTPUT_DIR
  
  INPUT_DIR is the directory containing video files
  INPUT_DIR can also be a zip file
  OUTPUT_DIR is where RGBD frames and json files are saved
Examples:
* To process first 100 frames only:
    python3 video_parser.py -i INPUT_DIR -o OUTPUT_DIR -n 100
* To flip image:
    python3 video_parser.py -i INPUT_DIR -o OUTPUT_DIR --flip
* To extract every 5th-frame:
    python3 video_parser.py -i INPUT_DIR -o OUTPUT_DIR --skip_frames 5
* To delete original data after processing:
    python3 video_parser.py -i INPUT_DIR -o OUTPUT_DIR --delete_original
    
To view all options:
  python3 video_parser.py -h 
"""


def _unzip(in_zip, out_dir):
    print("Unzipping {} to directory {}".format(in_zip, out_dir))
    if not os.path.exists(out_dir):
        zip_ref = zipfile.ZipFile(in_zip, 'r')
        zip_ref.extractall(out_dir)
        zip_ref.close()
    videos = [os.path.join(out_dir, f) for f in os.listdir(out_dir)
              if f.endswith('.avi')]
    assert len(videos) > 0, "zip file contains no video"
    return videos


def _move(in_dir, out_dir):
    print("Copying {} to {}".format(in_dir, out_dir))
    files = [f for f in os.listdir(in_dir) if not f.endswith('.avi')]
    for n, f in enumerate(files):
        shutil.copy(os.path.join(in_dir, f), out_dir)
        if (n + 1) % 500 == 0:
            print(n + 1, " files copied")
    videos = [os.path.join(in_dir, f) for f in os.listdir(in_dir)
              if f.endswith('.avi')]
    return videos


def _flip(image, video_dir, video_tag, frame):
    image = cv2.flip(image, -1)
    return image


def _parse_video(video, new_dir, extension='avi', skip_frames=None, 
                 flip=False, first_n=None):
    vidcap = cv2.VideoCapture(video, cv2.CAP_FFMPEG)
    while not vidcap.isOpened():
        vidcap = cv2.VideoCapture(video)
        cv2.waitKey(1000)
        print("Wait for the header")
    _, video_base = os.path.split(video)
    video_dir = new_dir
    video_tag, init_frame = video_base.split('_')
    init_frame = int(init_frame.split('.' + extension)[0])
    pos_frame = vidcap.get(cv2.CAP_PROP_POS_FRAMES)
    frame = init_frame
    failure_streak = 0
    while failure_streak < 10:
        success, image = vidcap.read()
        if (not success) or (image is None):
            print("Could not read frame ", frame)
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame+1)
            frame += 1
            failure_streak += 1
            continue
        failure_streak = 0
        pos_frame = vidcap.get(cv2.CAP_PROP_POS_FRAMES)
        if flip:
            image = _flip(image, video_dir, video_tag, frame)
        img_name = video_tag + '_' + str(frame).zfill(7) + '.jpg'
        img_name = os.path.join(video_dir, img_name)
        n = frame - init_frame
        if (n + 1) % 100 == 0:
            print(n + 1, " frames processed")
        if (skip_frames == 0) or (n % skip_frames == 0):
            cv2.imwrite(img_name, image)
        if first_n and (n > first_n):
            break
        frame += 1
        if pos_frame == vidcap.get(cv2.CAP_PROP_FRAME_COUNT):
            print("All frames read")
            break


def run_parser(input_dir, output_dir, extension='avi', skip_frames=0, flip=False, 
               first_n=None, delete_original=False):
    # sub_dirs = [os.path.join(input_dir, sub) for sub in os.listdir(input_dir)]
    # for d in sub_dirs:
    d = input_dir
    new_dir = os.path.join(output_dir, os.path.basename(d))
    videos = []
    if not os.path.exists(new_dir):
        if d.endswith('.zip'):
            new_dir = new_dir.split('.')[0]
            videos = _unzip(d, new_dir)
        else:
            os.makedirs(new_dir)
            videos = _move(d, new_dir)

    for video in videos:
        print("Parsing video : ", video)
        _parse_video(video, new_dir, extension, skip_frames, flip, first_n)
        if delete_original:
            os.remove(video)

    if delete_original:
        if d.endswith('.zip'):
            os.remove(input_dir)
        else:
            shutil.rmtree(input_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', help="directory or zip file containing the raw video files")
    parser.add_argument('-o', '--output_dir', help="directory containing the image frames and labels",
                        default='output')
    parser.add_argument("--extension", help="extension of video files e.g. avi, mp4",
                        default='avi')
    parser.add_argument('-n', '--first_n', help="extract only the first n frames", type=int)
    parser.add_argument("--skip_frames", help="number of frames to skip",
                        type=int, default=0)
    parser.add_argument("--flip", help="this option rotates images by 180 degrees",
                        action="store_true")
    parser.add_argument("--delete_original", help="this option deletes original data",
                        action="store_true")
    args = parser.parse_args()
    input_dir = args.input_dir
    assert input_dir, "Please specify input directory"
    assert os.path.exists(input_dir), "Input directory does not exist"
    out_dir = args.output_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    skip_frames = args.skip_frames
    flip = args.flip
    first_n = args.first_n
    delete_original = args.delete_original
    extension = args.extension
    run_parser(input_dir, out_dir, extension, skip_frames, flip, first_n, delete_original)
