import argparse
import yaml
import logging
from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.exceptions import ValidationError

__author__ = 'AdmiralGT'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Sim(object):

    def __init__(self, config):
        self.teams = []
        for team in config['teams']:
            self.teams.append(team)
        self.alliance_events = config['events']['alliance']
        self.normal_events = config['events']['normal']

    def addTeam(self, team):
        self.teams.append(team)

    def _score_alliance_event(self):
        pass

    def _score_normal_events(self):
        pass

    def runSim(self, iterations):
        for event in self.alliance_events:
            self._score_alliance_event()
        for event in self.normal_events:
            self._score_normal_event()


def parse_arguments():
    max_iterations = 10000
    parser = argparse.ArgumentParser(description="Calculate Doomtown Hand ranks.")
    parser.add_argument('config',
                        type=config_file_format,
                        help='The config file containing the teams, scores and events')
    parser.add_argument('--iterations', type=int, choices=range(max_iterations), action='store',
                        metavar='[0-{}]'.format(max_iterations), default=10,
                        help='The number of iterations to simulate scoring for')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose logging')
    return parser.parse_args()


def test_type(path):
    with open(path) as config_file:
        logger.info('Test')
        config = yaml.safe_load(config_file)
        return config

def validate_config(config, error_msg):
    for type in ['alliance', 'normal']:
        if type not in config:
            raise argparse.ArgumentTypeError('Invalid {} config, no {}'.format(error_msg, type))


def config_file_format(path):
    with open(path) as config_file:
        logger.info('Test')
        config = yaml.safe_load(config_file)
        config_types = ['teams', 'scores', 'events']
        for type in config_types:
            if type not in config:
                raise argparse.ArgumentTypeError('Config does not contain any {}'.format(type))

        teams = config['teams']
        alliances = set()
        for team in teams:
            t = Team(team)
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



class Team(Model):
    name = StringType(required=True)
    strength = IntType(required=True)
    alliance = StringType(required=True)


if __name__ == '__main__':
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    sim = Sim(args.config)
    sim.runSim(args.iterations)

