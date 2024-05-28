from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


# ----------File handling-----#
def read_from_file():
    try:
        data_frame = pandas.read_csv("./data/words_to_use.csv")
        words = data_frame.to_dict(orient="records")

    except FileNotFoundError:
        data_frame = pandas.read_csv("./data/french_words.csv")
        words = data_frame.to_dict(orient="records")

    return words


# ------------change word------#
def change_word(should_remove):
    if should_remove:
        to_remove = flash_card.itemcget(dynamic_word, "text")
        remove_from_list(to_remove)
    list_of_words2 = read_from_file()
    choice = random.randint(0, 101)
    flash_card.itemconfig(photo, image=card_front)
    flash_card.itemconfig(title, text="french", fill="black")
    flash_card.itemconfig(dynamic_word, text=list_of_words2[choice]['French'])
    screen.after(ms=3000, func=lambda: translation(list_of_words2, choice))


# ----Translate word---------#
def translation(list_of_words2, choice):
    flash_card.itemconfig(photo, image=card_back)
    flash_card.itemconfig(title, text="English", fill="white")
    flash_card.itemconfig(dynamic_word, text=list_of_words2[choice]['English'])


def remove_from_list(to_delete):
    new_list_of_words = read_from_file()
    for items in new_list_of_words:
        if items['English'] == to_delete:
            new_list_of_words.remove(items)
    new_df = pandas.DataFrame(new_list_of_words)
    new_df.to_csv("./data/words_to_use.csv",index=False)


# -----------GUI--------------#
screen = Tk()
screen.title("Flashy")
screen.config(padx=50, pady=50)
screen.minsize(width=900, height=700)
screen.config(bg=BACKGROUND_COLOR)
flash_card = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
photo = flash_card.create_image(400, 270, image=card_front)
flash_card.grid(row=0, column=0, columnspan=3)
title = flash_card.create_text(400, 150, fill="black", font=('Ariel', 40, 'italic'), text="french")
list_of_words = read_from_file()
dynamic_word = flash_card.create_text(400, 263, fill="black", font=('Ariel', 60, 'bold'),
                                      text="press any button to start..")  # might have to change
tick_button_image = PhotoImage(file="./images/right.png")
tick_button = Button(image=tick_button_image, highlightthickness=0)
tick_button.grid(row=1, column=0)
tick_button.config(command=lambda: change_word(should_remove=True))
cross_button_image = PhotoImage(file="./images/wrong.png")
cross_button = Button(image=cross_button_image, highlightthickness=0)
cross_button.grid(row=1, column=2)
cross_button.config(command=lambda: change_word(should_remove=False))
screen.mainloop()
