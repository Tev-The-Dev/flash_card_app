from tkinter import *
import pandas
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
try:
    with open("data/words_to_learn.csv", "r") as file:
        data = pandas.read_csv(file)
except FileNotFoundError:
    data=pandas.read_csv("data/japanese.csv")
data_dict = data.to_dict(orient="records")
random_row = random.choice(data_dict)  # Select ONE row at random
pandas.DataFrame(data_dict).to_csv("data/words_to_learn.csv",index=False)

def get_random_kanji():
    global random_row, timer_id, wrong_button
    window.after_cancel(timer_id)
    random_row = random.choice(data_dict)
    kanji = random_row["Kanji"]
    onyomi = random_row["Onyomi"]
    canvas.itemconfig(card_title, text="Japanese")
    canvas.itemconfig(canvas_id, image=card_front)
    canvas.itemconfig(card_title, fill="black")
    canvas.itemconfig(word_id, fill="black")
    # Check if Kanji is empty or NaN
    if pandas.isna(kanji) or kanji.strip() == "":
        canvas.itemconfig(word_id, text=f"{onyomi}")  # Display Onyomi only
    else:
        canvas.itemconfig(word_id, text=f"{kanji}\n{onyomi}")  # Display both together
    timer_id = window.after(3000, show_english)



def show_english():
    global random_row, timer_id
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(word_id, text=random_row["English"])
    canvas.itemconfig(word_id, font=("Arial", 40, "bold"))
    canvas.itemconfig(canvas_id, image=card_back)
    canvas.itemconfig(card_title,fill="white")
    canvas.itemconfig(word_id, fill="white")

def study_word():
    get_random_kanji()



def known_word():
    global random_row, data_dict
    if random_row in data_dict:
        data_dict.remove(random_row)
    pandas.DataFrame(data_dict).to_csv("data/words_to_learn.csv",index=False)
    get_random_kanji()


window = Tk()
window.title("Flash Cards App")

window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
timer_id = window.after(3000, func=show_english)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
canvas_id = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400,150, text="", font=("Arial", 40, "italic"))
word_id = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
get_random_kanji()
canvas.grid(column=0, row=0, columnspan=2)

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=study_word)
wrong_button.grid(column=0, row=1)
wrong_button.grid(row=1, column=0)


right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)



card_back = PhotoImage(file="images/card_back.png")

window.mainloop()