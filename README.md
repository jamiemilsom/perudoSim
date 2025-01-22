# PerudoSim

A Python-based simulation framework for the dice game Perudo (also known as Liar's Dice), designed to develop and test optimal playing strategies through different player agent implementations.

## Overview

PerudoSim provides a platform for simulating Perudo games between different player agent classes, each implementing distinct strategies. The project aims to discover and optimise winning strategies through extensive simulation and analysis. i.e. take all the fun out of the game so I can beat all my friends reliably :)

## Game Rules

Perudo is a strategic dice game where players:
- Start with 5 dice each
- Make sequential bids about the total number of specific dice values across all players
- Can challenge other players' bids ("Dudo")
- Can call exact bids ("Calza")
- Use ones (1s) as wild cards that can represent any number
- Lose or gain dice based on successful/unsuccessful bids and challenges

For detailed rules, see the [Rules Documentation](docs/rules.md).

## Project Structure

```
perudoSim/
├── src/
│   ├── players_class.py  # Different player agent implementations
│   ├── game.py           # Core game logic
├── docs/                 # Documentation
│   ├── rules.md          # Rules in markdown
```

## Player Classes

The project includes various player implementations, each using different strategies:

- `BasePlayer`: Abstract base class defining the player interface
- `ConservativeStrat`: Uses probability calculations for decision-making taking minimal risks
- `MiltonMethod`: The rough way I personally play the game

## Running Simulations

```python
from player_classes import BasePlayer, ConservativeStrat, MiltonMethod
from game import GameState, PerudoGame

# Create simulation with different player types
simulate_games(
    10000, [ConservativeStrat, MiltonMethod, ConservativeStrat, MiltonMethod]
)
```

## Contact

Create an issue in the GitHub repository for questions or suggestions.
