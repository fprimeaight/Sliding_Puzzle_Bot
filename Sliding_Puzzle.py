from random import randint

class Board:
    def __init__(self):
        self.size = 4
        self.board = [['' for i in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = self.size * i + j + 1

        self.final_board_pos = [['' for i in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.final_board_pos[i][j] = self.size * i + j + 1

        self.blank_tile_pos = (3,3)

    def Display(self):
        for i in range(self.size):
            line = ''
            for j in range(self.size):
                if self.board[i][j] == 16:
                    line += '. '
                else:
                    line += str(self.board[i][j]) + ' '
            print(line)
    
    def swap(self,pos1,pos2):
        temp = self.board[pos1[1]][pos1[0]]
        self.board[pos1[1]][pos1[0]] = self.board[pos2[1]][pos2[0]]
        self.board[pos2[1]][pos2[0]] = temp

    def MoveLeft(self):
        if self.blank_tile_pos[0] < self.size - 1:
            self.swap(self.blank_tile_pos,(self.blank_tile_pos[0]+1,self.blank_tile_pos[1]))
            self.blank_tile_pos = (self.blank_tile_pos[0]+1,self.blank_tile_pos[1])

    def MoveRight(self):
        if self.blank_tile_pos[0] > 0:
            self.swap(self.blank_tile_pos,(self.blank_tile_pos[0]-1,self.blank_tile_pos[1]))
            self.blank_tile_pos = (self.blank_tile_pos[0]-1,self.blank_tile_pos[1])

    def MoveUp(self):
        if self.blank_tile_pos[1] < self.size - 1:
            self.swap(self.blank_tile_pos,(self.blank_tile_pos[0],self.blank_tile_pos[1]+1))
            self.blank_tile_pos = (self.blank_tile_pos[0],self.blank_tile_pos[1]+1)
    
    def MoveDown(self):
        if self.blank_tile_pos[1] > 0:
            self.swap(self.blank_tile_pos,(self.blank_tile_pos[0],self.blank_tile_pos[1]-1))
            self.blank_tile_pos = (self.blank_tile_pos[0],self.blank_tile_pos[1]-1)

def main():
    b = Board()
    while b.board == b.final_board_pos:
        for i in range(randint(20,100)):
            move_index = randint(0,3)
            if move_index == 0:
                b.MoveUp()
            elif move_index == 1:
                b.MoveLeft()
            elif move_index == 2:
                b.MoveDown()
            else:
                b.MoveRight()

    b.Display()
    print()

    while b.board != b.final_board_pos:
        user_input = input('Enter move: ')
        if user_input == 'w':
            b.MoveUp()
        elif user_input == 'a':
            b.MoveLeft()
        elif user_input == 's':
            b.MoveDown()
        elif user_input == 'd':
            b.MoveRight()
        else:
            print("Error: Wrong input")
        b.Display()
        
        print('Puzzle Completed!')

if __name__ == '__main__':
    main()