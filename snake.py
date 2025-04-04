import pygame
import sys
import random
import time

pygame.init()  # Инициализация всех модулей Pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600  # Размеры игрового экрана
BLOCK_DIM = 40  # Размер одного блока (клетки)
FONT = pygame.font.Font(None, BLOCK_DIM * 2)  # Шрифт для отображения текста

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Создание окна с заданными размерами
pygame.display.set_caption("Snake Game")  # Заголовок окна
clock = pygame.time.Clock()  # Часы для контроля частоты кадров

class Snake:
    def __init__(self):
        self.reset()  # Вызов метода для сброса начальных параметров змеи

    def reset(self):
        self.x, self.y = BLOCK_DIM, BLOCK_DIM  # Начальные координаты головы змеи
        self.x_direction = 1  # Направление движения змеи по оси X
        self.y_direction = 0  # Направление движения змеи по оси Y
        self.head = pygame.Rect(self.x, self.y, BLOCK_DIM, BLOCK_DIM)  # Прямоугольник, представляющий голову змеи
        self.body = [pygame.Rect(self.x - BLOCK_DIM, self.y, BLOCK_DIM, BLOCK_DIM)]  # Тело змеи, включающее один сегмент
        self.dead = False  # Флаг, показывающий, мертва ли змея

    def update(self):
        if not (0 <= self.head.x < SCREEN_WIDTH and 0 <= self.head.y < SCREEN_HEIGHT):  # Проверка на выход за границы экрана
            self.reset()  # Если змея вышла за пределы экрана, сбросить игру

        for segment in self.body:  # Проверка на столкновение головы с телом
            if self.head.x == segment.x and self.head.y == segment.y:
                self.reset()  # Если столкновение, сбросить игру

        self.body.append(self.head.copy())  # Добавляем новый сегмент в конец тела змеи
        self.head.x += self.x_direction * BLOCK_DIM  # Обновляем координаты головы по оси X
        self.head.y += self.y_direction * BLOCK_DIM  # Обновляем координаты головы по оси Y
        self.body.pop(0)  # Удаляем последний сегмент тела, чтобы змея не росла бесконечно

class Food:
    def __init__(self):
        self.spawn()  # Генерация еды при создании объекта

    def spawn(self):
        self.x = random.randint(0, (SCREEN_WIDTH // BLOCK_DIM) - 1) * BLOCK_DIM  # Случайные координаты для еды по оси X
        self.y = random.randint(0, (SCREEN_HEIGHT // BLOCK_DIM) - 1) * BLOCK_DIM  # Случайные координаты для еды по оси Y
        self.rect = pygame.Rect(self.x, self.y, BLOCK_DIM, BLOCK_DIM)  # Прямоугольник для еды
        self.color = random.choice(["red", "orange"])  # Случайный цвет еды (красный или оранжевый)
        self.weight = -1 if self.color == "red" else 2  # Вес еды: красная еда уменьшает размер змеи, оранжевая увеличивает
        self.spawn_time = time.time()  # Засекаем время появления еды

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)  # Отрисовываем еду на экране

    def is_expired(self):
        return time.time() - self.spawn_time > 6  # Проверка на истечение времени жизни еды (6 секунд)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_DIM):  # Проходим по всем горизонтальным линиям
        for y in range(0, SCREEN_HEIGHT, BLOCK_DIM):  # Проходим по всем вертикальным линиям
            rect = pygame.Rect(x, y, BLOCK_DIM, BLOCK_DIM)  # Рисуем клетку
            pygame.draw.rect(screen, "#444444", rect, 1)  # Отрисовываем сетку на экране

snake = Snake()  # Создаем объект змеи
food = Food()  # Создаем объект еды
speed = 5  # Начальная скорость игры

while True:
    for event in pygame.event.get():  # Обработка событий игры
        if event.type == pygame.QUIT:  # Если игрок закрыл окно
            pygame.quit()  # Завершаем работу Pygame
            sys.exit()  # Завершаем программу

        if event.type == pygame.KEYDOWN:  # Если нажата клавиша
            if event.key == pygame.K_DOWN and snake.y_direction == 0:  # Если нажата стрелка вниз
                snake.y_direction = 1  # Направляем змейку вниз
                snake.x_direction = 0  # Останавливаем движение по оси X
            elif event.key == pygame.K_UP and snake.y_direction == 0:  # Если нажата стрелка вверх
                snake.y_direction = -1  # Направляем змейку вверх
                snake.x_direction = 0  # Останавливаем движение по оси X
            elif event.key == pygame.K_RIGHT and snake.x_direction == 0:  # Если нажата стрелка вправо
                snake.y_direction = 0  # Останавливаем движение по оси Y
                snake.x_direction = 1  # Направляем змейку вправо
            elif event.key == pygame.K_LEFT and snake.x_direction == 0:  # Если нажата стрелка влево
                snake.y_direction = 0  # Останавливаем движение по оси Y
                snake.x_direction = -1  # Направляем змейку влево

    snake.update()  # Обновляем положение змеи

    if food.is_expired():  # Если еда испортилась (прошло 6 секунд)
        food.spawn()  # Генерируем новую еду

    screen.fill('black')  # Заливаем экран черным цветом
    draw_grid()  # Рисуем сетку
    food.draw()  # Отрисовываем еду

    for segment in snake.body:  # Рисуем тело змеи
        pygame.draw.rect(screen, "green", segment)  # Каждый сегмент тела змеи — зеленый

    pygame.draw.rect(screen, "blue", snake.head)  # Отрисовываем голову змеи синим

    score_text = FONT.render(f"Score: {len(snake.body)}", True, "white")  # Рисуем текст с количеством очков
    level_text = FONT.render(f"Level: {1 + len(snake.body) // 4}", True, "white")  # Рисуем текст с уровнем
    screen.blit(score_text, (20, 20))  # Отображаем очки в верхнем левом углу
    screen.blit(level_text, (20, 80))  # Отображаем уровень

    if snake.head.colliderect(food.rect):  # Если голова змеи столкнулась с едой
        snake.body.append(snake.body[-1].copy())  # Увеличиваем тело змеи
        food.spawn()  # Генерируем новую еду

    pygame.display.update()  # Обновляем экран
    clock.tick(speed + len(snake.body) // 4)  # Контролируем скорость игры
