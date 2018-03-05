from evntbus import Event


class HighScoreEvent(Event):
    def __init__(self, account, highscore):
        self.account = account
        self.highscore = highscore


class HighScoreCreatedEvent(HighScoreEvent):
    pass


class GotHighScoreEvent(HighScoreEvent):
    pass


class GotHighScoresEvent(Event):
    def __init__(self, account, highscores):
        self.account = account
        self.highscores = highscores
