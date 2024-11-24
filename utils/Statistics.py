class Statistics:
    def __init__(self, questions: int, guesses: int, hints: int):
        """
        Statistics class used to save information about an instance of the guessing game
        :param questions: number of questions
        :param guesses: number of guesses
        :param hints: number of hints
        """
        self.questions = questions
        self.guesses = guesses
        self.hints = hints

    def __str__(self) -> str:
        return (f"Number of Questions = {self.questions} \nNumber of Guesses = {self.guesses} \nNumber of Hints = "
                f"{self.hints} \n")
