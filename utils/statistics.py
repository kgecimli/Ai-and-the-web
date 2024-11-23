
class Statistics:
    def __init__(self, questions, guesses, hints):
        self.questions = questions
        self.guesses = guesses
        self.hints = hints

    def __str__(self):
        return (f"Number of Questions = {self.questions} \nNumber of Guesses = {self.guesses} \nNumber of Hints = {self.hints} \n")


