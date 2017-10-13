#!/usr/bin/python -W ignore::Warning
# coding=utf8

################################################################################
# x264_encode.py
# A simple script to encode Video to h264/mp3/mkv
#
# Required:
# python3
# media-video/mkvtoolnix
# media-video/mplayer
# media-libs/x264
# dev-python/pexpect

import os
import sys
import getopt
import pexpect


# Colors
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
NORMAL  = "\033[0m"
BOLD    = "\033[1m"


def get_videos_from_file(src_file):

    src_videos = [line.strip() for line in open(src_file, "r") if line.strip() != ""]
    return src_videos


def make_output_file_name(src_file, output_path, extension):

    if "/" in src_file: src_file = src_file.rsplit("/",1)[1]
    if "." in src_file: src_file = src_file.rsplit(".",1)[0]
    output_file = output_path + src_file + extension
    return output_file


def print_ticks(event):

    line = event["child_result_list"].pop().decode("utf-8").strip().rsplit("\r",1)[1]
    print(CYAN + line + NORMAL, end="\r")


def main():

    # Check if arguments are available.
    if len(sys.argv[1:]) == 0:
        print()
        print(RED + "No arguments given. Exiting..." + NORMAL)
        usage()
        sys.exit(1)

    # Find the base directory.
    base = sys.argv[0]
    base_dir = base[0:base.rfind("/") + 1]

    # Settings
    video_bitrate = 5000
    video_scaling = "" # e.g. 1248:702 or empty
    audio_bitrate = 192
    audio_language = "eng"
    output_path = base_dir + "encoded/"

    # Check if output path exists, if not, create it.
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # Arguments
    try:
        options, src_videos = getopt.getopt(sys.argv[1:], "v:s:f:l:")
    except getopt.GetoptError as e:
        print()
        print(RED + "Parameter error. Exiting..." + NORMAL)
        print(RED + str(e) + NORMAL)
        usage()
        sys.exit(1)

    for o, a in options:
        if o in "-v": video_bitrate = a
        if o in "-s": video_scaling = a
        if o in "-l": audio_language = a
        if o in "-f": src_videos = get_videos_from_file(a)

    # Build the command string.
    for src_file in src_videos:
        command = "mencoder "
        command += src_file + " "
        command += "-ovc x264 -x264encopts bitrate=" + str(video_bitrate) + " "
        if video_scaling: command += "-vf scale=" + video_scaling + " "
        command += "-alang " + audio_language + " "
        command += "-oac mp3lame -lameopts abr:br=" + str(audio_bitrate) + " "
        command += "-af volnorm=1 "
        mencoder_output_file = make_output_file_name(src_file, output_path, ".avi")
        command += "-o " + mencoder_output_file

        print(command)

        # Encode the video
        print(BLUE + "Encoding file "+ YELLOW + src_file + NORMAL)
        (out, mencoder_exit) = pexpect.run(command, events={pexpect.TIMEOUT:print_ticks}, timeout=3, withexitstatus=1)
        print()

        # Build the mkv command string.
        mkv_command = "mkvmerge "
        mkv_command += mencoder_output_file + " "
        mkv_command += " -o " + make_output_file_name(mencoder_output_file, output_path, ".mkv")

        # Convert to mkv
        print(BLUE + "Converting file "+ YELLOW + mencoder_output_file + NORMAL)
        (out, mkv_exit) = pexpect.run(mkv_command, events={pexpect.TIMEOUT:print_ticks}, timeout=1, withexitstatus=1)
        print()

        # Remove mencoder temporary video file aka. mencoder_output_file.
        print(BLUE + "Cleaning up..." + NORMAL)
        try:
            os.remove(mencoder_output_file)
        except OSError as e:
            print(RED + str(e) + NORMAL)
        except IOError as e:
            print(RED + str(e) + NORMAL)

        # Finished.
        if mencoder_exit !=0 or mkv_exit !=0:
            print(RED + "Something went wrong." + NORMAL)
            print(RED + "Finished with exit codes: " + str(mencoder_exit) + " and " + str(mkv_exit))
        else:
            print(GREEN + "Finished with clean exit codes." + NORMAL)


def usage():

    print(GREEN)
    print("Usage:")
    print("./x264_encode.py [options] <file> : Encode <file> with options.")
    print("./x264_encode.py -f <file> : Encode files defined in <file>")
    print()
    print("Options:")
    print("-v <value> : Videobitrate will be set to <value>. Default 5000.")
    print("-s X:Y : Scale video to X:Y.")
    print("-l <language> : Sets language to <language>. Use like ger or eng here.")
    print(NORMAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(RED + "Exiting..." + NORMAL)
