import tkinter as tk
from tkinter import messagebox
import random
import time

root = tk.Tk()
root.title("Memory Game with DFS Tracking")

card_values = [str(i) for i in range(1, 9)] * 2
random.shuffle(card_values)
buttons = []
first_card = None
second_card = None
matched_pairs = 0
attempts = 0
start_time = None
revealed_cards = {}  

def start_game():
    global matched_pairs, attempts, start_time, revealed_cards
    matched_pairs = 0
    attempts = 0
    start_time = time.time()
    revealed_cards = {}
    update_score()
    random.shuffle(card_values)
    for button in buttons:
        button.config(text="", state="normal", bg="lightgray")
    result_label.config(text="")

def on_card_click(index):
    global first_card, second_card, matched_pairs, attempts
    
    button = buttons[index]
    
    # Show the card's value
    button.config(text=card_values[index], state="disabled")
    revealed_cards[index] = card_values[index]
    
    if first_card is None:
        first_card = index
    elif second_card is None:
        second_card = index
        attempts += 1
        update_score()
        if card_values[first_card] == card_values[second_card]:
            matched_pairs += 1
            first_card = None
            second_card = None
            if matched_pairs == 8:
                end_game()
        else:
            root.after(1000, reset_cards)
    else:
        reset_cards()
        first_card = index

def reset_cards():
    global first_card, second_card
    buttons[first_card].config(text="", state="normal", bg="lightgray")
    buttons[second_card].config(text="", state="normal", bg="lightgray")
    first_card = None
    second_card = None

def update_score():
    score_label.config(text=f"Attempts: {attempts}")

def end_game():
    elapsed_time = int(time.time() - start_time)
    messagebox.showinfo("Congratulations!", f"You matched all pairs!\nAttempts: {attempts}\nTime: {elapsed_time} seconds")
    result_label.config(text="You won!")

def provide_hint():
    if len(revealed_cards) < 2:
        messagebox.showinfo("Hint", "Not enough revealed cards to provide a hint.")
        return
    
    stack = list(revealed_cards.items())
    while stack:
        index1, value1 = stack.pop()
        for index2, value2 in revealed_cards.items():
            if index1 != index2 and value1 == value2:
                messagebox.showinfo("Hint", f"Try matching card {index1 + 1} with card {index2 + 1}.")
                return
    
    messagebox.showinfo("Hint", "No matching pairs found among the revealed cards.")

for i in range(16):
    button = tk.Button(root, text="", width=15 	, height=8, command=lambda i=i: on_card_click(i), bg="gray")
    button.grid(row=i//4, column=i%4)
    buttons.append(button)

score_label = tk.Label(root, text="Attempts: 0", font=("Helvetica", 14))
score_label.grid(row=4, column=0, columnspan=2)

restart_button = tk.Button(root, text="Restart Game", command=start_game)
restart_button.grid(row=4, column=2, columnspan=2)

hint_button = tk.Button(root, text="Get Hint", command=provide_hint)
hint_button.grid(row=4, column=4, columnspan=2)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.grid(row=5, column=0, columnspan=6)

start_game()

root.mainloop()
