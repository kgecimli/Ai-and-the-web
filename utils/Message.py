class Message:
    def __init__(self, role: str, message: str, hidden: bool = False):
        self.role = role
        self.message = message
        self.hidden = hidden

    def as_dict(self) -> dict:
        return {"role": self.role, "message": self.message, "hidden": self.hidden}