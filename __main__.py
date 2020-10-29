'''
*** TkWanderer Game ***
Version 1.0
by Gergo Vamosi, alias geritwo
https://github.com/geritwo

Milestone 4.: Map rendered, character moves, enemies generated and move + status display 0.1

Green Fox Academy, Zerda class, Lasers group, 2016.
'''

import model
import view

import random

class Game:
    '''
    Game controller object with main game functions.
    '''

    def __init__(self):
        self.model = model.AreaMap()
        self.characters = []

        # *** [ Movement variables, rulesets ] ***
        self.hero_heading = 'Down'
        self.movement_alterations = {'Up':[0, -1], 'Down':[0, 1], 'Left':[-1, 0], 'Right':[1, 0]}
        self.enemy_movement_keys = ['Up', 'Down', 'Left', 'Right']
        self.current_level = 1
        self.status_message = '-'

        self.game_flow_controller()

    def game_flow_controller(self):
        self.init_level()

        # *** [ TKinter Main loop: ] ***
        self.game_phase_display() # Draws everything
        self.game_keyboard_listener() # Binds kb input and executes commands
        self.view.show()

    def init_level(self):
        self.area_dimensions = self.model.get_area_dimensions()
        self.area_floorplan = self.model.get_area_floorplan()
        self.valid_character_positions = self.model.get_valid_character_positions()

        self.generate_characters()

        self.view = view.LevelDisplay(self.area_dimensions)


    def generate_characters(self):

        self.hero = model.Hero()
        self.characters.append(self.hero)

        number_of_enemies = random.randrange(3, 6)
        enemy_start_positions = []

        for i in range(number_of_enemies):
            position_index = random.randrange(len(self.valid_character_positions)-3) # Pick random pos from valid (w safety buffer - avoid out of range)
            position = self.valid_character_positions[position_index] # Set position there
            if position in enemy_start_positions or position == [1, 1]: # Check if not taken,
                position = self.valid_character_positions[position_index + 2] # if so, pick position two indexes further
            enemy_start_positions.append(position) # add position to list

            hp = 2 * self.current_level * random.randrange(1, 7)
            dp = self.current_level/2 * random.randrange(1, 7)
            sp = self.current_level * random.randrange(1, 7)

            keyholder = random.randrange(2, number_of_enemies+1)

            # Instantiate enemies, Boss first
            if i == 0: # If boss, apply stat modifiers
                hp += random.randrange(1, 7)
                dp += random.randrange(1, 7)/2
                sp += self.current_level
                self.characters.append(model.Character('Boss', enemy_start_positions[i], hp, dp, sp, has_key=False))

            else:
                if i == keyholder:
                    has_key = True
                else:
                    has_key = False
                self.characters.append(model.Character('Guard', enemy_start_positions[i], hp, dp, sp, has_key))

# *** [ Game View Controller Functions ] ***

    def game_phase_display(self):
        self.view.clear_display() # NOTE: Works without cleaning too. Maybe this spares memory?
        self.view.display_area(self.area_dimensions, self.area_floorplan)

        for character in self.characters:
            type = character.get_type()
            if type == "Hero":
                self.view.display_hero(self.hero.get_position(), self.hero_heading)
                #self.view.display_stats(character.get_level(), character.get_max_hp(), character.get_stats(), [0, 0, 0], self.status_message())
            else:
                self.view.display_enemies(type, character.get_position())


# *** [ Game keyboard IO] ***

    def game_keyboard_listener(self):
        self.view.root.bind('<Key>', self.game_command_interpreter)
        # NOTE: Later may need interpreter for other key commands.

    def game_command_interpreter(self, event):
        key_pressed = event.keysym
        movement_keys = ['Up', 'Down', 'Left', 'Right']
        actions_keys = ['space', 'q']
        if key_pressed in movement_keys:
            self.turn_and_move_hero(key_pressed)
        elif key_pressed == 'space':
            self.attack()
        elif key_pressed == 'q':
            exit()
        else:
            print('Invalid command:', key_pressed) # NOTE: Indev.

# *** [ Character movement and interaction ] ***

    def turn_and_move_hero(self, direction):
        self.hero_heading = direction # NOTE: Not writing back to model (hero object). Only view needs it.
        if self.is_way_free(self.hero, direction):
            self.hero.set_position(self.movement_alterations[direction])

        self.move_enemies()
        self.game_phase_display()

    def move_enemies(self):
        for i in range(1, len(self.characters)):
            direction = self.enemy_movement_keys[random.randint(0, 3)]
            if self.is_way_free(self.characters[i], direction) == True:
                self.characters[i].set_position(self.movement_alterations[direction])
            else:
                break  # TODO: Make movement more agile

    def attack(self, attacker, defender):
        attack_points = attacker.get_stats()[2]
        defense_ponts, defender_hp = defender.get_stats()[1], defender.get_stats()[0]
        if attack_points > defense_points:
            defender.set_hp(defender_hp - 1)
        if defender_hp == 0:
            self.characters.pop(defender)

    def is_way_free(self, character, direction):
        target_position = [0, 0] # NOTE: x, y = column, row
        map_max_x = range(self.area_dimensions[1])
        map_max_y = range(self.area_dimensions[0])

        target_position[0] = self.movement_alterations[direction][0] + character.get_position()[0]
        target_position[1] = self.movement_alterations[direction][1] + character.get_position()[1]

        if target_position[0] in map_max_x and target_position[1] in map_max_y:
            target_tile_type = int(self.area_floorplan[target_position[1]][target_position[0]])
            # NOTE: ^IDK why it becomes str.
            print(target_tile_type)
            if target_tile_type < 1:
                for i in range(0, len(self.characters)):
                    if self.characters[i].get_position() == target_position:
                        return False
                return True
            else:
                return False

# *** [ LAUNCH GAME ] ***
main = Game()
