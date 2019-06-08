# gop_scoring_sim

Scoring simulator for the Game of Phones event.

Usage:

```
gop_scoring_sim.py [-h] [--iterations [0-10000]] [-v] config

Simulate Game of Phones competition scores.

positional arguments:
  config                The config file containing the teams, scores and
                        events

optional arguments:
  -h, --help            show this help message and exit
  --iterations [0-10000]
                        The number of iterations to simulate scoring for
  -v                    Verbose logging
```

A configuration file must be provided, an example is provided in `config.yaml`.
The configuration file must take the following format:

```
scores:
  alliance:
  - list of integer scores, in descending order, the number of which must match the 
    number of unique alliance defined in teams->alliance.
  normal:
  - list of integer scores, in descending order, the number of which must match the
    number of teams defined.
teams:
    - a list of teams, each in the following format
    - name: <Team name, string>
      strength: <Comparitive strength, float
      alliance: <Alliance name, string>
events:
  alliance: <number of alliance events, integer>
  normal: <number of normal events, integer>
```