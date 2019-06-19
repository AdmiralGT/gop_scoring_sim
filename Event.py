import random
import logging

logger = logging.getLogger('gop_scoring_sim')

class Event(object):
    """
    An event class, u
    """

    def __init__(self, teams, scores):
        self.scores = scores
        self.teams = teams

    def total_strength(self, teams):
        """
        The total strength of all remaining teams in this event
        :param teams: A list of teams to calculate total strength of
        :return: The sum of the teams strength
        """
        total_strength = 0
        for team in teams:
            total_strength += team.strength
        return total_strength

    def choose_next_placed_team(self, teams, strength):
        """
        Choose the next placed team in this event
        :param teams: A list of teams to choose the winning team from
        :param strength: The strength (between 0 and the combined teams strength) to choose the team
        :return: Team object, that placed next highest
        """
        current_strength = 0
        winning_team = None
        for team in teams:
            current_strength += team.strength
            if strength <= current_strength:
                return team

    def score_event(self):
        """
        Score the event.
        :return: None
        """

        teams = list(self.teams)
        for ii in range(len(teams)):
            logger.debug('Scoring position {}'.format(ii + 1))
            # Determine the total strength of all remaining teams
            total_strength = self.total_strength(teams)
            logger.debug('Total strength {}'.format(total_strength))
            winning_strength = random.uniform(0, total_strength)
            logger.debug('Winning strength {}'.format(winning_strength))
            # Choose which team places next
            next_placed_team = self.choose_next_placed_team(teams, winning_strength)
            logger.debug('Winning team {}'.format(next_placed_team.name))
            next_placed_team.score_points(self.scores[ii])
            # Remove this team from the remaining teams
            teams.remove(next_placed_team)
