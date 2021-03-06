#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

import timeit

from time import sleep

import pickle

from head import *
from Game import *
from minimax import *
from MENACE import *



configurations = load_menace()
game = Game()
root = tk.Tk()
font = tkFont.Font(size=60)

buttons = [
    [],
    [],
    []
]


def disableButtons():
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            buttons[i][j].config(state='disabled')
            buttons[i][j].pack()
    root.update()

def enableButtons():
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            buttons[i][j].config(state='active')
            buttons[i][j].pack()
    root.update()

def buttonUpdate(i, j):
    text = game.get_board(i, j).upper()
    buttons[i][j].config(text=text)
    buttons[i][j].pack()
    root.update()

def win():
    disableButtons()
    messagebox.showinfo("Game Over", "Le joueur %s a gagné !" %(game.winner().upper()))

def NoWinner():
    disableButtons()
    messagebox.showinfo("Game Over", "égalité")

def iaMove():
    if CURRENT_AI == "menace":
        i, j = ai_menace_play(game.get_board(),historic,configurations)
    else :
        i, j, v = aiPlay(game.get_board())


    game.move(i, j)
    buttonUpdate(i, j)

def winUpdate():
    if game.is_there_winner():
        win()
        return True
    elif game.no_winner():
        NoWinner()
        return True
    return False

def buttonPress(i, j):
    if game.move(i, j):
        buttonUpdate(i, j)
    
    if not winUpdate():
        disableButtons()
        iaMove()
        enableButtons()
        winUpdate()
    elif CURRENT_AI == "menace" :
        if game.no_winner():
            ai_reward(1,historic,configurations)
        else:
            if game.winner() == COMPUTER:
                ai_reward(2,historic,configurations)
            else:
                ai_reward(-1,historic,configurations)

def autoTraining():
    global CURRENT_AI
    if not winUpdate():
        iaMove()
        winUpdate()
        root.after(500, autoTraining)
        if CURRENT_AI == "menace":
            CURRENT_AI = "minmax"
        else:
            CURRENT_AI = "menace"
    if game.no_winner():
        ai_reward(1,historic,configurations)
    else:
        if game.winner() == COMPUTER:
            ai_reward(2,historic,configurations)
        else:
            ai_reward(-1,historic,configurations)


    

def initBoard():
    for i in range(3):
        for j in range(3):
            frame = tk.Frame(
                master=root,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j, padx=5, pady=5)

            buttons[i].append(
                tk.Button(
                    master=frame,
                    font=font,
                    text=game.get_board(i, j).upper(),
                    command=lambda locI=i, locJ=j: buttonPress(locI, locJ),
                    width=3,
                    state='normal'
                )
            )
            buttons[i][j].pack(expand=1)

if __name__ == "__main__":
    initBoard()
    root.after(500, autoTraining)
    root.mainloop()
