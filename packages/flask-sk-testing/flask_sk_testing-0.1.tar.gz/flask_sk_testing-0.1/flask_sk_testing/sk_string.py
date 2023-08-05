class SkString:
    def __init__(self, text):
        self.text = text

    def to_upper(self):
        return self.text.upper()

    def to_lower(self):
        return self.text.lower()

    def to_title(self):
        return self.text.title()        