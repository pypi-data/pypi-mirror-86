#!/usr/bin/env python3
# -*- coding: utf-8 -*- Time-stamp: <2020-11-25 23:26:54 sander>*-

# pelmanism: Memory game
# Author: Rolf Sander (2017-2020)
__version__ = '1.1'
# http://www.rolf-sander.net/software/pelmanism

# This program is free software: you can use and distribute it under the
# terms of the GPL v2 or, at your option, any later GPL version:
# http://www.gnu.org/licenses/

##############################################################################

# Tkinter gui:
from tkinter import *
from tkinter.messagebox import *
# other modules:
import datetime
import sys
import random
import os
from glob import glob
from PIL import Image, ImageTk

# ----------------------------------------------------------------------------

class pelmanism:

    Nx = 5 # number of cards in each row
    Ny = 4 # number of cards in each column
    thumbsize = 150 # size of cards in pixels
    windowtitle = 'Pelmanism Memory Game'
    PELMANISMDIR = os.path.dirname(__file__)
    DEBUG = False

    @classmethod
    def show_pic(cls, card, filename):
        img0 = Image.open(filename)
        w = img0.width
        h = img0.height
        fct = min(1,float(cls.thumbsize)/max(w, h)) # scalefactor
        img0 = img0.resize((int(w*fct), int(h*fct)), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img0)
        cls.tpic[card].image = img1
        cls.tpic[card].config(image=img1)

    @classmethod
    def popupwindow(cls):
        popup = Toplevel()
        popup.title(cls.windowtitle)
        label1 = Label(popup, font='-weight bold',
                       text='DONE\nMoves: %2d, Time: %2d:%02d' % (
                           moves, minutes, seconds))
        label1.pack(padx=20, pady=10)
        Button(popup, text='OK, start new game', font='-weight bold',
               command=popup.destroy).pack(pady=10)
        popup.grab_set() # make main window inactive
        cls.gui.wait_window(popup) # pause main window

    @classmethod
    def click_card(cls, i):
        global first, last1, last2, moves, solution
        if (solution[i]<0):
                if (cls.DEBUG): print('already deactivated')
                return
        moves += 1
        if (first):
            # hide previous two cards:
            if (solution[last1]>=0):
                cls.show_pic(last1, cls.PELMANISMDIR+'/bg.png')
            if (solution[last2]>=0):
                cls.show_pic(last2, cls.PELMANISMDIR+'/bg.png')
            last1 = i
            cls.show_pic(i, cls.tfile[i])
        else:
            last2 = i
            if (last1==i):
                if (cls.DEBUG): print('same as last click')
                return
            cls.show_pic(i, cls.tfile[i])
            if (solution[last1]==solution[i]):
                if (cls.DEBUG): print('YES')
                # deactivate cards:
                solution[last1]=-1
                solution[i]=-1
                cls.show_pic(last1, cls.PELMANISMDIR+'/empty.png')
                cls.show_pic(i,     cls.PELMANISMDIR+'/empty.png')
        first = not first
        if (cls.DEBUG): print(solution)
        if (max(solution)<0):
            cls.popupwindow()
            cls.newgame()

    @classmethod
    def newgame(cls):
        global first, last1, last2, moves, solution, starttime
        moves = 0
        first = True
        last1 = 0
        last2 = 0
        solution = list(range(cls.N))
        random.shuffle(solution)
        if (cls.DEBUG): print(solution)
        random.shuffle(cls.allpics)
        if (cls.DEBUG): print(cls.allpics[:cls.N//2])
        for i in range(cls.N):
            # because of integer arithmetics, division by 2 turns
            # 0,1,2,3,4,5,... into 0,0,1,1,2,2,... and we have pairs of
            # cards:
            solution[i] = solution[i]//2
            cls.tfile[i] = cls.allpics[solution[i]]
            cls.show_pic(i, cls.PELMANISMDIR+'/bg.png')
        starttime = datetime.datetime.now()

    @classmethod
    def tick(cls):
        global minutes, seconds
        timenow = datetime.datetime.now()
        deltatime = (timenow-starttime).seconds
        minutes, seconds = divmod(deltatime,60)
        cls.clock.config(text='Moves: %2d, Time: %2d:%02d' % (
            moves, minutes, seconds))
        cls.clock.after(200, cls.tick)

    @classmethod
    def exe(cls):
        cls.gui = Tk()
        cls.gui.title(cls.windowtitle)

        # TODO: check that Nx >= 3
        # TODO: check that N is even
        # TODO: check that len(allpics) >= N//2
        cls.N = cls.Nx * cls.Ny
        cls.tfile = list(range(cls.N))
        cls.tpic  = list(range(cls.N))
        cls.allpics = glob(cls.PELMANISMDIR+'/cards/*.png')
        for i in range(cls.N):
            cls.tpic[i] = Button(height=cls.thumbsize, width=cls.thumbsize,
                             command=lambda i=i: cls.click_card(i))
            cls.tpic[i].grid(padx=5, pady=5, row=i//cls.Nx, column=i%cls.Nx)

        cls.newgame()

        cls.clock = Label(cls.gui, font='-weight bold')
        cls.clock.grid(padx=5, pady=5, row=cls.Ny, column=cls.Nx//2, columnspan=3)
        cls.tick()

        mainloop()

# ----------------------------------------------------------------------------

def main():
    pelmanism.exe()
    
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
