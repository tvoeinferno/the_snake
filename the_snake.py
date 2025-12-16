from random import randint

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Docsting для GameObject"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None  # Цвет - это аргумент init

    def draw(self):
        """Метод draw для GameObject"""
        pass


class Apple(GameObject):
    """Docstring для Apple"""

    def __init__(self, occupy_positions=[]):
        # Я вроде бы правильно тебя понял и добавил сюда аргумент
        # Который по умолчанию как пустой список и передаю его
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupy_positions)  # Вот сюда

    def draw(self):
        """Метод draw для Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, positions):
        """Метод для определения позиции яблока"""
        while self.position in positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Docstring для Snake"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1   # Решил не удалять длину,
        # а удалил её из самого метода reset
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [
            # Не понял, как это реализовано в 46 строке,
            # решил сделать через рандом
            # Можно конечно сделать что-то фиксированное,
            # но рандом как по мне интереснее
            (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)]
        # self.position = self.positions[0]
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод сброса змейки"""
        self.__init__()
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод draw класса Snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Это прекод, я думаю его не обязательно менять.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод движения змеи"""
        self.update_direction()
        # Не совсем понял почему тут лишний вызов метода.
        # Его конечно можно добавить в main
        # Но не будет лучше оставить его тут, так как
        # move как раз таки отвечает за движение змеики?
        new_head_x, new_head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head_x = (new_head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH
        new_head_y = (new_head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT

        self.position = (new_head_x, new_head_y)

        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Метод вычисления позиции головы"""

        return self.positions[0]


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:   # Это прекод, зачем его менять?
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    pygame.init()
    # Передаю позицию змеи непосредственно в вызовах функции,
    # не понимаю, как в Apple() передать snake.position?
    # И нужно ли это в текущей реализации?
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
