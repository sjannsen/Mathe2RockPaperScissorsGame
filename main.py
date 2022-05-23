from tkinter import *
from PIL import Image, ImageTk
from enum import Enum
import random
import numpy as np
from numpy import ndarray

np.set_printoptions(formatter={'float_kind': '{:f}'.format})  # to avoid scientific notations which mess up the format


# DEFINITION FOR REGRET AI
class Action(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


def get_payoff(action_1: Action, action_2: Action) -> int:  # returns payoff for the AI
    mod3_val = (action_1.value - action_2.value) % 3
    if mod3_val == 2:
        return -1
    else:
        return mod3_val


def get_strategy(cumulative_regrets: np.array) -> np.array:  # returns the strategy based on regret matching
    pos_cumulative_regrets = np.maximum(0, cumulative_regrets)
    if sum(pos_cumulative_regrets) > 0:
        return pos_cumulative_regrets / sum(pos_cumulative_regrets)
    else:
        return np.full(shape=len(Action), fill_value=1 / len(Action))


def get_regrets(payoff: int, action_2: Action) -> ndarray:  # returns the regret
    return np.array([get_payoff(a, action_2) - payoff for a in Action])


# main window
root = Tk()
root.title("Rock Paper Scissor")
root.configure(background="#9b59b6")

# pictures
rock_image = ImageTk.PhotoImage(Image.open("rock-user.png"))
paper_image = ImageTk.PhotoImage(Image.open("paper-user.png"))
scissors_image = ImageTk.PhotoImage(Image.open("scissors-user.png"))

rock_image_computer = ImageTk.PhotoImage(Image.open("rock.png"))
paper_image_computer = ImageTk.PhotoImage(Image.open("paper.png"))
scissors_image_computer = ImageTk.PhotoImage(Image.open("scissors.png"))

# inserting pictures
user_label = Label(root, image=scissors_image, background="#9b59b6")
user_label.grid(row=1, column=4)
computer_label = Label(root, image=scissors_image_computer, background="#9b59b6")
computer_label.grid(row=1, column=0)

# scores
playerScore = Label(root, text=0, font=100, background="#9b59b6", foreground="white")
computerScore = Label(root, text=0, font=100, background="#9b59b6", foreground="white")

playerScore.grid(row=1, column=3)
computerScore.grid(row=1, column=1)

# indicators
user_indicator = Label(root, font=50, text="USER", background="#9b59b6", foreground="white")
computer_indicator = Label(root, font=50, text="COMPUTER", background="#9b59b6", foreground="white")

user_indicator.grid(row=0, column=3)
computer_indicator.grid(row=0, column=1)

# messages
message = Label(root, font=50, background="#9b59b6", foreground="white")
message.grid(row=3, column=2)


# update message
def updateMessage(x):
    message['text'] = x


# update player score
def updateUserScore():
    score = int(playerScore["text"])
    score += 1
    playerScore["text"] = str(score)


# update computer score
def updateComputerScore():
    score = int(computerScore["text"])
    score += 1
    computerScore["text"] = str(score)


# check winner
def checkWinner(player, computer):
    if player == computer:
        updateMessage("Its a tie!")
    elif player == "rock":
        if computer == "paper":
            updateMessage("You loose")
            updateComputerScore()
        else:
            updateMessage("You win")
            updateUserScore()
    elif player == "paper":
        if computer == "scissors":
            updateMessage("You loose")
            updateComputerScore()
        else:
            updateMessage("You win")
            updateUserScore()
    elif player == "scissors":
        if computer == "rock":
            updateMessage("You loose")
            updateComputerScore()
        else:
            updateMessage("You win")
            updateUserScore()
    else:
        pass


# update choices
num_iterations = 0
cumulative_regrets = np.zeros(shape=(len(Action)), dtype=int)
strategy_sum = np.zeros(shape=(len(Action)))


def updateChoice(x):
    # for computer
    global num_iterations
    global cumulative_regrets
    global strategy_sum
    computerChoiceString: string

    num_iterations += 1
    strategy = get_strategy(cumulative_regrets)  # compute the strategy according to regret matching
    strategy_sum += strategy  # add the strategy to our running total of strategy probabilities

    computerChoice = random.choices(list(Action), weights=strategy)[0]  # Choose our action and our opponent's action

    if computerChoice == Action.ROCK:
        computer_label.configure(image=rock_image)
        computerChoiceString = "rock"
    elif computerChoice == Action.PAPER:
        computer_label.configure(image=paper_image)
        computerChoiceString = "paper"
    else:
        computer_label.configure(image=scissors_image)
        computerChoiceString = "scissors"

    # for user
    if x == "rock":
        user_label.configure(image=rock_image)
        playerChoice = Action.ROCK
    elif x == "paper":
        user_label.configure(image=paper_image)
        playerChoice = Action.PAPER

    else:
        user_label.configure(image=scissors_image)
        playerChoice = Action.SCISSORS

    #  compute the payoff and regrets
    our_payoff = get_payoff(computerChoice, playerChoice)
    regrets = get_regrets(our_payoff, playerChoice)
    cumulative_regrets += regrets  # add regrets from this round to the cumulative regrets

    optimal_strategy = strategy_sum / num_iterations
    print(num_iterations, optimal_strategy, computerChoice)

    checkWinner(x, computerChoiceString)


# buttons
rock = Button(root, width=20, height=2, text="ROCK", background="#FF3E4D", foreground="white",
              command=lambda: updateChoice("rock"))
paper = Button(root, width=20, height=2, text="PAPER", background="#FAD02E", foreground="white",
               command=lambda: updateChoice("paper"))
scissor = Button(root, width=20, height=2, text="SCISSORS", background="#0ABDE3", foreground="white",
                 command=lambda: updateChoice("scissors"))

rock.grid(row=2, column=1)
paper.grid(row=2, column=2)
scissor.grid(row=2, column=3)

root.mainloop()
