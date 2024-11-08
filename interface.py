from tkinter import *
from tkinter import ttk
from shoe import Shoe
from stats import Stats


class Interface:
    def __init__(self) -> None:
        self.num_of_decks = 2
        self.shoe = Shoe(self.num_of_decks)
        self.root = Tk()
        self.root.title("Blackjack Card Counting and Strategy")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)

        # Main frame
        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        main_title = ttk.Label(
            self.mainframe,
            text="Blackjack Card Counting and Strategy",
            font=("Helvetica", 16, "bold"),
        )
        main_title.grid(column=0, row=0, columnspan=3, sticky=(N, W), pady=10)

        self.card_values = [str(i) for i in range(1, 11)]  # '1' represents Ace

        self.set_buttons()
        self.set_labels()
        self.set_entry()
        self.board_labels = {}
        self.board_label_colors = {}
        self.make_board()
        self.update_numbers()
        self.last_numbers = []

    def set_entry(self):
        self.controls_frame = ttk.Frame(
            self.mainframe, padding="5 5 5 5", relief="ridge"
        )
        self.controls_frame.grid(column=2, row=1, sticky=(N, W))
        self.controls_frame_label = ttk.Label(
            self.controls_frame, text="Controls", font=("Helvetica", 12, "bold")
        )
        self.controls_frame_label.grid(column=0, row=0, columnspan=2)

        label_num_of_decks = ttk.Label(self.controls_frame, text="Number of Decks:")
        label_num_of_decks.grid(column=0, row=1, sticky=W)
        self.slider = Scale(
            self.controls_frame, from_=1, to=8, orient=HORIZONTAL, length=150
        )
        self.slider.grid(column=0, row=2, sticky=(W, E))

        button_shuffle = ttk.Button(
            self.controls_frame, text="Shuffle", command=self.shuffle_shoe
        )
        button_shuffle.grid(column=0, row=3, sticky=W, pady=10)

    def set_buttons(self):
        self.button_frame = ttk.Frame(self.mainframe, padding="5 5 5 5", relief="ridge")
        self.button_frame.grid(column=0, row=1, sticky=(N, W))
        self.button_frame_label = ttk.Label(
            self.button_frame, text="Cards", font=("Helvetica", 12, "bold")
        )
        self.button_frame_label.grid(column=0, row=0, columnspan=2)

        for idx, val in enumerate(self.card_values):
            display_val = "A" if val == "1" else val
            button = ttk.Button(
                self.button_frame,
                text=display_val,
                command=lambda v=val: self.remove_card(v),
                width=5,
            )
            button.grid(column=idx % 2, row=1 + idx // 2, sticky=(W, E), padx=5, pady=5)

            key = val if val != "10" else "+"
            self.root.bind(key, lambda event, v=val: self.remove_card(v))

        self.root.bind("<Return>", lambda event: self.update_board())

    def set_labels(self):
        self.labels_frame = ttk.Frame(self.mainframe, padding="5 5 5 5", relief="ridge")
        self.labels_frame.grid(column=1, row=1, sticky=(N, W))
        self.labels_frame_label = ttk.Label(
            self.labels_frame, text="Counts", font=("Helvetica", 12, "bold")
        )
        self.labels_frame_label.grid(column=0, row=0, columnspan=2)

        self.card_counts = {}
        for idx, val in enumerate(self.card_values):
            self.card_counts[val] = StringVar()
            display_val = "A" if val == "1" else val
            label = ttk.Label(self.labels_frame, textvariable=self.card_counts[val])
            label.grid(column=0, row=1 + idx, sticky=W)

        self.cards_left = StringVar()
        label_cards_left = ttk.Label(self.labels_frame, textvariable=self.cards_left)
        label_cards_left.grid(column=0, row=1 + len(self.card_values), sticky=W, pady=5)

        self.running_count = StringVar()
        label_running_count = ttk.Label(
            self.labels_frame, textvariable=self.running_count
        )
        label_running_count.grid(
            column=0, row=2 + len(self.card_values), sticky=W, pady=5
        )

        self.true_count = StringVar()
        label_true_count = ttk.Label(self.labels_frame, textvariable=self.true_count)
        label_true_count.grid(column=0, row=3 + len(self.card_values), sticky=W, pady=5)

        self.expectation = StringVar()
        label_expectation = ttk.Label(self.labels_frame, textvariable=self.expectation)
        label_expectation.grid(
            column=0, row=4 + len(self.card_values), sticky=W, pady=5
        )

        self.last_cards_var = StringVar()
        label_last_cards = ttk.Label(
            self.labels_frame, textvariable=self.last_cards_var
        )
        label_last_cards.grid(column=0, row=5 + len(self.card_values), sticky=W, pady=5)

    def make_board(self):
        self.board_frame = ttk.Frame(self.mainframe, padding="5 5 5 5", relief="ridge")
        self.board_frame.grid(
            column=0, row=2, columnspan=3, sticky=(N, W, E, S), pady=10
        )
        self.board_frame_label = ttk.Label(
            self.board_frame,
            text="Strategy Board",
            font=("Helvetica", 14, "bold"),
        )
        self.board_frame_label.grid(column=0, row=0, columnspan=12, pady=5)

        dealer_upcards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]
        for idx, val in enumerate(dealer_upcards):
            display_val = "A" if val == 1 else str(val)
            label = Label(
                self.board_frame,
                text=display_val,
                bg="gray",
                width=5,
                relief="solid",
            )
            label.grid(column=1 + idx, row=1, sticky=(W, E))

        row_offset = 2
        self.stats = Stats(self.shoe.count_of_cards)
        dictionary = {
            "HIT": ("H", "#FF6347"),  # Tomato
            "STAND": ("S", "#32CD32"),  # LimeGreen
            "DOUBLE": ("D", "#1E90FF"),  # DodgerBlue
            "SPLIT": ("Y", "#FFD700"),  # Gold
            "NONE": ("N", "#6388FF"),  # LightSlateGrey
        }

        # Hard Totals
        for row_idx, total in enumerate(range(8, 19)):
            label = Label(
                self.board_frame,
                text=f"HARD {total}",
                bg="gray",
                width=10,
                relief="solid",
            )
            label.grid(column=0, row=row_offset + row_idx, sticky=(W, E))

            for col_idx, dealer_card in enumerate(dealer_upcards):
                move = self.stats.hard_board.get((total, dealer_card), "NONE")
                text, color = dictionary[move]
                move_label = Label(
                    self.board_frame,
                    text=text,
                    bg=color,
                    width=5,
                    relief="solid",
                )
                move_label.grid(
                    column=1 + col_idx, row=row_offset + row_idx, sticky=(W, E)
                )
                self.board_labels[f"hard({dealer_card},{total})"] = move_label

        row_offset += len(range(8, 19)) + 1  # Add a row for separation

        # Soft Totals
        for row_idx, total in enumerate(range(12, 20)):
            label = Label(
                self.board_frame,
                text=f"SOFT {total}",
                bg="gray",
                width=10,
                relief="solid",
            )
            label.grid(column=0, row=row_offset + row_idx, sticky=(W, E))

            for col_idx, dealer_card in enumerate(dealer_upcards):
                move = self.stats.soft_board.get((total, dealer_card), "NONE")
                text, color = dictionary[move]
                move_label = Label(
                    self.board_frame,
                    text=text,
                    bg=color,
                    width=5,
                    relief="solid",
                )
                move_label.grid(
                    column=1 + col_idx, row=row_offset + row_idx, sticky=(W, E)
                )
                self.board_labels[f"soft({dealer_card},{total})"] = move_label

        row_offset += len(range(12, 20)) + 1  # Add a row for separation

        # Splits
        player_pairs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]
        for row_idx, player_pair in enumerate(player_pairs):
            display_pair = "A,A" if player_pair == 1 else f"{player_pair},{player_pair}"
            label = Label(
                self.board_frame,
                text=display_pair,
                bg="gray",
                width=10,
                relief="solid",
            )
            label.grid(column=0, row=row_offset + row_idx, sticky=(W, E))

            for col_idx, dealer_card in enumerate(dealer_upcards):
                move = self.stats.split_board.get((player_pair, dealer_card), "NONE")
                if move == "SPLIT":
                    text, color = dictionary["SPLIT"]
                else:
                    text, color = dictionary.get(move, ("", "gray"))
                move_label = Label(
                    self.board_frame,
                    text=text,
                    bg=color,
                    width=5,
                    relief="solid",
                )
                move_label.grid(
                    column=1 + col_idx, row=row_offset + row_idx, sticky=(W, E)
                )
                self.board_labels[f"split({dealer_card},{player_pair})"] = move_label

    def update_board(self):
        self.stats = Stats(self.shoe.count_of_cards)
        dictionary = {
            "HIT": ("H", "#FF6347"),  # Tomato
            "STAND": ("S", "#32CD32"),  # LimeGreen
            "DOUBLE": ("D", "#1E90FF"),  # DodgerBlue
            "SPLIT": ("Y", "#FFD700"),  # Gold
            "NONE": ("N", "#6388FF"),  # LightSlateGrey
        }
        dealer_upcards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]

        # Update hard totals
        for dealer_card in dealer_upcards:
            for total in range(8, 19):
                move = self.stats.hard_board.get((total, dealer_card), "NONE")
                text, color = dictionary[move]
                label = self.board_labels.get(f"hard({dealer_card},{total})")
                if label:
                    label.configure(text=text, bg=color)

        # Update soft totals
        for dealer_card in dealer_upcards:
            for total in range(12, 20):
                move = self.stats.soft_board.get((total, dealer_card), "NONE")
                text, color = dictionary[move]
                label = self.board_labels.get(f"soft({dealer_card},{total})")
                if label:
                    label.configure(text=text, bg=color)

        # Update splits
        player_pairs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]
        for dealer_card in dealer_upcards:
            for player_pair in player_pairs:
                move = self.stats.split_board.get((player_pair, dealer_card), "NONE")
                if move == "SPLIT":
                    text, color = dictionary["SPLIT"]
                else:
                    text, color = dictionary.get(move, ("", "gray"))
                label = self.board_labels.get(f"split({dealer_card},{player_pair})")
                if label:
                    label.configure(text=text, bg=color)

    def update_numbers(self):
        for val in self.card_values:
            count = self.shoe.count_of_cards.get(val, 0)
            display_val = "A" if val == "1" else val
            self.card_counts[val].set(f"{display_val}: {count}")
        self.cards_left.set(f"Cards Left: {self.shoe.total_cards()}")
        self.running_count.set(f"Running Count: {round(self.shoe.running_count(), 5)}")
        self.true_count.set(f"True Count: {round(self.shoe.true_count(), 5)}")
        expectation_value = round(self.shoe.true_count(), 5) * 0.5 - 0.5
        self.expectation.set(f"Expectation: {expectation_value:+.5f}")

    def remove_card(self, card):
        self.last_numbers.insert(0, "A" if card == "1" else card)
        if len(self.last_numbers) == 11:
            self.last_numbers.pop()
        self.shoe.remove_card(card)
        self.update_numbers()
        self.update_board()
        self.last_cards_var.set("Last Cards: " + ", ".join(list(self.last_numbers)))

    def shuffle_shoe(self):
        self.num_of_decks = int(self.slider.get())
        self.shoe = Shoe(self.num_of_decks)
        self.update_numbers()
        self.update_board()


if __name__ == "__main__":
    interface = Interface()
    interface.root.mainloop()
