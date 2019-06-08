import argparse
import yaml
import logging
from schematics.models import Model
from schematics.types import StringType, FloatType
from schematics.exceptions import ValidationError
from Event import Event
from Participant import Team, Alliance

__author__ = 'AdmiralGT'

logging.basicConfig()
logger = logging.getLogger('gop_scorer')
logger.setLevel(logging.INFO)

class Sim(object):
    """
    A Simulation objects, runs a simulation of the scoring system and produces a result.
    """

    def __init__(self, config, iterations):
        """

        :param config: A dictionary of the configuration
        :param iterations: Integer, number of iterations to run this simulation for
        """
        self.teams = []
        self.events = []
        self.alliances = {}
        self.iterations = iterations

        # Add the teams
        for team in config['teams']:
            self.addTeam(team)

        # Add alliance events
        for ii in range(config['events']['alliance']):
            logger.info('Adding Alliance Event')
            self.events.append(Event(self.alliances.values(), config['scores']['alliance']))

        # Add normal events
        for ii in range(config['events']['normal']):
            logger.info('Adding Normal Event')
            self.events.append(Event(self.teams, config['scores']['normal']))

    def addTeam(self, team_config):
        """
        Add a team to the simulation

        :param team_config: Dictionary of team configuration
        """
        logger.info('Adding team {}'.format(team_config['name']))
        team = Team(team_config['name'], team_config['alliance'], team_config['strength'])
        self.teams.append(team)
        logger.info('Added team {} of alliance {} with strength {}'.format(team.name, team.alliance, team.strength))

        # Add this team to an alliance
        if team.alliance not in self.alliances:
            logger.info('Adding new alliance {}'.format(team.alliance))
            self.alliances[team.alliance] = Alliance(team.alliance)
        self.alliances[team.alliance].addTeam(team)

    def runSim(self):
        """
        Run the simulation
        """
        for ii in range(self.iterations):
            logger.debug('Running simulation {}'.format(ii))
            for event in self.events:
                logger.debug('Scoring Event')
                event.score_event()
            self.score_sim()

    def score_sim(self):
        """
        Score a single iteration of the simulation
        """

        # Sort the teams by their score, in descending order
        logger.debug('Sorting teams')
        self.teams.sort(key=lambda x: x.points)

        # Create a list of positions, noting that teams may finish on the same number of points so finish in the same
        # position.
        positions = set()
        for team in self.teams:
            positions.add(team.points)
        positions = list(positions)
        positions.sort(reverse=True)

        # Assign teams to their position
        pos = 1
        logger.debug(positions)
        for position_points in positions:
            # Assign the position to a temporary variable so all teams at this points can get the same position.
            temp_pos = pos
            for team in self.teams:
                # The next position needs to increment once for each team at this position.
                # There's an inefficiency here in that we loop through all teams, they should be sorted by score so
                # as soon as we've found some and then stopped we can move on.
                if position_points == team.points:
                    team.record_result(temp_pos)
                    pos += 1

    def print_results(self):
        """
        Print the results of the simulation
        """
        logger.info('=======================================')
        logger.info('Printing results')
        logger.info('=======================================')
        self.teams.sort(key=lambda x: x.name)
        for team in self.teams:
            logger.info('Team {}, Average position {}, Average points {}'.format(team.name,
                                                                                 team.total_positions / self.iterations,
                                                                                 team.total_points / self.iterations))


def parse_arguments():
    """
    Parse the arguments to this script
    """
    max_iterations = 1000000
    parser = argparse.ArgumentParser(description="Simulate Game of Phones competition scores.")
    parser.add_argument('config',
                        type=config_file_format,
                        help='The config file containing the teams, scores and events')
    parser.add_argument('--iterations', type=int, choices=range(max_iterations), action='store',
                        metavar='[0-{}]'.format(max_iterations), default=10000,
                        help='The number of iterations to simulate scoring for')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose logging')
    return parser.parse_args()


def validate_config(config, error_msg):
    """
    Validate a piece of configuration
    :param config: A dictionary that is a piece of configuration with an alliance and normal sections
    :param error_msg: What configuration section is being validated

    :raises: argparse.ArgumentTypeError if configuration is missing configuration
    """
    for type in ['alliance', 'normal']:
        if type not in config:
            raise argparse.ArgumentTypeError('Invalid {} config, no {}'.format(error_msg, type))


def config_file_format(path):
    """
    :param path: Filepath to the configuration file to validate
    :return: The validated configuration as a dictionary
    :raises: argparse.ArgumentTypeError if the configuration is invalid
    """

    # Load the yaml file
    with open(path) as config_file:
        config = yaml.safe_load(config_file)

    # Check every section of config is present
    config_types = ['teams', 'scores', 'events']
    for type in config_types:
        if type not in config:
            raise argparse.ArgumentTypeError('Config does not contain any {}'.format(type))

    # Read the teams section. Check against the TeamModel to check the team validity.
    teams = config['teams']
    alliances = set()
    for team in teams:
        t = TeamModel(team)
        try:
            t.validate()
            alliances.add(t.alliance)
        except ValidationError as e:
            raise argparse.ArgumentTypeError('Invalid config format: {}'.format(e.messages))

    # Validate the events and scoring section to make sure they have the necessary elements
    validate_config(config['events'], 'events')
    validate_config(config['scores'], 'scores')

    # The number of teams must match the number of scores for a normal team event otherwise we won't know what score to
    # assign a team in an event
    score_element = config['scores']['normal']
    if len(teams) != len(score_element):
        raise argparse.ArgumentTypeError('Must have same number of teams as number of scoring options in normal events, '
                                         'have {} teams and {} score options'.format(teams, score_element))

    # The number of alliances must match the number of scores for an alliance event otherwise we won't know what score to
    # assign teams in an event
    score_element = config['scores']['alliance']
    if len(alliances) != len(score_element):
        raise argparse.ArgumentTypeError('Must have same number of alliances as number of scoring options in alliances events, '
                                         'have {} alliances and {} score options'.format(alliances, score_element))

    return config

class TeamModel(Model):
    """
    Model for team configuration
    """
    name = StringType(required=True)
    strength = FloatType(required=True)
    alliance = StringType(required=True)

if __name__ == '__main__':
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    sim = Sim(args.config, args.iterations)
    sim.runSim()
    sim.print_results()

