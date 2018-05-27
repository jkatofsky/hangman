"""
Josh Katofsky
B Block Python
October 2nd, 2017 - October 16th, 2017
Funny Word Hangman

This is a hangman game written in Python and implemented visually with the Pygame library
It uses a dicitonary of strictly the FUNNIEST words for a bit of added pizzaz
"""

import sys
import random
import pygame

# https://www.alphadictionary.com/articles/100_funniest_words.html
funnyWordDictionary = open("funnyWordDictionary.txt",
                           "r").read().upper().split("\n")[:-1]
# https://github.com/mikenorthorp/Hangman/tree/master/images
hangmanImages = [pygame.image.load(
    "images/hang%s.gif" % (i)) for i in range(7)]

# setting up the Pygame window and defining useful constants
pygame.init()
DISPLAY = pygame.display.set_mode((800, 500))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("FUNNY WORD HANGMAN")
SMALL_FONT = pygame.font.SysFont(None, 30)
MEDIUM_FONT = pygame.font.SysFont(None, 40)
BIG_FONT = pygame.font.SysFont(None, 50)
W, H = pygame.display.get_surface().get_size()

# A helper method for drawing centered text


def drawText(string, x, y, font, color):
    text = font.render(string, True, color)
    DISPLAY.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

# Returns true if all of the letters in the word are replaced by the correct guesses


def phraseGuessed(word, correctGuesses):
    word = word.replace(" ", "")
    for letter in correctGuesses:
        word = word.replace(str(letter), "")
    return len(word) is 0

# Generates the string displayed to the user showing their progress towards guessing the word


def getGuessingProgress(word, correctGuesses):
    phraseProgress = ""
    for character in word:
        if character in correctGuesses:
            phraseProgress += character
        elif character == " ":
            phraseProgress += " "
        else:
            phraseProgress += "_"
        phraseProgress += " "
    return phraseProgress


# Defining constants for the flow of the game
START, PLAY, WIN, LOSS = 0, 1, 2, 3
INCORRECT_LIMIT = 6

# A class that encapsulates everything for the hang man game's drawing and functionality


class HangmanGame:

    # The class variables set upon the instantiation of the class
    def __init__(self):
        self.gameState = START

    # The class variables set upon the beginning of the gameplay
    def setupPlay(self):
        self.word = random.choice(funnyWordDictionary)
        self.incorrectGuesses = []
        self.correctGuesses = []
        self.guessingProgress = getGuessingProgress(
            self.word, self.correctGuesses)
        self.gameState = PLAY

    # Updating the start based on events
    def updateStart(self, event):
        if event.type == pygame.KEYDOWN:
            self.setupPlay()
    # Drawing the start screen

    def drawStart(self):
        drawText("Welcome to funny word HangMan!",
                 W/2, H/2 - 50, BIG_FONT, (0, 0, 0))
        drawText("Press any key to play hangman with strictly the FUNNIEST WORDS",
                 W/2, H/2+50, SMALL_FONT, (0, 0, 0))

    # Updating the play based on events; this is where the real logic of hangman lives
    def updatePlay(self, event):
        if event.type == pygame.KEYDOWN:
            guess = chr(event.key).upper()
            if guess.isalpha():
                if guess in self.word:
                    if guess not in self.correctGuesses:
                        self.correctGuesses.append(guess)
                else:
                    if guess not in self.incorrectGuesses:
                        self.incorrectGuesses.append(guess)

                self.guessingProgress = getGuessingProgress(
                    self.word, self.correctGuesses)

                if phraseGuessed(self.word, self.correctGuesses):
                    self.gameState = WIN
                if len(self.incorrectGuesses) >= INCORRECT_LIMIT:
                    self.gameState = LOSS

    # Drawing the play screen
    def drawPlay(self):
        drawText(self.guessingProgress, W/2, 50, BIG_FONT, (0, 0, 0))
        DISPLAY.blit(hangmanImages[len(self.incorrectGuesses)], (250, 100))
        drawText("Incorrect Guesses: " + str(self.incorrectGuesses)
                 [1:-1], W/2, H-50, MEDIUM_FONT, (0, 0, 0))

    # Updating both the win or loss screens based on events (they behave the excact same)
    def updateEnd(self, event):
        if event.type == pygame.KEYDOWN:
            self.gameState = START

    # Drawing the win or loss screens - they're layed out the same with the only difference being the content of the strings
    def drawWin(self):
        drawText("YOU GOT IT! The word was " + self.word +
                 "!", W/2, 50, MEDIUM_FONT, (0, 0, 0))
        DISPLAY.blit(hangmanImages[len(self.incorrectGuesses)], (250, 100))
        drawText("(press ESCAPE to quit or any other key to play again)",
                 W/2, H-50, SMALL_FONT, (0, 0, 0))

    def drawLoss(self):
        drawText("You dummy! The word was obviously " +
                 self.word + "!", W/2, 50, MEDIUM_FONT, (0, 0, 0))
        DISPLAY.blit(hangmanImages[len(self.incorrectGuesses)], (250, 100))
        drawText("(press ESCAPE to quit or any other key to play again)",
                 W/2, H-50, SMALL_FONT, (0, 0, 0))

    # This method is the culmination of all the other methods within the class, running the correct update and draw methods based on the current gameState and dealing with any Pygame baloney
    def run(self):

        for event in pygame.event.get():
            if self.gameState is START:
                self.updateStart(event)
            elif self.gameState is PLAY:
                self.updatePlay(event)
            elif self.gameState is WIN or self.gameState is LOSS:
                self.updateEnd(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((255, 255, 255))

        if self.gameState is START:
            self.drawStart()
        elif self.gameState is PLAY:
            self.drawPlay()
        elif self.gameState is WIN:
            self.drawWin()
        elif self.gameState is LOSS:
            self.drawLoss()

        pygame.display.update()


# The main function of the program - it instantiates a HangmanGame and calls its run method in an infinite loop
if __name__ == "__main__":
    game = HangmanGame()
    while True:
        CLOCK.tick(15)
        game.run()
