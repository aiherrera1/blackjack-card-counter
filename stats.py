class Stats:
    def __init__(self, count_of_cards):
        self.count_of_cards = count_of_cards
        self.total_cards = sum(self.count_of_cards.values())
        self.total_cards_1_to_9 = sum(
            v for k, v in self.count_of_cards.items() if k != "10"
        )
        self.total_cards_2_to_13 = sum(
            v for k, v in self.count_of_cards.items() if k != "1"
        )
        self.dealer_european_hard_log = {}
        self.dealer_european_soft_log = {}
        self.dealer_american_log = {}
        self.stand_hard_log = {}
        self.stand_soft_log = {}
        self.hit_hard_log = {}
        self.hit_soft_log = {}
        self.hit_stand_hard_log = {}
        self.hit_stand_soft_log = {}
        self.double_hard_log = {}
        self.double_soft_log = {}
        self.hsd_hard_log = {}
        self.hsd_soft_log = {}
        self.split_log = {}
        self.split_best_log = {}
        self.hard_board = {}
        self.soft_board = {}
        self.split_board = {}
        self.get_stats()

    def dealer_european_hard(self, outcome, card):
        # outcome (16, 17, 18, 19, 20, 21) usamos 16 para simplificar el codigo, pero 16=bust
        # card (2-31)
        if (outcome, card) in self.dealer_european_hard_log:
            return self.dealer_european_hard_log[(outcome, card)]
        if card >= 22:
            if outcome == 16:
                self.dealer_european_hard_log[(outcome, card)] = 1
                return 1
            else:
                self.dealer_european_hard_log[(outcome, card)] = 0
                return 0
        elif card >= 17:
            if outcome == 16:
                self.dealer_european_hard_log[(outcome, card)] = 0
                return 0
            else:
                if card == outcome:
                    self.dealer_european_hard_log[(outcome, card)] = 1
                    return 1
                else:
                    self.dealer_european_hard_log[(outcome, card)] = 0
                    return 0
        else:
            suma = sum(
                [
                    self.dealer_european_hard(outcome, card + i + 2)
                    * self.count_of_cards[str(i + 2)]
                    for i in range(9)
                ]
            )
            suma += (
                self.dealer_european_soft(outcome, card + 11) * self.count_of_cards["1"]
            )
            self.dealer_european_hard_log[(outcome, card)] = suma / self.total_cards
            return suma / self.total_cards

    def dealer_european_soft(self, outcome, card):
        # outcome (16-21)
        # card (12-31)
        if (outcome, card) in self.dealer_european_soft_log:
            return self.dealer_european_soft_log[(outcome, card)]
        if card >= 22:
            prob = self.dealer_european_hard(outcome, card - 10)
            self.dealer_european_soft_log[(outcome, card)] = prob
            return prob
        elif card >= 17:
            if outcome == 16:
                self.dealer_european_soft_log[(outcome, card)] = 0
                return 0
            else:
                if card == outcome:
                    self.dealer_european_soft_log[(outcome, card)] = 1
                    return 1
                else:
                    self.dealer_european_soft_log[(outcome, card)] = 0
                    return 0
        else:
            suma = sum(
                [
                    self.dealer_european_soft(outcome, card + i + 1)
                    * self.count_of_cards[str(i + 1)]
                    for i in range(10)
                ]
            )
            self.dealer_european_soft_log[(outcome, card)] = suma / self.total_cards
            return suma / self.total_cards

    def dealer_american(self, outcome, card):
        # outcome (16-21)
        # card (1-10)
        if (outcome, card) in self.dealer_american_log:
            return self.dealer_american_log[(outcome, card)]
        if card == 10:
            suma = sum(
                [
                    self.dealer_european_hard(outcome, i)
                    * self.count_of_cards[str(i - 10)]
                    for i in range(12, 21)
                ]
            )
            self.dealer_american_log[(outcome, card)] = suma / self.total_cards_2_to_13
            return suma / self.total_cards_2_to_13
        elif card == 1:
            suma = sum(
                [
                    self.dealer_european_soft(outcome, i)
                    * self.count_of_cards[str(i - 11)]
                    for i in range(12, 21)
                ]
            )
            self.dealer_american_log[(outcome, card)] = suma / self.total_cards_1_to_9
            return suma / self.total_cards_1_to_9
        else:
            prob = self.dealer_european_hard(outcome, card)
            self.dealer_american_log[(outcome, card)] = prob
            return prob

    def stand_hard(self, outcome, card):
        if (outcome, card) in self.stand_hard_log:
            return self.stand_hard_log[(outcome, card)]
        if outcome == 4:
            total = self.dealer_american(16, card) - sum(
                [self.dealer_american(i, card) for i in range(17, 22)]
            )
            self.stand_hard_log[(outcome, card)] = total
            return total
        elif outcome <= 16:
            prob = self.stand_hard(4, card)
            self.stand_hard_log[(outcome, card)] = prob
            return prob
        elif outcome <= 21:
            total = sum(
                [self.dealer_american(i, card) for i in range(16, outcome)]
            ) - sum([self.dealer_american(i, card) for i in range(outcome + 1, 22)])
            self.stand_hard_log[(outcome, card)] = total
            return total
        else:
            self.stand_hard_log[(outcome, card)] = -1
            return -1

    def stand_soft(self, outcome, card):
        if (outcome, card) in self.stand_soft_log:
            return self.stand_soft_log[(outcome, card)]
        if outcome <= 21:
            prob = self.stand_hard(outcome, card)
            self.stand_soft_log[(outcome, card)] = prob
            return prob
        else:
            prob = self.stand_hard(outcome - 10, card)
            self.stand_soft_log[(outcome, card)] = prob
            return prob

    def hit_hard(self, outcome, card):
        if (outcome, card) in self.hit_hard_log:
            return self.hit_hard_log[(outcome, card)]
        if outcome <= 20:
            total = sum(
                [
                    self.hit_stand_hard(outcome + i + 2, card)
                    * self.count_of_cards[str(i + 2)]
                    for i in range(9)
                ]
            )
            total += self.hit_stand_soft(outcome + 11, card) * self.count_of_cards["1"]
            self.hit_hard_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards
        else:
            self.hit_hard_log[(outcome, card)] = -1
            return -1

    def hit_soft(self, outcome, card):
        if (outcome, card) in self.hit_soft_log:
            return self.hit_soft_log[(outcome, card)]
        if outcome <= 21:
            total = sum(
                [
                    self.hit_stand_soft(outcome + i + 1, card)
                    * self.count_of_cards[str(i + 1)]
                    for i in range(10)
                ]
            )
            self.hit_soft_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards
        else:
            prob = self.hit_hard(outcome - 10, card)
            self.hit_soft_log[(outcome, card)] = prob
            return prob

    def hit_stand_hard(self, outcome, card):
        if (outcome, card) in self.hit_stand_hard_log:
            return self.hit_stand_hard_log[(outcome, card)]
        if outcome <= 21:
            hit = self.hit_hard(outcome, card)
            stand = self.stand_hard(outcome, card)
            self.hit_stand_hard_log[(outcome, card)] = max(hit, stand)
            return max(hit, stand)
        else:
            self.hit_stand_hard_log[(outcome, card)] = -1
            return -1

    def hit_stand_soft(self, outcome, card):
        if (outcome, card) in self.hit_stand_soft_log:
            return self.hit_stand_soft_log[(outcome, card)]
        hit = self.hit_soft(outcome, card)
        stand = self.stand_soft(outcome, card)
        self.hit_stand_soft_log[(outcome, card)] = max(hit, stand)
        return max(hit, stand)

    def double_hard(self, outcome, card):
        if (outcome, card) in self.double_hard_log:
            return self.double_hard_log[(outcome, card)]
        if outcome <= 11:
            total = sum(
                [
                    self.stand_hard(outcome + 2 + i, card)
                    * self.count_of_cards[str(i + 2)]
                    for i in range(9)
                ]
            )
            total += self.stand_soft(outcome + 11, card) * self.count_of_cards["1"]
            total *= 2
            self.double_hard_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards
        elif outcome <= 21:
            total = (
                sum(
                    [
                        self.stand_hard(outcome + 1 + i, card)
                        * self.count_of_cards[str(i + 1)]
                        for i in range(10)
                    ]
                )
                * 2
            )
            self.double_hard_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards
        else:
            self.double_hard_log[(outcome, card)] = -2
            return -2

    def double_soft(self, outcome, card):
        if (outcome, card) in self.double_soft_log:
            return self.double_soft_log[(outcome, card)]
        if outcome <= 21:
            total = (
                sum(
                    [
                        self.stand_soft(outcome + 1 + i, card)
                        * self.count_of_cards[str(i + 1)]
                        for i in range(10)
                    ]
                )
                * 2
            )
            self.double_soft_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards
        else:
            prob = self.double_hard(outcome - 10, card)
            self.double_soft_log[(outcome, card)] = prob
            return prob

    def hsd_hard(self, outcome, card):
        if (outcome, card) in self.hsd_hard_log:
            return self.hsd_hard_log[(outcome, card)]
        hit = self.hit_hard(outcome, card)
        stand = self.stand_hard(outcome, card)
        double = self.double_hard(outcome, card)
        self.hsd_hard_log[(outcome, card)] = max(hit, stand, double)
        return max(hit, stand, double)

    def hsd_soft(self, outcome, card):
        if (outcome, card) in self.hsd_soft_log:
            return self.hsd_soft_log[(outcome, card)]
        hit = self.hit_soft(outcome, card)
        stand = self.stand_soft(outcome, card)
        double = self.double_soft(outcome, card)
        self.hsd_soft_log[(outcome, card)] = max(hit, stand, double)
        return max(hit, stand, double)

    def split(self, outcome, card):
        if (outcome, card) in self.split_log:
            return self.split_log[(outcome, card)]
        if outcome == 1:
            total = (
                sum(
                    [
                        self.stand_soft(outcome + 11 + i, card)
                        * self.count_of_cards[str(i + 1)]
                        for i in range(10)
                    ]
                )
                * 2
            )
            self.split_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards

        else:
            total = sum(
                [
                    self.hsd_hard(outcome + 2 + i, card)
                    * self.count_of_cards[str(i + 2)]
                    for i in range(9)
                ]
            )
            total += self.hsd_soft(outcome + 11, card) * self.count_of_cards["1"]
            total *= 2
            self.split_log[(outcome, card)] = total / self.total_cards
            return total / self.total_cards

    def split_best(self, outcome, card):
        if (outcome, card) in self.split_best_log:
            return self.split_best_log[(outcome, card)]
        split = self.split(outcome, card)
        if outcome == 1:
            hsd = self.hsd_soft(12, card)
        else:
            hsd = self.hsd_hard(outcome * 2, card)
        self.split_best_log[(outcome, card)] = max(split, hsd)
        return max(split, hsd)

    def get_stats(self):
        for outcome in range(16, 22):
            for card in range(2, 32):
                self.dealer_european_hard(outcome, card)
            for card in range(12, 32):
                self.dealer_european_soft(outcome, card)
            for card in range(1, 11):
                self.dealer_american(outcome, card)
        for card in range(1, 11):
            for outcome in range(4, 32):
                self.stand_hard(outcome, card)
                self.hit_hard(outcome, card)
                self.hit_stand_hard(outcome, card)
                self.double_hard(outcome, card)
                self.hsd_hard(outcome, card)
            for outcome in range(12, 32):
                self.stand_soft(outcome, card)
                self.hit_soft(outcome, card)
                self.hit_stand_soft(outcome, card)
                self.double_soft(outcome, card)
                self.hsd_soft(outcome, card)
        for outcome in range(1, 11):
            for card in range(1, 11):
                self.split(outcome, card)
                self.split_best(outcome, card)
        self.get_hsd_hard_board()
        self.get_hsd_soft_board()
        self.get_split_board()

    def get_hsd_hard_board(self):
        for x in range(4, 32):
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]:
                if self.hsd_hard_log[(x, y)] == self.stand_hard_log[(x, y)]:
                    self.hard_board[(x, y)] = "STAND"
                else:
                    if self.hsd_hard_log[(x, y)] == self.double_hard_log[(x, y)]:
                        self.hard_board[(x, y)] = "DOUBLE"
                    else:
                        self.hard_board[(x, y)] = "HIT"

    def get_hsd_soft_board(self):
        for x in range(12, 22):
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]:
                if self.hsd_soft_log[(x, y)] == self.stand_soft_log[(x, y)]:
                    self.soft_board[(x, y)] = "STAND"
                else:
                    if self.hsd_soft_log[(x, y)] == self.double_soft_log[(x, y)]:
                        self.soft_board[(x, y)] = "DOUBLE"
                    else:
                        self.soft_board[(x, y)] = "HIT"

    def get_split_board(self):
        for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]:
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]:
                if self.split_log[(x, y)] == self.split_best_log[(x, y)]:
                    self.split_board[(x, y)] = "SPLIT"
                else:
                    self.split_board[(x, y)] = "N"

    def perfect_move(self, dealer, player, split=True):
        if len(player) == 2 and player[0] == player[1] and split:
            if self.split_board[(player[0], dealer)] == "SPLIT":
                return "SPLIT"
        if self.is_soft(player):
            if self.soft_board[(sum(player) + 10, dealer)] == "DOUBLE" and (
                len(player) != 2 or not split
            ):
                return "HIT"
            return self.soft_board[(sum(player) + 10, dealer)]
        if self.hard_board[(sum(player), dealer)] == "DOUBLE" and (
            len(player) != 2 or not split
        ):
            return "HIT"
        return self.hard_board[(sum(player), dealer)]

    def is_soft(self, player):
        if 1 in player and sum(player) + 10 <= 21:
            return True
        return False


if __name__ == "__main__":
    count_of_cards = {
        "1": 4 * 8,
        "2": 4 * 8,
        "3": 4 * 8,
        "4": 4 * 8,
        "5": 4 * 8,
        "6": 4 * 8,
        "7": 4 * 8,
        "8": 4 * 8,
        "9": 4 * 8,
        "10": 16 * 8,
    }
    while True:
        stats = Stats(count_of_cards)
        print("=" * 50)
        print("Enter dealer and player cards")
        print("Dealer Card: ")
        dealer = int(input())
        count_of_cards[str(dealer)] -= 1
        print("Player Cards: (separate cards by space, use 1 for Ace)")
        player = [int(x) for x in input().split()]
        for card in player:
            count_of_cards[str(card)] -= 1
        print(dealer, player)
        print(stats.perfect_move(dealer, player, split=False))
