import random
import json
import inquirer
from termcolor import colored
from clear import main as clr
from tabulate import tabulate
from datetime import datetime


class Card:
  def __init__(self, colour, value):
    self.colour = colour
    self.value = value
    self.ascii = [[] for i in range(9)]

    if self.value == 10:
      space = ""
    else:
      space = " "

    self.ascii[0].append(colored("┌─────────┐", self.colour))
    self.ascii[1].append(colored(f"│{self.value}{space}       │", self.colour))
    self.ascii[2].append(colored("│         │", self.colour))
    self.ascii[3].append(colored("│         │", self.colour))
    self.ascii[4].append(colored(f"│    {self.colour[0].upper()}    │", self.colour))
    self.ascii[5].append(colored("│         │", self.colour))
    self.ascii[6].append(colored("│         │", self.colour))
    self.ascii[7].append(colored(f"│       {space}{self.value}│", self.colour))
    self.ascii[8].append(colored("└─────────┘", self.colour))

    self.ascii = "\n".join(["".join(line) for line in self.ascii])


class Deck:
  def __init__(self):
    self.cards = []
    self.create()

  def create(self):
    for colour in ["red", "black", "yellow"]:
      for value in range(10): self.cards.append(Card(colour, value + 1))

  def shuffle(self):
    random.shuffle(self.cards)


class Player:
  def __init__(self, player, username):
    self.number = player
    self.username = username
    self.hand = []

  def draw_card(self, deck):
    input(colored("\nPlayer %d (%s): Press Enter to pick up a card: " % (self.number, self.username), "blue",))
    self.hand.append(deck.cards.pop())
    print("\nPlayer %d (%s) has received:\n" % (self.number, self.username))
    print(colored(self.hand[-1].ascii, self.hand[-1].colour))


def evaluate(player_1, player_2):
  if player_1.hand[-1].colour == player_2.hand[-1].colour:
    if player_1.hand[-1].value > player_2.hand[-1].value:
      player_1.hand.append(player_2.hand.pop())
      return True
    elif player_2.hand[-1].value > player_1.hand[-1].value:
      player_2.hand.append(player_1.hand.pop())
      return False
  elif (player_1.hand[-1].colour == "red" and player_2.hand[-1].colour == "black"):
    player_1.hand.append(player_2.hand.pop())
    return True
  elif (player_1.hand[-1].colour == "red" and player_2.hand[-1].colour == "yellow"):
    player_2.hand.append(player_1.hand.pop())
    return False
  elif (player_1.hand[-1].colour == "yellow" and player_2.hand[-1].colour == "red"):
    player_1.hand.append(player_2.hand.pop())
    return True
  elif (player_1.hand[-1].colour == "yellow" and player_2.hand[-1].colour == "black"):
    player_2.hand.append(player_1.hand.pop())
    return False
  elif (player_1.hand[-1].colour == "black" and player_2.hand[-1].colour == "yellow"):
    player_1.hand.append(player_2.hand.pop())
    return True
  elif (player_1.hand[-1].colour == "black" and player_2.hand[-1].colour == "red"):
    player_2.hand.append(player_1.hand.pop())
    return False


def log(username, points):
   # Read the existing JSON file (if it exists) and load its contents
  try:
    with open("log.json", "r") as logfile:
      log_contents = json.load(logfile)
  except FileNotFoundError:
    log_contents = {}

    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  # Update the user's entry or create a new entry
  if username in log_contents:
    log_contents[username].append({"date": current_date, "points": points})
  else:
    log_contents[username] = [{"date": current_date, "points": points}]

  # Store the updated dictionary back into the JSON file
  with open("log.json", "w") as logfile:
    json.dump(log_contents, logfile, indent=3)


def main(player_1_username="test", player_2_username="test2"):
  clr()
  my_deck = Deck()
  player_1 = Player(1, player_1_username)
  player_2 = Player(2, player_2_username)
  my_deck.shuffle()

  for i in range(15):
    print(tabulate([[player_1.username, len(player_1.hand)], [player_2.username, len(player_2.hand)]], ["Player", "Points"], tablefmt="simple_grid"))
    player_1.draw_card(my_deck)
    player_2.draw_card(my_deck)
    if evaluate(player_1, player_2):
      print(colored("\nPlayer 1 Wins", "green"))
    else:
      print(colored("\nPlayer 2 Wins", "green"))
    input(colored("\nPress Enter to continue: ", "blue"))
    clr()

  if len(player_1.hand) > len(player_2.hand):
    winner = player_1
  else:
    winner = player_2

  print(colored("Player %d (%s) wins the game with %d points!\n" % (winner.number, winner.username, len(winner.hand)), "green",))
  print(colored("The winning cards are:", "green"))

  for i in range(0, len(winner.hand), 9):
    cards = winner.hand[i:i + 9]
    card_lines = [card.ascii.split("\n") for card in cards]
    combined_lines = [" ".join(lines) for lines in zip(*card_lines)]
    for line in combined_lines:
      print(line)
    print()

    log(winner.username, len(winner.hand))

  if inquirer.confirm("Play again?"):
    main(player_1.username, player_2.username)
  else:
    exit()


if __name__ == "__main__":
    main()
