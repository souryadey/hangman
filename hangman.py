import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk, Image
import os
import random
from english_words import english_words_lower_alpha_set as words


################################################################################
# Create root
################################################################################
root = tk.Tk()
root.title('Hangman')
################################################################################


################################################################################
# Define constants
################################################################################
INITIAL_TRIES = 6

words = list(words)
MIN_WORD_SIZE = 5
WORD_FONT = tk.font.Font(size=40)

BUTTON_WIDTH = 60
BUTTON_HEIGHT = 60
BUTTON_FONT = tk.font.Font(size=20)

MESSAGE_FONT = tk.font.Font(size=20)
################################################################################


################################################################################
# Create frames and globals
################################################################################
frame_word = tk.Frame(root)
frame_word.grid(row=0, column=0, pady=10)

frame_keys = tk.Frame(root)
frame_keys.grid(row=1, column=0, padx=10)

frame_hang = tk.Frame(root)
frame_hang.grid(row=0, column=1, rowspan=2)

actual_word = ''
formed_word = ''
label_formed_word = None

image = None
label_image = None

buttons = {}

button_play = None
button_quit = None
label_message = None

tries = INITIAL_TRIES
################################################################################


################################################################################
# Load hangman images
################################################################################
image_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
image_files = [f for f in os.listdir(image_directory) if f.startswith('h') and f.endswith('.png')]
image_files.sort(key = lambda f: int(os.path.splitext(f)[0][1:]))
image_files = [os.path.join(image_directory,f) for f in image_files]
################################################################################


################################################################################
# Methods
################################################################################
def write_formed_word():
    """ Write the formed word in frame_word """
    global formed_word, label_formed_word
    if label_formed_word:
        label_formed_word.grid_forget()
    label_formed_word = tk.Label(frame_word, text=' '.join(formed_word), font=WORD_FONT)
    label_formed_word.grid(row=0, column=0, rowspan=3, columnspan=2, pady=10)

def show_final(message):
    """ Show the final message and replay / quit options """
    global label_message, button_play, button_quit
    label_message = tk.Label(frame_word, text=message, font=MESSAGE_FONT)
    button_play = Button(frame_word, text='Play again', command = load_new_word, font=MESSAGE_FONT)
    button_quit = Button(frame_word, text='Quit', command = root.quit, font=MESSAGE_FONT)
    label_message.grid(row=3, column=0, columnspan=2, pady=10)
    button_play.grid(row=4, column=0, pady=10)
    button_quit.grid(row=4, column=1, pady=10)

def show_image(tries):
    """ Show the hangman image in frame_hang """
    global image, label_image
    image = ImageTk.PhotoImage(Image.open(image_files[tries]))
    if label_image:
        label_image.pack_forget()
    label_image = tk.Label(frame_hang, image=image)
    label_image.pack(padx=5, pady=5)


def click_button(letter):
    """ What happens on clicking a letter """
    global actual_word, formed_word, buttons, tries
    
    match = False
    for idx,actual_letter in enumerate(actual_word):
        if letter == actual_letter:
            match = True
            formed_word[idx] = letter
    
    write_formed_word()
    buttons[letter]['state'] = tk.DISABLED
    
    if match:
        buttons[letter]['background'] = 'green'
        if formed_word == actual_word:
            show_final('\U0001F601 Congratulations, you successfully guessed the word!')
    else:
        buttons[letter]['background'] = 'red'
        tries -= 1
        show_image(tries)
        if tries == 0:
            show_final(f'\U0001F641 No more tries remaining. The word is {"".join(actual_word)}')


def load_new_word():
    global actual_word, formed_word, buttons, label_message, button_play, button_quit, tries
    
    if label_message:
        label_message.grid_forget()
    if button_play:
        button_play.grid_forget()
    if button_quit:
        button_quit.grid_forget()

    row = 0
    column = 0
    for letter in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        buttons[letter] = Button(frame_keys, text=letter, command = (lambda letter = letter: click_button(letter)), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=BUTTON_FONT, disabledforeground='black')
        buttons[letter].grid(row=row, column=column, columnspan=3)
        column += 3
        if row == 0 and column == 10*3:
            row = 1
            column = 1
        if row == 1 and column == 1+9*3:
            row = 2
            column = 2
    
    tries = INITIAL_TRIES
    show_image(tries)

    while True:
        actual_word = random.sample(words,1)[0]
        if len(actual_word) >= MIN_WORD_SIZE:
            break
    actual_word = [*actual_word.upper()]
    formed_word = len(actual_word)*['_']
    write_formed_word()
################################################################################


load_new_word()

root.mainloop()
