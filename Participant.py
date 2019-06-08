import logging

logger = logging.getLogger('gop_scorer')

class EventParticipant(object):
    """
    Super class of Participants
    """

    def __init__(self, name, strength):
        """

        :param name: The name of this participant
        :param strength: The strength of this participant
        """
        self.name = name
        self.strength = float(strength)

class Team(EventParticipant):
    """
    A Team of players e.g. Stark, Lannister
    """

    def __init__(self, name, alliance, strength):
        """

        :param name: The name of this team, used to identify team
        :param alliance: The name of the alliance this team is in.
        :param strength: The comparative strength of this team.
        """
        super(Team, self).__init__(name, strength)
        self.alliance = alliance
        self.points = 0
        self.total_positions = 0
        self.total_points = 0

    def score_points(self, score):
        """
        Score points for this team for an event.
        :param score: The score this team received in an event
        """
        logger.debug('Team {} scoring {} points'.format(self.name, score))
        self.points += int(score)
        logger.debug('Team {} now has {} points'.format(self.name, self.points))

    def record_result(self, position):
        """
        Record a result for a competition
        :param position: The position the team finished in.
        """
        logger.debug('Team {} scored {} points in position {}'.format(self.name, self.points, position))
        self.total_points += self.points
        self.total_positions += position
        self.points = 0

class Alliance(EventParticipant):
    """
    An alliance of teams.
    """

    def __init__(self, name):
        """

        :param name: The name of the alliance
        """
        super(Alliance, self).__init__(name, 0)
        self.teams = []

    def addTeam(self, team):
        """
        Add a team to this alliance
        :param team: A Team object to add to this alliance
        """
        logger.info('Added {} to alliance {}'.format(team.name, self.name))
        self.teams.append(team)
        self.strength += team.strength

    def score_points(self, score):
        """
        Score points for all the teams in this alliance for an Alliance event.
        :param score: The score this alliance got
        """
        logger.debug('Alliance {} scoring {} points'.format(self.name, score))
        for team in self.teams:
            team.score_points(score)

