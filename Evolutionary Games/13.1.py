import numpy as np
import matplotlib.pyplot as plt

"""
N = 10      # Rounds
T = 0       # Betrayer
R = 0.5     # Both cooperate
P = 1       # Both defect
S = 1.5     # Betrayed
"""

class Main:

    def __init__(self, defect):
        self.defect = defect
        self.init_defect = defect
        self.years = 0.
        self.choices = []

    def reset(self):
        self.years = 0
        self.choices = []
        self.defect = self.init_defect


def play(rules, player1, player2):
    player1.reset()
    player2.reset()

    for i in range(rules.get("Rounds")):
        if i < player1.defect:
            player1.choices.append("coop")
        else:
            player1.choices.append("defect")
        if i < player2.defect:
            player2.choices.append("coop")
        else:
            player2.choices.append("defect")

        if player1.choices[i] == "defect":
            player2.defect = 0
        elif player2.choices[i] == "defect":
            player1.defect = 0

    count_years(player1, player2, rules)


def count_years(p1, p2, rules):  # add years based on choices and rules
    for i in range(rules.get("Rounds")):
        if p1.choices[i] == p2.choices[i] and p1.choices[i] == "coop":
            p1.years += rules.get("R")
            p2.years += rules.get("R")
        if p1.choices[i] == p2.choices[i] and p1.choices[i] == "defect":
            p1.years += rules.get("P")
            p2.years += rules.get("P")
        if p1.choices[i] == "coop" and p2.choices[i] == "defect":
            p1.years += rules.get("S")
            p2.years += rules.get("T")
        if p1.choices[i] == "defect" and p2.choices[i] == "coop":
            p1.years += rules.get("T")
            p2.years += rules.get("S")


if __name__ == "__main__":
    # initialize arrays and constants
    dilemma_rules = {"Rounds": 10, "T": 0, "R": 0.5, "P": 1, "S": 1.5}
    final_years_p1 = []
    years_p1 = []
    years_p2 = []
    values = 11
    for i in range(values):
        prisoner1 = Main(defect=i)  # initialize a prisoner with defect of 0-10
        prisoner2 = Main(defect=6)  # initialize a prisoner with defect of 6
        play(dilemma_rules, prisoner1, prisoner2)  # play the game with the two prisoners
        final_years_p1.append(prisoner1.years)  # add the results from the game to the array

    for j in range(values):
        player1 = Main(defect=j)
        for k in range(values):
            player2 = Main(defect=k)
            play(dilemma_rules, player1, player2)
            years_p1.append(player1.years)
            years_p2.append(player2.years)

    #print("p1 years:", len(years_p1))
    #print("p2 years:", len(years_p2))
    #print(np.array(years_p1).reshape(-1, 11))
    #print(np.array(years_p2).reshape(-1, 11))

    fig, axes = plt.subplots(nrows=1, ncols=2)
    x = np.linspace(0, 10, values, endpoint=True)  # m
    y = np.linspace(0, 10, values, endpoint=True)  # n
    axes[0].plot(x, final_years_p1)
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('Years in prison')
    c = axes[1].pcolor(x, y, np.array(years_p1).reshape(-1, 11))
    axes[1].set_xlabel('m')
    axes[1].set_ylabel('n')
    fig.colorbar(c, ax=axes[1])
    plt.show()
