class Player:

    def __init__(self, number):
        self.cards = []
        self.number = number

    def __str__(self):
        return f"Player {self.number}: {self.cards}"

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def sort_cards(self):
        color_order = {'B': 0, 'G': 1, 'Y': 2, 'R': 3, 'C': 4, 'F': 4}
        self.cards = sorted(self.cards, key=lambda card: color_order[card[1]])


class Robot(Player):

    def __init__(self, number):
        super().__init__(number)

    def __str__(self):
        return f"Robot {self.number}: {self.cards}"

    def play_card(self, card):
        limit = len(self.cards)
        for i in range(limit):
            karta = self.cards[i]
            if karta[0] == card[0] or karta[1] == card[1]:
                self.cards.remove(karta)
                return karta
            elif karta == "CC":
                self.cards.remove(karta)
                return "C" + self.cards[0][1]
            elif karta == "PF":
                self.cards.remove(karta)
                return karta
        return None