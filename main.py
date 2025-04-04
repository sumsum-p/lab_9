import pygame, sys  # Импортируем библиотеки pygame для создания игры и sys для выхода из программы
from pygame.locals import *  # Импортируем стандартные события и константы pygame
import random, time  # Импортируем модули random (для случайных чисел) и time (для задержек)

pygame.init()  # Инициализация pygame

FPS = 60  # Устанавливаем количество кадров в секунду
FramePerSec = pygame.time.Clock()  # Создаем объект для управления FPS

# Цвета (в формате RGB)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Параметры экрана
SCREEN_WIDTH = 400  # Ширина экрана
SCREEN_HEIGHT = 600  # Высота экрана
global SPEED  # Объявляем глобальную переменную для скорости врагов
SPEED = 5  # Начальная скорость врагов
COINS_COLLECTED = 0  # Счётчик собранных монет

# Шрифты
font = pygame.font.SysFont("Verdana", 60)  # Шрифт для текста "Game Over"
font_small = pygame.font.SysFont("Verdana", 20)  # Шрифт для отображения счёта монет
game_over = font.render("Game Over", True, BLACK)  # Текст "Game Over" для вывода в конце игры

# Фон и звуки
background = pygame.image.load("AnimatedStreet.png")  # Загрузка изображения фона
coin_sound = pygame.mixer.Sound("Coin.wav")  # Звук при сборе монеты

# Настройки окна игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Устанавливаем размер окна
DISPLAYSURF.fill(WHITE)  # Заполняем экран белым цветом
pygame.display.set_caption("Game")  # Устанавливаем название окна

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Инициализация базового класса Sprite
        self.image = pygame.image.load("Enemy (1).png")  # Загружаем изображение врага
        self.rect = self.image.get_rect()  # Получаем прямоугольник для врага
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Размещение врага в случайной позиции сверху

    def move(self):
        self.rect.move_ip(0, SPEED)  # Двигаем врага вниз по экрану с заданной скоростью
        if self.rect.top > SCREEN_HEIGHT:  # Если враг вышел за нижнюю границу экрана
            self.rect.top = 0  # Сбрасываем врага в верхнюю часть экрана
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Размещение врага в случайной позиции сверху

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Инициализация базового класса Sprite
        self.image = pygame.image.load("Player.png")  # Загружаем изображение игрока
        self.rect = self.image.get_rect()  # Получаем прямоугольник для игрока
        self.rect.center = (160, 520)  # Начальная позиция игрока

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Получаем нажатые клавиши
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:  # Если нажата клавиша "влево"
                self.rect.move_ip(-5, 0)  # Двигаем игрока влево
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:  # Если нажата клавиша "вправо"
                self.rect.move_ip(5, 0)  # Двигаем игрока вправо

# Класс монеты с различными размерами и весами
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Инициализация базового класса Sprite
        self.size = random.choice([40, 50, 60, 80])  # Случайный выбор размера монеты
        self.image = pygame.image.load("coin-removebg-preview.png")  # Загружаем изображение монеты
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # Масштабируем изображение
        self.rect = self.image.get_rect()  # Получаем прямоугольник для монеты
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, -40))  # Размещение монеты

        # Присваиваем количество очков в зависимости от размера монеты
        self.points = {40: 1, 50: 2, 60: 3, 80: 4}[self.size]

    def move(self):
        self.rect.move_ip(0, SPEED // 2)  # Двигаем монету вниз с меньшей скоростью, чем врагов
        if self.rect.top > SCREEN_HEIGHT:  # Если монета вышла за нижнюю границу экрана
            self.rect.top = random.randint(-100, -40)  # Сбрасываем монету в верхнюю часть экрана
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), self.rect.top)  # Размещение монеты в случайной позиции сверху

# Инициализация объектов игры
P1 = Player()  # Создание объекта игрока
E1 = Enemy()  # Создание объекта врага
coins = pygame.sprite.Group()  # Группа монет
for _ in range(3):  # Добавляем три монеты в игру
    new_coin = Coin()
    coins.add(new_coin)

enemies = pygame.sprite.Group()  # Группа врагов
enemies.add(E1)  # Добавляем врага в группу

all_sprites = pygame.sprite.Group()  # Группа всех объектов
all_sprites.add(P1)  # Добавляем игрока
all_sprites.add(E1)  # Добавляем врага
all_sprites.add(*coins)  # Добавляем все монеты

# Событие для увеличения скорости врагов
INC_SPEED = pygame.USEREVENT + 1  # Создаем уникальное пользовательское событие
pygame.time.set_timer(INC_SPEED, 1000)  # Устанавливаем таймер для этого события, оно будет срабатывать каждую секунду

while True:
    for event in pygame.event.get():  # Обрабатываем все события
        if event.type == INC_SPEED:  # Если сработал таймер для увеличения скорости
            SPEED += 0.5  # Увеличиваем скорость врагов
        if event.type == QUIT:  # Если игрок закрывает окно
            pygame.quit()  # Закрываем pygame
            sys.exit()  # Выход из программы

    DISPLAYSURF.blit(background, (0, 0))  # Отображаем фон на экране
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)  # Отображаем количество собранных монет
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))  # Размещаем текст с монетами в правом верхнем углу

    # Отображаем все спрайты на экране и двигаем их
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка на столкновение игрока с врагами
    if pygame.sprite.spritecollideany(P1, enemies):  # Если игрок столкнулся с врагом
        pygame.mixer.Sound('braking-a-car-in-a-tunnel-153305.mp3').play()  # Проигрываем звук аварии
        time.sleep(0.5)  # Задержка перед завершением игры
        DISPLAYSURF.fill(RED)  # Заполняем экран красным цветом
        DISPLAYSURF.blit(game_over, (30, 250))  # Выводим текст "Game Over"
        pygame.display.update()  # Обновляем экран
        for entity in all_sprites:
            entity.kill()  # Удаляем все объекты игры
        time.sleep(2)  # Задержка перед завершением игры
        pygame.quit()  # Закрываем pygame
        sys.exit()  # Выход из программы

    # Проверка на столкновение игрока с монетами
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)  # Проверка на столкновение и удаление монет
    for coin in collected_coins:
        COINS_COLLECTED += coin.points  # Добавляем очки в зависимости от размера монеты
        coin_sound.play()  # Проигрываем звук сбора монеты
        new_coin = Coin()  # Создаем новую монету
        coins.add(new_coin)  # Добавляем монету в группу
        all_sprites.add(new_coin)  # Добавляем монету в общую группу объектов

    pygame.display.update()  # Обновляем экран
    FramePerSec.tick(FPS)  # Устанавливаем количество кадров в секунду
