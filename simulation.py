from typing import Dict, List
import random
from tabulate import tabulate

class PerudoSimulation:
    
    def __init__(self, num_players):
        
        self.num_players: int  = num_players
        self.player_names: List[str] = [f'Player {player_num}' for player_num in range(self.num_players)]
        
        self.current_round: int = 0
        self.calza_successful_count: int = 0
        self.total_dice: int = num_players * 5
        
        self.possible_rolls: List[str] = ['1', '2', '3', '4', '5', '6']
        
        self.player_dice_counts: Dict[str, int] = {player_name: 5 for player_name in self.player_names}
        self.player_dice_rolls: Dict[str, list] = {player_name: [] for player_name in self.player_names}
        self.total_dice_rolls_count: Dict[str, int] = {die: 0 for die in self.possible_rolls}
        
        self.player_probabilities: Dict[str, dict] = {player_name: {} for player_name in self.player_names}
        
        self.current_bid = None
        self.dudo = False


    def roll_dice(self):
        for player_name in self.player_names:
            self.player_dice_rolls[player_name] = sorted([random.randint(1, 6) for _ in range(self.player_dice_counts[player_name])])
            
        self.total_dice_rolls_count = self.bin_dice([die for player_name in self.player_names for die in self.player_dice_rolls[player_name]])
        
        return self.player_dice_rolls
    
    def bin_dice(self, dice):
        binned_dice = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        for die in dice:
            binned_dice[str(die)] += 1
        return binned_dice
    
    def calculate_probabilities(self):
        for player_name in self.player_names:
            known_dice = self.bin_dice(self.player_dice_rolls[player_name])
            unseen_dice = self.total_dice - self.player_dice_counts[player_name]
            
            for die_face in self.possible_rolls:
                self.player_probabilities[player_name][die_face] = known_dice[die_face] + (unseen_dice * 1/6)

        return self.player_probabilities
    
    
    def make_bid(self, player_name, previous_die = None, previous_quantity = None):
        
        if previous_die is None or previous_quantity is None:
            current_die = str(random.randint(3, 6))
            current_quantity = random.randint(self.total_dice // 12, self.total_dice // 6)
            return current_die, current_quantity # reasonable starting bid
        
        else:
            if self.player_probabilities[player_name][previous_die] > previous_quantity:
                return previous_die, previous_quantity + 1
            
            for die in map(str, range(int(previous_die) + 1, 7)):
                if self.player_probabilities[player_name][die] > previous_quantity:
                    return die, previous_quantity
            
            return previous_die, "Dudo"
                    
            
        
    def check_dudo(self, current_player_name, previous_player_name, previous_die, previous_quantity):
        if self.total_dice_rolls_count[previous_die] >= previous_quantity:
            self.player_dice_counts[previous_player_name] -= 1
            print(f"There was {self.total_dice_rolls_count[previous_die]} {previous_die}'s, {previous_player_name} loses a die!")
            if self.player_dice_counts[previous_player_name] == 0:
                self.num_players -= 1
                print(f"{previous_player_name} is out of the game!")

        else:
            self.player_dice_counts[current_player_name] -= 1
            print(f"There was {self.total_dice_rolls_count[previous_die]} {previous_die}'s, {current_player_name} loses a die!")
            if self.player_dice_counts[current_player_name] == 0:
                self.num_players -= 1
                print(f"{current_player_name} is out of the game!")

        
    
    def check_calza(self, current_bid):
        pass
    
        
    def play_round(self):
        self.roll_dice()
        self.calculate_probabilities()
        
        i = 0
        previous_die, previous_quantity = None, None
        
        while self.dudo == False:
            self.display_round()
            i = i % self.num_players
            current_player_name = self.player_names[i]
            current_die, current_quantity = self.make_bid(current_player_name, previous_die, previous_quantity)
            self.current_bid = (current_die, current_quantity)
            if current_quantity == 'Dudo':
                self.dudo = True
                self.check_dudo(current_player_name, previous_player_name, previous_die, previous_quantity)
            else:
                i += 1
                previous_player_name, previous_die, previous_quantity = current_player_name, current_die, current_quantity
        
        
    def display_round(self):
        table_data = [
            [player, self.player_dice_rolls[player], self.player_dice_counts[player]]
            for player in self.player_names
        ]

        print(f"Round {self.current_round + 1}")
        print("-" * 40)

        headers = ["Player", "Dice Rolls", "Remaining Dice"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

        print()
        if self.current_bid:
            print(f"Current Bid: {self.current_bid[1]} dice showing {self.current_bid[0]}")
        else:
            print("No bids yet.")
        print("-" * 40)


        
        
    
    
    
sim = PerudoSimulation(num_players=6)
sim.play_round()

print('Probabilities:')
print(sim.player_dice_rolls)
for player in sim.player_names:
    print(player, sim.player_probabilities[player])

    