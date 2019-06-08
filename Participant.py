import logging

logger = logging.getLogger('gop_scorer')

class EventParticipant(object):

    def __init__(self, name, strength):
        self.name = name
        self.strength = float(strength)

class Team(EventParticipant):

    def __init__(self, name, alliance, strength):
        super(Team, self).__init__(name, strength)
        self.alliance = alliance
        self.points = 0
        self.total_positions = 0
        self.total_points = 0

    def score_points(self, score):
        logger.debug('Team {} scoring {} points'.format(self.name, score))
        self.points += int(score)
        logger.debug('Team {} now has {} points'.format(self.name, self.points))

    def record_result(self, position):
        logger.debug('Team {} scored {} points in position {}'.format(self.name, self.points, position))
        self.total_points += self.points
        self.total_positions += position
        self.points = 0

class Alliance(EventParticipant):

    def __init__(self, name):
        super(Alliance, self).__init__(name, 0)
        self.teams = []

    def addTeam(self, team):
        logger.info('Added {} to alliance {}'.format(team.name, self.name))
        self.teams.append(team)
        self.strength += team.strength

    def score_points(self, score):
        logger.debug('Alliance {} scoring {} points'.format(self.name, score))
        for team in self.teams:
            team.score_points(score)

