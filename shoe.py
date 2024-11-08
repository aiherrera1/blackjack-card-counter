import random


class Shoe:
    def __init__(self, num_of_decks) -> None:
        self.num_of_decks = num_of_decks
        self.count_of_cards = {
            "1": 4,
            "2": 4,
            "3": 4,
            "4": 4,
            "5": 4,
            "6": 4,
            "7": 4,
            "8": 4,
            "9": 4,
            "10": 16,
        }
        self.count_of_cards.update(
            (key, value * self.num_of_decks)
            for key, value in self.count_of_cards.items()
        )
        self.get_shoe()

    def total_cards(self):
        return sum(self.count_of_cards.values())

    def running_count(self):
        return sum(
            1 if card in ["2", "3", "4", "5", "6"] else -1 if card in ["10", "1"] else 0
            for card in self.shoe
        )

    def true_count(self):
        return self.running_count() / (self.total_cards() / 52)

    def get_shoe(self):
        self.shoe = []
        for i in range(1, 9):
            self.shoe += [f"{i}"] * 4 * self.num_of_decks
        self.shoe += ["10"] * 16 * self.num_of_decks
        random.shuffle(self.shoe)

    def get_card(self):
        card = self.shoe.pop()
        self.count_of_cards[card] -= 1
        return card

    def remove_card(self, card):
        self.count_of_cards[card] -= 1
