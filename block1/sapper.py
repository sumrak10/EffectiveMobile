# Управление в игре происходит с помощью нажатия стрелок на клавиатуре
# Для раскрытия клетки нажимается кнопка 'O' (open)
# Игра завершается с проигрышем если открывается клетка в которой находится мина
# Игра завершается выигрышем если будут открыты все клетки кроме клеток в которых находятся мины

import random
import keyboard
import os

class Cell:
    def __init__(self, mine: bool = False) -> None:
        self.around_mines_count = 0
        self.mine = mine
        self.open = False

    def __str__(self) -> str:
        if self.open:
            if self.mine:
                return '*'
            else:
                if self.around_mines_count == 0:
                    return '□'
                return str(self.around_mines_count)
        else:
            return '#'

class GamePole:
    def __init__(self, size: int, mines_count: int) -> None:
        self.pole: list[list[Cell]] = []
        self.size = size
        self.mines_count = mines_count
        self.game_over = False

        # init pole
        for i in range(size):
            row = []
            for j in range(size):
                row.append(Cell())
            self.pole.append(row)
        
        # place random mines
        for _ in range(mines_count):
            while True:
                x = random.randint(0,size-1)
                y = random.randint(0,size-1)
                if self.pole[x][y].mine == False:
                    self.pole[x][y].mine = True
                    around_coods = [[x-1,y-1],[x-1,y],[x-1,y+1],
                                    [x,y-1],           [x,y+1],
                                    [x+1,y-1],[x+1,y],[x+1,y+1]]
                    for coords in around_coods:
                        if coords[0] < 0 or coords[1] < 0:
                            continue
                        try:
                            self.pole[coords[0]][coords[1]].around_mines_count += 1
                        except IndexError:
                            pass
                    break
        
    def show(self, cx:int = None, cy:int = None) -> None:
        '''
        Отображение игрового поля в консоли
        '''
        os.system('cls')
        for x in range(self.size):
            for y in range(self.size):
                if cx is not None and cy is not None:
                    if cx == x and cy == y:
                        print(' x ', end='')
                    else:
                        print(f" {self.pole[x][y]} ", end='')
                else:
                    print(f" {self.pole[x][y]} ", end='')
            print()

    def open_cells(self, x:int, y:int) -> None:
        '''
        Рекурсивный алгоритм который открывает все клетки число мин вокруг которых равно 0
        '''
        around_coods_with_center = [[x-1,y-1],[x-1,y],[x-1,y+1],
                        [x,y-1], [x,y],  [x,y+1],
                        [x+1,y-1],[x+1,y],[x+1,y+1]]
        for coords in around_coods_with_center:
            if coords[0] < 0 or coords[1] < 0:
                continue
            try:
                cell = self.pole[coords[0]][coords[1]]
                opened_now = False
                if cell.open == False and cell.mine == False:
                    cell.open = True
                    opened_now = True
                if cell.around_mines_count == 0 and cell.mine == False and (cell.open == False or opened_now == True):
                    self.open_cells(coords[0],coords[1])
            except IndexError:
                pass

    def check_win(self) -> None:
        '''
        Метод проверяющий условия выигрыша
        '''
        count_open_cells = True
        for x in range(self.size):
            for y in range(self.size):
                if self.pole[x][y].open:
                    count_open_cells += 1
        if count_open_cells == self.size**2-self.mines_count:
            self.game_over = True
            self.show()
            print('Вы выиграли!')

    def player_turn(self, x: int, y: int) -> None:
        '''
        Метод который выполняет проверку выполненных пользователем действий
        Так же на основе этих действий происходит запуск остальных методов
        '''
        if x > self.size or y > self.size:
            print(f'Введены некорректные значения. Значения должны быть в пределах 0 < x < {self.size}')
            return None
        
        if self.pole[x][y].mine == True:
            self.game_over = True
            print('Вы наступили на мину!')
            return None
        
        self.pole[x][y].open = True
        if self.pole[x][y].around_mines_count == 0:
            self.open_cells(x,y)
        self.check_win()

if __name__ == '__main__':
    n = 10
    game = GamePole(n,12)
    cx,cy = n // 10, n // 10 
    while not game.game_over:
        game.show(cx, cy)
        key = keyboard.read_event()
        if key.event_type == 'down':
            if key.name == 'up':
                cx -= 1
            if key.name == 'down':
                cx += 1
            if key.name == 'right':
                cy += 1
            if key.name == 'left':
                cy -= 1
            if key.name == 'o':
                game.player_turn(cx,cy)
            if cx < 0:
                cx = 0
            if cy < 0:
                cy = 0
            if cx >= n:
                cx = n-1
            if cy >= n:
                cy = n-1
            print(cx,cy)
    input('Нажмите enter что закрыть программу')