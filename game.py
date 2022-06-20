from shoe import Shoe
from prob import Stats

print("hi")
shoe = Shoe(8)
stats = Stats(shoe)


# turn 
dealer = []
player = []

dealer.append(shoe.get_card())
player.append(shoe.get_card())
player.append(shoe.get_card())
print(dealer)
print(player)
# print(stats.perfect_move(dealer, player))





