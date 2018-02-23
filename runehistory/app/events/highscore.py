from evntbus import Event


class HighScoreEvent(Event):
    def __init__(self, highscore):
        self.highscore = highscore


class HighScoreCreatedEvent(HighScoreEvent):
    pass


class GotHighScoreEvent(HighScoreEvent):
    pass


class GotHighScoresEvent(Event):
    def __init__(self, highscores):
        self.highscore = highscores
