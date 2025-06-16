player_list = []


class PlayerScore:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def scoreChange(self, change):
        self.score += change

    def printScore(self):
        score = str(self.score)
        print(self.name + " has " + score + " points.")

    def isCringe(self):
        if self.score == 0:
            print(self.name + " has a fat 0 to their name.")
        elif self.score < 0:
            print(self.name + " is cringe. What a loser.")
        else:
            print(self.name + " is based. What a chad.")

    def addToList(self):
        player = [self.score, self.name]
        player_list.append(player)



def printList():
    for player_list_index in player_list:
        print(player_list_index[1] + " | " + str(player_list_index[0]))


def printLeaderboard():
    player_list.sort(reverse = True)
    printList()


def cringeStatus():
    based_list = []
    nothing_list = []
    cringe_list = []
    for x in player_list:
        if x[0] == 0:
            nothing_list.append(x[1])
        elif x[0] > 0:
            based_list.append(x[1])
        else:
            cringe_list.append(x[1])
    print("Players with based status:")
    print(based_list)
    print("Players with no status:")
    print(nothing_list)
    print("Players with cringe status:")
    print(cringe_list)


def deletePlayer(player_name):
    for x in player_list:
        if x[1] == player_name:
            player_list.remove(player_name)


def hardResetAll():
    pass


if __name__ == '__main__':
    base_score = 0
    Ruby = PlayerScore("Ruby", base_score)
    Casrai = PlayerScore("Casrai", base_score)
    Levia = PlayerScore("Levia", base_score)
    Kyu = PlayerScore("Kyu", base_score)
    Lunarya = PlayerScore("Lunarya", base_score)

    Ruby.scoreChange(20)
    Casrai.scoreChange(-10)
    Kyu.scoreChange(100)
    Lunarya.scoreChange(40)

    Ruby.addToList()
    Casrai.addToList()
    Levia.addToList()
    Kyu.addToList()
    Lunarya.addToList()

    printList()
    deletePlayer(Ruby)
    print("---------")
    printList()

