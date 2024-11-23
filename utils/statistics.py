
class Statistics:
    def __init__(self, questions, guesses, hints):
        self.questions = questions
        self.guesses = guesses
        self.hints = hints

    def __str__(self):
        return (f"Number of Questions = {self.questions} \n Number of Guesses = {self.guesses} \n Number of Hints = {self.hints} \n")
               # f"Number of games played {self.games_played} Average number of guesses = {self.average_guesses} ")

