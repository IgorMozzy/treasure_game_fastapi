import random
import requests
import os
class TreasureMap:
    """Представляет игровое поле с координатами сокровища"""

    def __init__(self, size):
        self.size = size
        self.treasure_x = random.randint(0, size-1)
        self.treasure_y = random.randint(0, size-1)
        # для наглядного представления создается матрица с двумя
        # дополнительными рядами букв и цифр качестве координат
        self.matrix = [['[ ]' for _ in range(size+1)] for _ in range(size+1)]
        for i in range(size):
            self.matrix[size][i] = f' {i}'.ljust(3)
            self.matrix[i][size] = f'{chr(i+65)}'
        del self.matrix[size][size]

    def check_treasure(self, x, y):
        # проверяет, является ли предположение игрока верным
        return (x == self.treasure_x) and (y == self.treasure_y)

    def get_hint(self, x, y):
        distance = abs(x - self.treasure_x) + abs(y - self.treasure_y)
        return f'Вы находитесь на расстоянии {distance} от сокровища.', min(distance, 9)

class Player:
    """Включает в себя артрибуты и логику игрока"""

    def __init__(self, size):
        self.attempts = 0
        self.choices = []  # для хранения ранее вводимых координат
        self.size = size   # ограничитель для метода choose_coordinates


    def choose_coordinates(self, string):
        # для удобства координаты вводятся в формате x - заглавная буква англ. алфавита,
        # y - цифра. x переводится в допустимое числовое значение, равное позиции в алфавите
        x, y = string.split('-')
        y = int(y)
        if 65 <= ord(x) <= 65+self.size:
            x = ord(x) - 65
        else:
            # для обработки ввода, отличного от A-Z
            raise TypeError
        if (x, y) in self.choices:
            # повторение уже используемых значений
            raise NotImplementedError
        elif not ((0 <= x < self.size) and (0 <= y < self.size)):
            # значения не должны превышать пределов поля и/или исп. как отрицательные индексы
            raise IndexError
        self.attempts += 1
        self.choices.append((x, y))
        return x, y

class Game:
    """Представляет логику игры, содержит необходимые атрибуты и метод запуска"""

    def __init__(self, size=10):
        self.map = TreasureMap(size)
        self.player = Player(self.map.size)


    def start(self, st):
        try:
            x, y = self.player.choose_coordinates(st)
        except (TypeError, ValueError, IndexError):
            buffer = 'Некорректный ввод. Следуйте шаблону!'
            return buffer, -1
        except NotImplementedError:
            buffer = f'Комбинация уже использовалась!'
            return buffer, -1
        else:
            buffer, distance = self.map.get_hint(x, y)
            if distance == 0:
                img = str(requests.get('https://shibe.online/api/cats').content)[4:-3]
                buffer = f'Поздравляем! Вы нашли сокровище на {chr(x+65)}-{y}! Количество попыток: {self.player.attempts}. Ссылка на подарочного котика: {img}'
                self.map.matrix[x][y] = f'[{distance}]'
            else:
                self.map.matrix[x][y] = f'[{distance}]'

            return buffer, distance

    def console_out(self, buffer='Игра начата! Вводите координаты в формате A-1'):
        while True:
            distance = None
            os.system('cls')
            print(buffer)
            for row in self.map.matrix:
                print(*row)
            if distance == 0:
                break
            buffer, distance = self.start(input('Введите координаты в формате A-1: '))

        input('Любую клавишу извольте')


if __name__ == '__main__':
    game = Game()
    game.console_out()
