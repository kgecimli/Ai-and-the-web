class Statistics:
    def __init__(self, questions: int = 0, guesses: int = 0, hints: int = 0, verybad=0, bad: int = 0, moderate: int = 0,
                 good: int = 0, verygood: int = 0, unknown: int = 0):
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
        return (
            f"| **Number of:**             | **Count** |\n"
            f"|----------------------|-------|\n"
            f"| Questions           | {self.questions} |\n"
            f"| Guesses             | {self.guesses} |\n"
            f"| Hints               | {self.hints} |\n"
            f"| Very Good Guesses   | {self.verygood} |\n"
            f"| Good Guesses        | {self.good} |\n"
            f"| Moderate Guesses    | {self.moderate} |\n"
            f"| Bad Guesses         | {self.bad} |\n"
            f"| Very Bad Guesses    | {self.verybad} |\n"
            f"| Unknown Guesses     | {self.unknown} |\n"
        )
