import random
import logging

logger = logging.getLogger('gop_scorer')

class Event(object):

    def __init__(self, teams, scores):
        self.scores = scores
        self.teams = teams

    def total_strength(self, teams):
        total_strength = 0
        for team in teams:
            total_strength += team.strength
        return total_strength

    def winning_team(self, teams, strength):
        current_strength = 0
        winning_team = None
        for team in teams:
            current_strength += team.strength
            if strength <= current_strength:
                return team

    def score_event(self):
        teams = list(self.teams)
        for ii in range(len(self.teams)):
            logger.debug('Scoring position {}'.format(ii + 1))
            total_strength = self.total_strength(teams)
            logger.debug('Total strength {}'.format(total_strength))
            winning_strength = random.uniform(0, total_strength)
            logger.debug('Winning strength {}'.format(winning_strength))
            winning_team = self.winning_team(teams, winning_strength)
            logger.debug('Winning team {}'.format(winning_team.name))
            winning_team.score_points(self.scores[ii])
            teams.remove(winning_team)
