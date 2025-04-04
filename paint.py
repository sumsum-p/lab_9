import pygame

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((600, 600))  # Создание окна размером 600x600 пикселей
clock = pygame.time.Clock()  # Устанавливаем таймер для ограничения FPS

radius = 15  # Радиус кисти/ластика
color = (0, 0, 255)  # Цвет кисти по умолчанию (синий)
draw_mode = 'free'  # Режим рисования (по умолчанию - кисть для свободного рисования)
start_pos = None  # Начальная позиция для рисования

running = True  # Флаг, управляющий циклом игры
while running:
    for event in pygame.event.get():  # Обрабатываем все события в очереди
        if event.type == pygame.QUIT:  # Если событие закрытия окна
            running = False  # Закрываем программу

        elif event.type == pygame.KEYDOWN:  # Когда нажата клавиша
            if event.key == pygame.K_ESCAPE:  # Если нажата клавиша ESC
                running = False  # Закрываем программу
            elif event.key == pygame.K_r:  # Если нажата клавиша R, устанавливаем красный цвет
                color = (255, 0, 0)
            elif event.key == pygame.K_g:  # Если нажата клавиша G, устанавливаем зеленый цвет
                color = (0, 255, 0)
            elif event.key == pygame.K_b:  # Если нажата клавиша B, устанавливаем синий цвет
                color = (0, 0, 255)
            elif event.key == pygame.K_k:  # Если нажата клавиша K, устанавливаем черный цвет
                color = (0, 0, 0)

            elif event.key == pygame.K_1:  # Если нажата клавиша 1, выбираем режим рисования прямоугольника
                draw_mode = 'rect'
            elif event.key == pygame.K_2:  # Если нажата клавиша 2, выбираем режим рисования круга
                draw_mode = 'circle'
            elif event.key == pygame.K_3:  # Если нажата клавиша 3, выбираем режим ластика
                draw_mode = 'eraser'
            elif event.key == pygame.K_4:  # Если нажата клавиша 4, выбираем режим рисования квадрата
                draw_mode = 'square'
            elif event.key == pygame.K_t:  # Если нажата клавиша T, выбираем режим рисования прямоугольного треугольника
                draw_mode = 'right_triangle'
            elif event.key == pygame.K_d:  # Если нажата клавиша D, выбираем режим рисования равностороннего треугольника
                draw_mode = 'equilateral_triangle'
            elif event.key == pygame.K_m:  # Если нажата клавиша M, выбираем режим рисования ромба
                draw_mode = 'rhombus'
            elif event.key == pygame.K_f:  # Если нажата клавиша F, выбираем режим кисти (свободное рисование)
                draw_mode = 'free'

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Когда нажата кнопка мыши
            start_pos = event.pos  # Сохраняем начальную позицию
            if event.button == 1:  # Если нажата левая кнопка мыши (кликаем для увеличения радиуса кисти)
                radius = min(200, radius + 1)  # Увеличиваем радиус кисти (не более 200)
            elif event.button == 3:  # Если нажата правая кнопка мыши (кликаем для уменьшения радиуса кисти)
                radius = max(1, radius - 1)  # Уменьшаем радиус кисти (не менее 1)

        elif event.type == pygame.MOUSEBUTTONUP:  # Когда отпущена кнопка мыши
            if start_pos is None:
                continue  # Если не было нажатия, пропускаем
            end_pos = event.pos  # Сохраняем конечную позицию

            if draw_mode == 'rect':  # Если выбран режим рисования прямоугольника
                rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))  # Вычисляем размеры прямоугольника
                pygame.draw.rect(screen, color, rect, width=2)  # Рисуем прямоугольник
            elif draw_mode == 'circle':  # Если выбран режим рисования круга
                center = start_pos  # Центр круга - начальная позиция
                radius_c = int(((end_pos[0] - center[0]) ** 2 + (end_pos[1] - center[1]) ** 2) ** 0.5)  # Вычисляем радиус круга
                pygame.draw.circle(screen, color, center, radius_c, width=2)  # Рисуем круг
            elif draw_mode == 'square':  # Если выбран режим рисования квадрата
                side_length = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))  # Вычисляем сторону квадрата
                square = pygame.Rect(start_pos, (side_length, side_length))  # Прямоугольник с равными сторонами
                pygame.draw.rect(screen, color, square, width=2)  # Рисуем квадрат
            elif draw_mode == 'right_triangle':  # Если выбран режим рисования прямоугольного треугольника
                points = [start_pos, (end_pos[0], start_pos[1]), end_pos]  # Вершины прямоугольного треугольника
                pygame.draw.polygon(screen, color, points)  # Рисуем прямоугольный треугольник
            elif draw_mode == 'equilateral_triangle':  # Если выбран режим рисования равностороннего треугольника
                height = int(abs(end_pos[0] - start_pos[0]) * (3 ** 0.5) / 2)  # Вычисляем высоту равностороннего треугольника
                points = [start_pos, (end_pos[0], start_pos[1]), (start_pos[0] + (end_pos[0] - start_pos[0]) / 2, start_pos[1] - height)]  # Вершины треугольника
                pygame.draw.polygon(screen, color, points)  # Рисуем равносторонний треугольник
            elif draw_mode == 'rhombus':  # Если выбран режим рисования ромба
                width = abs(end_pos[0] - start_pos[0])  # Ширина ромба
                height = abs(end_pos[1] - start_pos[1])  # Высота ромба
                points = [(start_pos[0] + width / 2, start_pos[1]),  # Верхняя вершина
                          (start_pos[0] + width, start_pos[1] + height / 2),  # Правая вершина
                          (start_pos[0] + width / 2, start_pos[1] + height),  # Нижняя вершина
                          (start_pos[0], start_pos[1] + height / 2)]  # Левая вершина
                pygame.draw.polygon(screen, color, points)  # Рисуем ромб
            start_pos = None  # Сбрасываем начальную позицию

        elif event.type == pygame.MOUSEMOTION:  # Когда мышь двигается
            if draw_mode in ['free', 'eraser'] and event.buttons[0]:  # Если рисуем кистью или ластиком и нажата левая кнопка мыши
                pos = event.pos  # Позиция мыши
                draw_color = (0, 0, 0) if draw_mode == 'eraser' else color  # Если ластик, рисуем черным, иначе текущим цветом
                pygame.draw.circle(screen, draw_color, pos, radius)  # Рисуем круг с радиусом кисти или ластика

    pygame.display.flip()  # Обновляем экран
    clock.tick(60)  # Ограничиваем FPS до 60

pygame.quit()  # Завершаем работу Pygame
