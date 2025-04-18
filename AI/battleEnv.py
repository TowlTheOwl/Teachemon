import os
import csv
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class BattleGymEnv(gym.Env):
    def __init__(self):
        super().__init__()

        # load card data
        file_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'TeachemonData - Teachemon.csv')
        with open(file_path, 'r') as file:
            teachemon_data = []
            csvfile = csv.DictReader(file) # reads data file for teachemon
            for row in csvfile:
                teachemon_data.append(row)
        self.teachemon_data = teachemon_data

        self.max_hp = 100
        self.max_speed = 5
        self.max_cost = 10

        
        # initialize selected cards
        self.p1_cards = [1, 2, 3, 4]
        self.p2_cards = [1, 2, 3, 4] # 1 thorugh 59
        random.shuffle(self.p1_cards)
        random.shuffle(self.p2_cards)

        # initialize player hps (all teachemon have 100 hp to begin with)
        self.p1_hps = [100, 100, 100, 100]
        self.p2_hps = [100, 100, 100, 100]
        self.all_hps = (self.p1_hps, self.p2_hps)

        # initialize item effects (no effects at the start)
        self.p1_effects = [0, 0]
        self.p2_effects = [0, 0]
        self.all_effects = (self.p1_effects, self.p2_effects)

        # initialize teachemon energies (all have 10 to begin with, gain 1 per turn)
        self.energies = [[10, 10, 10, 10], [10, 10, 10, 10]]

        # both players start with the first card in their deck
        self.curr_cards = [0, 0]


        # define actions space
        # 0-2: use moves 1/2/3
        # 3-5: use items 1/2/3
        # 6-9: swap to cards 1/2/3/4
        # 3+3+4 = 10 total moves
        self.action_space = spaces.Discrete(10)

        # define observation space
        # [selected card (one-hot len=4), hps (len=4), energies (len=4), card infos(9 per card * 4 cards = 36 len), attack potion active] * 2 (same for other) = 98 action space
        # 9 spaces for card data of one card 
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(98,), dtype=np.float32)

        self.last_actions = (None,None) # stores user actions for rendering
        self.num_to_action = {
            0: "Move 1",
            1: "Move 2",
            2: "Move 3",
            3: "Item 1",
            4: "Item 2",
            5: "Item 3",
            6: "Switch to Teachemon 1",
            7: "Switch to Teachemon 2",
            8: "Switch to Teachemon 3",
            9: "Switch to Teachemon 4",
        }

        self.reset()

    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self.np_random, _ = gym.utils.seeding.np_random(seed)
        
        # Reset game state
        self.done = False
        # initialize selected cards
        self.p1_cards = [1, 2, 3, 4]
        self.p2_cards = [1, 2, 3, 4] # 1 thorugh 59
        random.shuffle(self.p1_cards)
        random.shuffle(self.p2_cards)

        # initialize player hps (all teachemon have 100 hp to begin with)
        self.p1_hps = [100]*4
        self.p2_hps = [100]*4
        self.all_hps = (self.p1_hps, self.p2_hps)

        # initialize item effects (no effects at the start)
        self.p1_effects = [0, 0]
        self.p2_effects = [0, 0]
        self.all_effects = (self.p1_effects, self.p2_effects)

        # initialize teachemon energies (all have 10 to begin with, gain 1 per turn)
        self.energies = [[10]*4, [10]*4]

        # both players start with the first card in their deck
        self.curr_cards = [0, 0]

        return self._get_observation(0), {}

    def _get_observation(self, player_num):
        def get_player_obs(cards, hps, energies, curr_card_idx, effects):
            # selected card (one-hot)
            selected = [0] * 4
            selected[curr_card_idx] = 1

            # HPs normalized
            norm_hps = [hp / self.max_hp for hp in hps]

            # energies normalized
            norm_energies = [e / 10.0 for e in energies]

            # flatten teachmon info
            teachemon_info = []
            for card_id in cards:
                card_data = self.teachemon_data[card_id-1]
                # normalize values
                teachemon_info.extend([
                    int(card_data["Move 1 Damage"]) / self.max_hp,
                    int(card_data["Move 1 Speed"]) / self.max_speed,
                    int(card_data["Move 1 Cost"]) / self.max_cost,
                    int(card_data["Move 2 Damage"]) / self.max_hp,
                    int(card_data["Move 2 Speed"]) / self.max_speed,
                    int(card_data["Move 2 Cost"]) / self.max_cost,
                    int(card_data["Move 3 Damage"]) / self.max_hp,
                    int(card_data["Move 3 Speed"]) / self.max_speed,
                    int(card_data["Move 3 Cost"]) / self.max_cost,
                ])
            
            potion_active = effects[0] / 3

            return selected + norm_hps + norm_energies + teachemon_info + [potion_active]
        
        p1_obs = get_player_obs(self.p1_cards, self.p1_hps, self.energies[0], self.curr_cards[0], self.p1_effects)
        p2_obs = get_player_obs(self.p2_cards, self.p2_hps, self.energies[1], self.curr_cards[1], self.p2_effects)

        if player_num == 0:
            return np.array(p1_obs + p2_obs, dtype=np.float32)
        elif player_num == 1:
            return np.array(p2_obs + p1_obs, dtype=np.float32)
    
    def get_action_mask(self, player_idx):
        mask = [1] * 10 # assume all valid to start

        curr_idx = self.curr_cards[player_idx]
        curr_card_id = self.p1_cards[curr_idx] if player_idx == 0 else self.p2_cards[curr_idx]
        curr_hp = self.p1_hps[curr_idx] if player_idx == 0 else self.p2_hps[curr_idx]
        energy = self.energies[player_idx][curr_idx]
        card_data = self.teachemon_data[curr_card_id - 1]

        # Moves 0-2
        for move in range(3):
            cost = int(card_data[f"Move {move + 1} Cost"])
            if curr_hp <= 0 or energy < cost:
                mask[move] = 0

        # Moves 3-5
        for item in range(3):
            if curr_hp <= 0:
                mask[3 + item] = 0

        # Swaps 6-9
        hps = self.p1_hps if player_idx == 0 else self.p2_hps
        for i in range(4):
            if hps[i] <= 0 or i == curr_idx:
                mask[6 + i] = 0

        return np.array(mask, dtype=np.bool_)

    def _cast_ability(self, player_idx:int, card_data:dict, ability_idx:int, opp_curr_card: int, opp_hps:list):
        # cast the selected ability, calculate damage
        opp_idx = (player_idx+1)%2
        damage = int(card_data[f"Move {ability_idx + 1} Damage"])
        if self.all_effects[player_idx][0] > 0:     # check for player attack potion effect
            damage *= 1.5
        
        if self.all_effects[opp_idx][1] > 0:    # check for opponent defense potion effect
            damage = max(damage-30, 0)
        
        self.energies[player_idx][self.curr_cards[player_idx]] -= int(card_data[f"Move {ability_idx + 1} Cost"])
        damage_dealt = min(damage, opp_hps[opp_curr_card])
        opp_hps[opp_curr_card] -= damage_dealt
        if opp_hps[opp_curr_card] < 0:
            opp_hps[opp_curr_card] = 0
        
        return damage_dealt
        
    def step(self, actions:list):
        action_p1, action_p2 = actions
        self.last_actions = actions
        
        if self.done:
            return self._get_observation(0), [0, 0], self.done, {}

        """
        0: move 1
        1: move 2
        2: move 3
        3: item 1
        4: item 2
        5: item 3
        6: swap to 1
        7: swap to 2
        8: swap to 3
        9: swap to 4

        """

        curr_cards_data = (self.teachemon_data[self.p1_cards[self.curr_cards[0]]-1], self.teachemon_data[self.p2_cards[self.curr_cards[1]]-1])

        # handle actions
        moved = [False, False]
        if self.p1_hps[self.curr_cards[0]] <= 0:
            moved[0] = True  # skip action
        if self.p2_hps[self.curr_cards[1]] <= 0:
            moved[1] = True  # skip action

        # swap occurs first
        if not all(moved):
            for i in range(2):
                if actions[i] > 5: # 6-9 (swap)
                    self.curr_cards[i] = actions[i] - 6
                    moved[i] = True
        
        
        # items are used
        if not all(moved):
            for i in range(2):
                if not moved[i]:
                    if actions[i] > 2: # must be 3-5, as if greater, already moved
                        if actions[i] == 3:
                            self.all_effects[i][0] = 3
                        elif actions[i] == 4:
                            self.all_effects[i][1] = 1
                        else:
                            self.energies[i][self.curr_cards[i]] = min(10, self.energies[i][self.curr_cards[i]] + 1)
                        moved[i] = True
        
        # abilities are cast
        p1_damage_dealt = 0
        p2_damage_dealt = 0
        if not all(moved):
            if action_p1 < 3 and action_p2 < 3:
                p1_speed = int(curr_cards_data[0][f"Move {action_p1+1} Speed"])
                p2_speed = int(curr_cards_data[1][f"Move {action_p2+1} Speed"])

                if p1_speed > p2_speed or (p1_speed == p2_speed and random.randint(0, 1) == 0):
                    p1_damage_dealt = self._cast_ability(0, curr_cards_data[0], action_p1, self.curr_cards[1], self.p2_hps)
                    if self.p2_hps[self.curr_cards[1]] > 0:
                        p2_damage_dealt = self._cast_ability(1, curr_cards_data[1], action_p2, self.curr_cards[0], self.p1_hps)
                else:
                    p2_damage_dealt = self._cast_ability(1, curr_cards_data[1], action_p2, self.curr_cards[0], self.p1_hps)
                    if self.p1_hps[self.curr_cards[0]] > 0:
                        p1_damage_dealt = self._cast_ability(0, curr_cards_data[0], action_p1, self.curr_cards[1], self.p2_hps)
            elif action_p1 < 3:
                p1_damage_dealt = self._cast_ability(0, curr_cards_data[0], action_p1, self.curr_cards[1], self.p2_hps)
            elif action_p2 < 3:
                p2_damage_dealt = self._cast_ability(1, curr_cards_data[1], action_p2, self.curr_cards[0], self.p1_hps)


        # update effects & energy
        self.p1_effects[0] = max(0, self.p1_effects[0]-1)
        self.p2_effects[0] = max(0, self.p2_effects[0]-1)
        self.p1_effects[1] = 0
        self.p2_effects[1] = 0
        self.energies[0] = [min(e + 1, 10) for e in self.energies[0]]
        self.energies[1] = [min(e + 1, 10) for e in self.energies[1]]

        self.done = all(hp <= 0 for hp in self.p1_hps) or all(hp <= 0 for hp in self.p2_hps)
        rewards = [0, 0]

        if self.done:
            if all(hp <= 0 for hp in self.p2_hps):
                rewards = [100, -100]
            else:
                rewards = [-100, 100]
        
        rewards[0] += p1_damage_dealt/2
        rewards[1] += p2_damage_dealt/2

        info = {"action_masks": [self.get_action_mask(0), self.get_action_mask(1)]}

        return self._get_observation(0), rewards, self.done, False, info
    
    def render(self, mode='human'):
        print("=" * 50)
        print(" Teachemon Battle ")
        print(f"Done: {self.done}")
        print()
        print(f"Player 1 Action: {self.num_to_action[int(self.last_actions[0])]}")
        print(f"Player 2 Action: {self.num_to_action[int(self.last_actions[1])]}")
        print()

        for player_id in [0, 1]:
            print(f"Player {player_id + 1}")
            cards = self.p1_cards if player_id == 0 else self.p2_cards
            hps = self.p1_hps if player_id == 0 else self.p2_hps
            energies = self.energies[player_id]
            effects = self.p1_effects if player_id == 0 else self.p2_effects
            curr = self.curr_cards[player_id]

            for idx, card_id in enumerate(cards):
                active = " (Active)" if idx == curr else ""
                hp = hps[idx]
                energy = energies[idx]
                print(f"  Card {idx + 1}: ID={card_id} | HP={hp} | Energy={energy}{active}")

            print(f"Effects: AttackPotion={effects[0]}")
            print()

        print("=" * 50)

env = BattleGymEnv()