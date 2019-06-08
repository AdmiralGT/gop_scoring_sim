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

    def __init__(self, config, iterations):
        self.teams = []
        self.events = []
        self.alliances = {}
        self.iterations = iterations
        for team in config['teams']:
            self.addTeam(team)

        for ii in range(config['events']['alliance']):
            logger.info('Adding Alliance Event')
            self.events.append(Event(self.alliances.values(), config['scores']['alliance']))
        for ii in range(config['events']['normal']):
            logger.info('Adding Normal Event')
            self.events.append(Event(self.teams, config['scores']['normal']))

    def addTeam(self, team_config):
        logger.info('Adding team {}'.format(team_config['name']))
        team = Team(team_config['name'], team_config['alliance'], team_config['strength'])
        self.teams.append(team)
        logger.info('Added team {} of alliance {} with strength {}'.format(team.name, team.alliance, team.strength))
        if team.alliance not in self.alliances:
            logger.info('Adding new alliance {}'.format(team.alliance))
            self.alliances[team.alliance] = Alliance(team.alliance)
        self.alliances[team.alliance].addTeam(team)

    def runSim(self):
        for ii in range(self.iterations):
            logger.debug('Running simulation {}'.format(ii))
            for event in self.events:
                logger.debug('Scoring Event')
                event.score_event()
            self.score_sim()

    def score_sim(self):
        logger.debug('Sorting teams')
        self.teams.sort(key=lambda x: x.points)
        positions = set()
        for team in self.teams:
            positions.add(team.points)

        pos = 1
        positions = list(positions)
        positions.sort(reverse=True)
        logger.debug(positions)
        for position_points in positions:
            temp_pos = pos
            for team in self.teams:
                if position_points == team.points:
                    team.record_result(pos)
                    temp_pos += 1
            pos = temp_pos

    def print_results(self):
        logger.info('=======================================')
        logger.info('Printing results')
        logger.info('=======================================')
        self.teams.sort(key=lambda x: x.name)
        for team in self.teams:
            logger.info('Team {}, Average position {}, Average points {}'.format(team.name,
                                                                                 team.total_positions / self.iterations,
                                                                                 team.total_points / self.iterations))


def parse_arguments():
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
    for type in ['alliance', 'normal']:
        if type not in config:
            raise argparse.ArgumentTypeError('Invalid {} config, no {}'.format(error_msg, type))


def config_file_format(path):
    with open(path) as config_file:
        config = yaml.safe_load(config_file)
        config_types = ['teams', 'scores', 'events']
        for type in config_types:
            if type not in config:
                raise argparse.ArgumentTypeError('Config does not contain any {}'.format(type))

        teams = config['teams']
        alliances = set()
        for team in teams:
            t = TeamModel(team)
            try:
                t.validate()
                alliances.add(t.alliance)
            except ValidationError as e:
                raise argparse.ArgumentTypeError('Invalid config format: {}'.format(e.messages))

        validate_config(config['events'], 'events')
        validate_config(config['scores'], 'scores')

        if len(teams) != len(config['scores']['normal']):
            raise argparse.ArgumentTypeError('Must have same number of teams as number of scoring options in normal events, '
                                             'have {} teams and {} score options'.format(teams, config['scores']['normal']))

        if len(alliances) != len(config['scores']['alliance']):
            raise argparse.ArgumentTypeError('Must have same number of alliances as number of scoring options in alliances events, '
                                             'have {} alliances and {} score options'.format(alliances, config['scores']['alliance']))

        return config

class TeamModel(Model):
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

