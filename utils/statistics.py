
class Statistics:
    def __init__(self, questions, guesses, games_played, average_guesses):
        self.questions = questions
        self.guesses = guesses
        self.games_played = games_played
        if self.games_played > 0:
            self.average_guesses = self.guesses/self.games_played
        else:
            self.average_guesses = 0
    questions = 0
    guesses = 0
    games_played = 0
    average_guesses = guesses / games_played

    def __str__(self):
        return f"Number of Questions = {self.questions} \n Number of Guesses = {self.guesses} \n Number of games played {self.games_played} Average number of guesses = {self.average_guesses} "

