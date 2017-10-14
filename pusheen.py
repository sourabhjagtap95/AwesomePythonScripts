#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Pusheen
Script that mimics `sl` but with pusheen instead of a train.
"""

from time import sleep
from math import floor
import curses


FRAME_TIME = 0.04

# KEY FRAMES
PUSHEEN = """   ▐▀▄       ▄▀▌   ▄▄▄▄▄▄▄
   ▌  ▀▄▄▄▄▄▀  ▐▄▀▀ ██ ██ ▀▀▄
  ▐    ▀ ▀ ▀                 ▀▄
  ▌               ▄            ▀▄
▀█   █   █   █   ▀               ▌
▀▌      ▀ ▀      ▀▀              ▐   ▄▄
▐                                 ▌▄█ █
▐                                 █ █▀
▐                                 █▀
▐                                 ▌
 ▌                               ▐
 ▐                               ▌
  ▌                             ▐
  ▐▄                           ▄▌
""".splitlines()

PUSHEEN_FEET = """   ▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀
    ▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀
    ▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀
    ▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀
    ▀▄▄▀▀▀▀▀▄▄▀▀▀▀▀▀▀▄▄▀▀▀▀▀▄▄▀
    ▀▄▄▀▀▀▀▀▄▄▀▀▀▀▀▀▀▄▄▀▀▀▀▀▄▄▀
    ▀▄▄▀▀▀▀▀▄▄▀▀▀▀▀▀▀▄▄▀▀▀▀▀▄▄▀
    ▀▄▄▀▀▀▀▀▄▄▀▀▀▀▀▀▀▄▄▀▀▀▀▀▄▄▀
    ▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀
    ▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀
    ▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀
    ▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀▀▀▀▀▀▀▀
""".splitlines()



def main(win):
    #invisible cursor
    curses.curs_set(0)
    # get size of terminal
    MAX_Y, MAX_X = win.getmaxyx()
    CENTER = floor(MAX_Y / 2) - floor((len(PUSHEEN) + 1) / 2) - 1

    feet_frame = 0

    # fade in from right
    for x in range(MAX_X):
        win.erase()

        # draw body
        for y, line in enumerate(PUSHEEN):
            win.addstr(CENTER + y, MAX_X-(x+1), line[:x])

        # draw feet
        if feet_frame == len(PUSHEEN_FEET):
            feet_frame = 0
        win.addstr(CENTER + len(PUSHEEN), MAX_X-(x+1), PUSHEEN_FEET[feet_frame][:x])
        feet_frame += 1

        win.refresh()
        sleep(FRAME_TIME)

    # fade out left
    # range is based on the length of the longest string
    for x in range(len(max(PUSHEEN, key=len))):
        win.erase()

        # draw body
        for y, line in enumerate(PUSHEEN):
            win.addstr(CENTER + y, 0, line[x:])

        # draw feet
        if feet_frame == len(PUSHEEN_FEET):
            feet_frame = 0
        win.addstr(CENTER + len(PUSHEEN), 0, PUSHEEN_FEET[feet_frame][x:])
        feet_frame += 1

        win.refresh()
        sleep(FRAME_TIME)


if __name__ == '__main__':
    curses.wrapper(main)
