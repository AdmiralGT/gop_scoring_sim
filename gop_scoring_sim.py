import argparse
import yaml
import logging
from schematics.models import Model
from schematics.types import StringType, IntType, DictType
from schematics.exceptions import ValidationError

__author__ = 'AdmiralGT'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Sim(object):

    def __init__(self):
        self.teams = []
        self.events = []

    def addTeam(self, team):
        self.teams.append(team)

    def _score_event(self):
        pass

    def runSim(self, iterations):
        for event in self.events:
            self._score_event()


def parse_arguments():
    max_iterations = 10000
    parser = argparse.ArgumentParser(description="Calculate Doomtown Hand ranks.")
    parser.add_argument('config',
                        type=config_file_format,
                        # type=test_type,
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

        for team in config['teams']:
            t = Team(team)
            try:
                t.validate()
            except ValidationError as e:
                raise argparse.ArgumentTypeError('Invalid config format: {}'.format(e.messages))

        validate_config(config['events'], 'events')
        validate_config(config['scores'], 'scores')

        return config



class Team(Model):
    strength = IntType(required=True)
    alliance = StringType(required=True)


if __name__ == '__main__':
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    sim = Sim()
    sim.runSim(args.iterations)

