import random


class Shoe:
    def __init__(self, num_of_decks) -> None:
        self.num_of_decks = num_of_decks
        self.count_of_cards = {"1": 4, "2": 4, "3": 4, "4": 4,
                               "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 16}
        self.count_of_cards.update((key, value*self.num_of_decks)
                                   for key, value in self.count_of_cards.items())
        self.get_shoe()

    def get_shoe(self):
        self.shoe = []
        for i in range(1,9):
            self.shoe+=[f"{i}"]*4*self.num_of_decks
        self.shoe+=["10"]*16*self.num_of_decks           
        random.shuffle(self.shoe)
        
    def get_card(self):
        card= self.shoe.pop()
        self.count_of_cards[card]-=1
        return card

shoe = Shoe(8)
print(shoe.shoe)
print(shoe.count_of_cards)
shoe.get_card()
shoe.get_card()
print(shoe.count_of_cards)