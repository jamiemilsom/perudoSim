from typing import Dict, List, Optional, Tuple
import random
from abc import ABC, abstractmethod
from tabulate import tabulate


class BasePlayer(ABC):
    def __init__(self, name: str):
        self.name = name
        self.dice: List[str] = []  # List of dice values '1' to '6'
        self.dice_count = 5
        self.probabilities: Dict[str, float] = {}  # {die face: probability, ... }

    def roll_dice(self) -> None:
        self.dice = list(
            map(str, sorted([random.randint(1, 6) for _ in range(self.dice_count)]))
        )

    def calculate_probabilities(self, total_dice: int) -> None:
        known_dice = self.bin_dice(self.dice)
        unseen_dice = total_dice - self.dice_count
        wild_ones = known_dice["1"] + (unseen_dice * 1 / 6)

        self.probabilities = {
            str(face): known_dice[str(face)] + (unseen_dice * 1 / 6)
            for face in range(1, 7)
        }

    @staticmethod
    def bin_dice(dice: List[str]) -> Dict[str, int]:
        binned_dice = {str(i): 0 for i in range(1, 7)}
        for die in dice:
            binned_dice[die] += 1
        return binned_dice

    def lose_die(self) -> None:
        self.dice_count -= 1
        if self.dice_count > 0:
            self.dice = self.dice[:-1]

    @abstractmethod
    def make_bid(
        self, game_state: "GameState"
    ) -> Tuple[str, int]:  # (die, quantity) or (die, "Dudo")
        pass


class ConservativeStrat(BasePlayer):
    def make_bid(
        self, game_state: "GameState"
    ) -> Tuple[str, int]:  # (die, quantity) or (die, "Dudo")
        if game_state.previous_bid is None:
            return str(random.randint(3, 6)), max(
                1, game_state.total_dice // 6
            )  # reasonable starting bid

        prev_die, prev_quantity = game_state.previous_bid

        if self.probabilities[prev_die] > prev_quantity + 1:
            return prev_die, prev_quantity + 1

        if self.probabilities[prev_die] < prev_quantity * 0.8:
            return prev_die, "Dudo"

        for die in map(str, range(int(prev_die) + 1, 7)):
            if self.probabilities[die] > prev_quantity:
                return die, prev_quantity

        return prev_die, "Dudo"


class MiltonMethod(BasePlayer):
    def make_bid(
        self, game_state: "GameState"
    ) -> Tuple[str, int]:  # (die, quantity) or (die, "Dudo")
        if game_state.previous_bid is None:
            return str(random.randint(5, 6)), max(1, game_state.total_dice // 3)

        prev_die, prev_quantity = game_state.previous_bid

        for die in map(str, range(int(prev_die) + 1, 7)):
            if self.probabilities[die] > prev_quantity:
                return die, prev_quantity

        if self.probabilities[prev_die] > prev_quantity - 0.9:
            return prev_die, prev_quantity + 1

        return prev_die, "Dudo"
