
class Hero:
    def __init__(self, symbol, start_x, start_y):
        self.symbol = symbol
        self.x = start_x
        self.y = start_y

    # You don't have to use this if you don't want to.
    def draw_on_board(self, board):
       board[self.y][self.x] = self.symbol

class Object:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y

# You don't have to use this if you don't want to.
    def draw_on_board(self, board):
        board[self.y][self.x] = self.symbol

building = [['-','-','-','-','-','-'], ['|',' ',' ',' ',' ','|'], ['|',' ','&','&',' ','|'], ['-','-','&','&','-','-']]
class Building:
    def __init__(self, x, y):
        self.width = 6
        self.height = 4
        self.door_height = 2
        self.door_width = 2
        self.x = x
        self.y = y
    def draw_on_board(self, board):
        for row in range(self.y, self.y + 4):
            for i in range(self.x, self.x + 6):
                board[self.y][self.x] = building[0][0]
                board[self.y][i] = building[0][1]
                board[self.y+1][self.x] = building[1][0]
                board[self.y+1][self.x+5] = building[1][5]
                board[self.y+2][self.x] = building[2][0]
                board[self.y+2][self.x+2] = building[2][2]
                board[self.y+2][self.x+3] = building[2][3]
                board[self.y+2][self.x+5] = building[2][5]
                board[self.y+3][i] = building[3][0]
                board[self.y+3][self.x+2] = building[3][2]
                board[self.y+3][self.x+3] = building[3][3]

    def contains(self, x, y):
        self.index = x
        self.row = y
        if self.row in range(self.y, self.y + 4):
            if self.index in range(self.x, self.x + 6):
                return True
        return False

def print_board(board):
    for row in board:
        for spot in row:
            print(spot, end='')
        print()

def board_outline(board, height, width):
    for row in range(0, height):
        for i in range(1, width):
            board[0][0] = ' '
            board[0][i] = '-'
            board[0][width-1] = ' '
            board[row][0] = '|'
            board[row][width-1] = '|'
            board[height-1][0] = ' '
            board[height-1][i] = '-'
            board[height-1][width-1] = ' '

class Game:
    def __init__(self, input_file_name):
        self.hero = None
        self.num_objects = 0
        self.board = None
        self.buildings = []
        self.objects = []
        self.down_key = None
        self.up_key = None
        self.right_key = None
        self.left_key = None
        self.read_input_file(input_file_name)
        self.hero.draw_on_board(self.board)
        self.user_quit = False

    def read_input_file(self, input_file_name):
        self.file = open(input_file_name, "r")
        f = []
        for line in self.file:
            f.append(line)
            vals = line.split()
            if line == f[0]:
                self.width = int(vals[0])
                self.height = int(vals[1])
                self.board = [[' '] * self.width for i in range(self.height)]
                board_outline(self.board, self.height, self.width)
                continue
            elif line == f[1]:
                Hero.symbol = vals[0]
                Hero.x = int(vals[1])
                Hero.y = int(vals[2])
                self.hero = Hero(Hero.symbol, Hero.x, Hero.y)
                self.board[Hero.y][Hero.x] = Hero.symbol
            elif line == f[2]:
                self.up_key = vals[0]
            elif line == f[3]:
                self.left_key = vals[0]
            elif line == f[4]:
                self.down_key = vals[0]
            elif line == f[5]:
                self.right_key = vals[0]
            if 'o' in line:
                self.num_objects += 1
                Object.symbol = vals[1]
                Object.x = int(vals[2])
                Object.y = int(vals[3])
                self.objects.append(Object(Object.symbol, Object.x, Object.y))
                self.board[Object.y][Object.x] = Object.symbol
            if 'b' in line:
                Building.x = int(vals[1])
                Building.y = int(vals[2])
                b = Building(Building.x, Building.y)
                self.buildings.append(b)
                b.draw_on_board(self.board)
        self.file.close()

    def print_game(self):
        for row in self.board:
            for spot in row:
                print(spot, end='')
            print()

    def game_ended(self):
        return self.all_objects_collected() or self.user_quit

    def all_objects_collected(self):
        return self.num_objects == 0

    def detect_collision(self, y, x):
        self.next_index = x
        self.next_row = y
        if self.board[self.next_row][self.next_index] == "-" or self.board[self.next_row][self.next_index] == "|" or self.board[self.next_row][self.next_index] == "&":
            return True
        return False

    def detect_object(self, y, x):
        #returns True if object is going to be collected, point needs to resemble this
        if self.board[self.next_row][self.next_index] == Object.symbol:
            self.num_objects -= 1
            return True
        return False

    def run(self):
        quit_cmds = ['q', 'end', 'exit']
        while not self.game_ended():
            self.print_game()
            inp = input("Enter: ")
            if inp == self.up_key:
                if not self.detect_collision(Hero.y - 1, Hero.x):
                    self.detect_object(Hero.y - 1, Hero.x)
                    self.board[Hero.y][Hero.x] = " "
                    self.board[Hero.y - 1][Hero.x] = Hero.symbol
                    Hero.y = Hero.y - 1
            if inp == self.down_key:
                if not self.detect_collision(Hero.y + 1, Hero.x):
                    self.detect_object(Hero.y + 1, Hero.x)
                    self.board[Hero.y][Hero.x] = " "
                    self.board[Hero.y + 1][Hero.x] = Hero.symbol
                    Hero.y = Hero.y + 1
            if inp == self.right_key:
                if not self.detect_collision(Hero.y, Hero.x + 1):
                    self.detect_object(Hero.y, Hero.x + 1)
                    self.board[Hero.y][Hero.x] = " "
                    self.board[Hero.y][Hero.x + 1] = Hero.symbol
                    Hero.x = Hero.x + 1
            if inp == self.left_key:
                if not self.detect_collision(Hero.y, Hero.x - 1):
                    self.detect_object(Hero.y, Hero.x - 1)
                    self.board[Hero.y][Hero.x] = " "
                    self.board[Hero.y][Hero.x - 1] = Hero.symbol
                    Hero.x = Hero.x - 1
            if inp in quit_cmds:
                self.user_quit = True
        self.print_game()
        if self.user_quit:
            print("You are a quitter!")
        elif inp != self.up_key and inp != self.down_key and inp != self.right_key and inp != self.left_key:
                print("Invalid command")
        else:
            print("Congratulations: you've collected all of the items!")