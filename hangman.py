import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk, Image

import random

from load_images import IMAGE_FILES
from config import *


################################################################################
# Root, frames, global state
################################################################################
root = tk.Tk()
root.title('Hangman')


# frame_init = tk.Frame(root)

frame_word = tk.Frame(root)
frame_word.grid(row=0, column=0, pady=10)

frame_keys = tk.Frame(root)
frame_keys.grid(row=1, column=0, padx=10)

frame_hang = tk.Frame(root)
frame_hang.grid(row=0, column=1, rowspan=2)


gs = {
    'actual_word': [],
    'formed_word': [],
    'label_formed_word': None,

    'image': None,
    'label_image': None,

    'buttons': {},

    'button_play': None,
    'button_quit': None,
    'label_message': None,

    'tries': INITIAL_TRIES
}


################################################################################
# Methods
################################################################################
def write_formed_word():
    """ Write the formed word in frame_word """
    global gs
    if gs['label_formed_word']:
        gs['label_formed_word'].grid_forget()
    gs['label_formed_word'] = tk.Label(frame_word, text=' '.join(gs['formed_word']), font=('TkDefaultFont',WORD_FONT_SIZE))
    gs['label_formed_word'].grid(row=0, column=0, rowspan=3, columnspan=2, pady=10)


def show_final(message):
    """ Show the final message and replay / quit options """
    global gs
    gs['label_message'] = tk.Label(frame_word, text=message, font=('TkDefaultFont',MESSAGE_FONT_SIZE))
    gs['button_play'] = Button(frame_word, text='Play again', command = load_new_word, font=('TkDefaultFont',MESSAGE_FONT_SIZE))
    gs['button_quit'] = Button(frame_word, text='Quit', command = root.quit, font=('TkDefaultFont',MESSAGE_FONT_SIZE))
    gs['label_message'].grid(row=3, column=0, columnspan=2, pady=10)
    gs['button_play'].grid(row=4, column=0, pady=10)
    gs['button_quit'].grid(row=4, column=1, pady=10)


def show_image(t):
    """ Show the hangman image in frame_hang """
    global gs
    gs['image'] = ImageTk.PhotoImage(Image.open(IMAGE_FILES[t]))
    if gs['label_image']:
        gs['label_image'].pack_forget()
    gs['label_image'] = tk.Label(frame_hang, image=gs['image'])
    gs['label_image'].pack(padx=5, pady=5)


def click_button(letter):
    """ What happens on clicking a letter """
    global gs
    
    match = False
    for idx,actual_letter in enumerate(gs['actual_word']):
        if letter == actual_letter:
            match = True
            gs['formed_word'][idx] = letter
    
    write_formed_word()
    gs['buttons'][letter]['state'] = tk.DISABLED
    
    if match:
        gs['buttons'][letter]['background'] = 'green'
        if gs['formed_word'] == gs['actual_word']:
            show_final("\U0001F601 Congratulations, you successfully guessed the word!")
    else:
        gs['buttons'][letter]['background'] = 'red'
        gs['tries'] -= 1
        show_image(gs['tries'])
        if gs['tries'] == 0:
            show_final(f"\U0001F641 No more tries remaining. The word is {''.join(gs['actual_word'])}")


def load_new_word():
    global gs
    
    if gs['label_message']:
        gs['label_message'].grid_forget()
    if gs['button_play']:
        gs['button_play'].grid_forget()
    if gs['button_quit']:
        gs['button_quit'].grid_forget()

    row = 0
    column = 0
    for letter in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        if gs['buttons'].get(letter):
            gs['buttons'][letter].grid_forget() # Doing grid_forget() here is not required since the newly created button should perfectly sit on top of the previously created button, if it existed. However, we do it as a form of defensive coding.
        gs['buttons'][letter] = Button(frame_keys, text=letter, command = (lambda letter = letter: click_button(letter)), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=('TkDefaultFont',BUTTON_FONT_SIZE), disabledforeground='black')
        gs['buttons'][letter].grid(row=row, column=column, columnspan=3)
        column += 3
        if row == 0 and column == 10*3:
            row = 1
            column = 1
        if row == 1 and column == 1+9*3:
            row = 2
            column = 2
    
    gs['tries'] = INITIAL_TRIES
    show_image(gs['tries'])

    while True:
        gs['actual_word'] = random.sample(WORDS,1)[0]
        if len(gs['actual_word']) >= MIN_WORD_SIZE:
            break
    gs['actual_word'] = [*gs['actual_word'].upper()]
    gs['formed_word'] = len(gs['actual_word'])*['_']
    write_formed_word()


################################################################################
# Main
################################################################################
load_new_word()
root.mainloop()
