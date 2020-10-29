import csv

class AreaMap:

    def __init__(self):
        self.area_floorplan = []

        with open('./mapdata.csv', 'r', newline='') as f:
            f_reader=csv.reader(f, delimiter=',')
            for line in f_reader:
                self.area_floorplan.append(line)

        self.area_dimensions = [len(self.area_floorplan), len(self.area_floorplan[0])]
        # NOTE: rows, columns (y, x!)

        self.valid_character_positions = []

        for row in range(self.area_dimensions[0]):
            for column in range(self.area_dimensions[1]):
                if int(self.area_floorplan[row][column]) == 0:
                    self.valid_character_positions += [[column, row]]

    def get_area_floorplan(self):
        return self.area_floorplan

    def get_area_dimensions(self):
        return self.area_dimensions

    def get_valid_character_positions(self):
        return self.valid_character_positions

class Character:

    def __init__(self, character_type, position, hp, dp, sp, has_key):
        self.character_type = character_type
        self.position = position
        self.hp = hp
        self.dp = dp
        self.sp = sp
        self.has_key = has_key

    def set_position(self, alteration):
        self.position[0] += alteration[0]
        self.position[1] += alteration[1]

    def get_position(self):
        return self.position

    def get_type(self):
        return self.character_type

    def get_stats(self):
        return self.hp, self.dp, self.sp

    def set_hp(self, hp):
        self.hp = hp

class Hero(Character):

    def __init__(self):
        super().__init__("Hero", [1, 1], 10, 6, 3, False)
        self.level = 1
        self.max_hp = 10

    def get_level(self):
        return self.level

    def get_max_hp(self):
        return self.max_hp
