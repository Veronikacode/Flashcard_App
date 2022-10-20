from tkinter import *
import pandas
import random

to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/polish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="Polish", fill="black")
    canvas.itemconfig(word_text, text=current_card["Polish"], fill="black")
    canvas.itemconfig(card_background, image=flashcard_front)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=flashcard_secondback)

def is_known():
    to_learn.remove(current_card)
    learn = pandas.DataFrame(to_learn)
    learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard_back = PhotoImage(file="images/card_back.png")
flashcard_front = PhotoImage(file="images/card_front.png")
flashcard_secondback = PhotoImage(file="images/card_back.png")
canvas.create_image(400, 263, image=flashcard_back)
card_background = canvas.create_image(400, 263, image=flashcard_front)
canvas.grid(column=0, row=0, columnspan=2)

title_text = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")

red_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
red_button.grid(column=0, row=1)

green_button= Button(image= right_image, highlightthickness=0, command=is_known)
green_button.grid(column=1, row=1)

next_card()

window.mainloop()