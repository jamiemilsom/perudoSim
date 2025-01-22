from typing import Dict, List, Optional, Tuple
from tabulate import tabulate
from player_classes import BasePlayer, ConservativeStrat, MiltonMethod

PRINT_GAME_INFO = False
ANONOMISE_DICE = False


class GameState:
    def __init__(self):
        self.previous_bid: Optional[Tuple[str, int]] = None  # (die, quantity) or None
        self.total_dice: int = 0
        self.current_roll_counts: Dict[str, int] = {}  # {die face: count, ... }
        self.round: int = 1


class PerudoGame:
    def __init__(self, players: List[BasePlayer]):
        self.players = players
        self.state = GameState()
        self.state.total_dice = sum(player.dice_count for player in players)

    def play_round(self) -> None:

        for player in self.players:
            player.roll_dice()

        all_dice = [die for player in self.players for die in player.dice]
        self.state.current_roll_counts = BasePlayer.bin_dice(all_dice)

        for player in self.players:
            player.calculate_probabilities(self.state.total_dice)

        if PRINT_GAME_INFO:
            self.display_game_state()

        current_player_idx = 0
        self.state.previous_bid = None

        while True:
            current_player = self.players[current_player_idx]

            if current_player.dice_count > 0:
                die, quantity = current_player.make_bid(self.state)

                if quantity == "Dudo":
                    self.handle_dudo(current_player)
                    break
                else:
                    if PRINT_GAME_INFO:
                        print(
                            f"{current_player.name} bids: {quantity} dice showing {die}"
                        )
                    self.state.previous_bid = (die, quantity)

            current_player_idx = (current_player_idx + 1) % len(self.players)

    def handle_dudo(self, doubting_player: BasePlayer) -> None:

        prev_die, prev_quantity = self.state.previous_bid
        actual_count = self.state.current_roll_counts[prev_die]

        if PRINT_GAME_INFO:
            print(f"\nDudo called! Actual count of {prev_die}s: {actual_count}")
            print("All dice:", {player.name: player.dice for player in self.players})

        prev_player_idx = (self.players.index(doubting_player) - 1) % len(self.players)
        while self.players[prev_player_idx].dice_count == 0:
            prev_player_idx = (prev_player_idx - 1) % len(self.players)
        previous_player = self.players[prev_player_idx]

        if actual_count >= prev_quantity:
            doubting_player.lose_die()
            if PRINT_GAME_INFO:
                print(f"{doubting_player.name} loses a die!")
        else:
            previous_player.lose_die()
            if PRINT_GAME_INFO:
                print(f"{previous_player.name} loses a die!")

        self.state.total_dice = sum(player.dice_count for player in self.players)

    def display_game_state(self) -> None:
        table_data = [
            [
                player.name,
                (
                    player.dice
                    if not PRINT_GAME_INFO and not ANONOMISE_DICE
                    else ["?" * len(player.dice)]
                ),
                player.dice_count,
            ]
            for player in self.players
        ]
        print(f"\nRound {self.state.round}")
        print(
            tabulate(table_data, headers=["Player", "Dice", "Count"], tablefmt="pretty")
        )

    def play_game(self) -> BasePlayer:
        while sum(1 for player in self.players if player.dice_count > 0) > 1:
            self.play_round()
            self.state.round += 1

        winner = next(player for player in self.players if player.dice_count > 0)
        if PRINT_GAME_INFO:
            print(f"\nGame Over! {winner.name} wins!")
        return winner


def simulate_games(n_games: int, player_types: List[type]) -> Dict[str, int]:
    wins = {player_type.__name__: 0 for player_type in player_types}

    for game_num in range(n_games):
        players = [
            player_type(f"{player_type.__name__}_{i}")
            for i, player_type in enumerate(player_types)
        ]
        game = PerudoGame(players)
        winner = game.play_game()
        wins[winner.__class__.__name__] += 1

        if game_num == n_games - 1:
            print(f"\nAfter {game_num + 1} games:")
            for player_type, win_count in wins.items():
                print(
                    f"{player_type}: {win_count} wins ({win_count/(game_num+1)*100:.1f}%)"
                )

    return wins


simulate_games(
    10000, [ConservativeStrat, MiltonMethod, ConservativeStrat, MiltonMethod]
)
