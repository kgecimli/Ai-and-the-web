class Statistics:
    def __init__(self, questions: int = 0, guesses: int = 0, hints: int = 0, verybad=0, bad=0, moderate=0, good=0, verygood=0, unknown=0):
        """
        Statistics class used to save information about an instance of the guessing game
        :param questions: number of questions
        :param guesses: number of guesses
        :param hints: number of hints
        """
        self.questions = questions
        self.guesses = guesses
        self.hints = hints
        self.verybad = verybad
        self.bad = bad
        self.moderate = moderate
        self.good = good
        self.verygood = verygood
        self.unknown = unknown

    def __str__(self) -> str:
        return (f"Number of questions = {self.questions}  \nNumber of guesses = {self.guesses}  \nNumber of hints = "
                f"{self.hints}  \nNumber of very good guesses: {self.verygood}  \nNumber of good guesses: {self.good}"
                f"  \nNumber of moderate guesses: {self.moderate}  \nNumber of bad guesses: {self.bad}"
                f"  \nNumber of very bad guesses: {self.verybad}  \nNumber of unknown guesses: {self.unknown}")
