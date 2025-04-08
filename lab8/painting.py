import pygame

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Paint")
CLOCK = pygame.time.Clock()

# Создаём отдельную поверхность для рисования (холст)
canvas = pygame.Surface(screen.get_size())
canvas.fill((255, 255, 255))

# Загрузка изображений значков
image_rectangle = pygame.image.load("C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/images/rectangle.png")
image_circle = pygame.image.load("C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/images/circle.png")

# Установка позиций для значков
rectangle_rect = image_rectangle.get_rect(topleft=(10, 10))
circle_rect = image_circle.get_rect(topleft=(rectangle_rect.right + 10, 10))

# Установка палитры цветов
color_palette = [
    (0, 0, 0),       # Black
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (255, 255, 255), # White
]

palette_rects = []
for i, color in enumerate(color_palette):
    rect = pygame.Rect(10 + i * 40, 60, 30, 30)  # Positions of color blocks
    palette_rects.append((rect, color))

running = True
color_brush = (0, 0, 0)
brush_size = 10
prev_pos = None

# Выбранный инструмент: "brush", "rectangle", "circle", "eraser"
current_tool = "brush"
drawing = False
start_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if rectangle_rect.collidepoint(pos):
                current_tool = "rectangle"
            elif circle_rect.collidepoint(pos):
                current_tool = "circle"
            elif current_tool in ["rectangle", "circle"]:
                start_pos = pos
                drawing = True
            # Check if a color is selected
            for rect, color in palette_rects:
                if rect.collidepoint(pos):
                    color_brush = color

        if pygame.mouse.get_pressed()[0] and current_tool in ["brush", "eraser"]:
            pos = pygame.mouse.get_pos()
            if not (rectangle_rect.collidepoint(pos) or circle_rect.collidepoint(pos)):
                color = (255, 255, 255) if current_tool == "eraser" else color_brush
                if prev_pos is not None:
                    pygame.draw.line(canvas, color, prev_pos, pos, brush_size * 2)
                prev_pos = pos
        else:
            prev_pos = None

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            end_pos = event.pos
            if start_pos and end_pos:
                x1, y1 = start_pos
                x2, y2 = end_pos
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                top_left = (min(x1, x2), min(y1, y2))

                if current_tool == "rectangle":
                    pygame.draw.rect(canvas, color_brush, (*top_left, width, height), 2)
                elif current_tool == "circle":
                    radius = max(width, height) // 2
                    center = (x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)
                    pygame.draw.circle(canvas, color_brush, center, radius, 2)

            drawing = False
            start_pos = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                current_tool = "brush"
            elif event.key == pygame.K_e:
                current_tool = "eraser"
            elif event.key == pygame.K_1:
                color_brush = (0, 0, 0)       # Black
            elif event.key == pygame.K_2:
                color_brush = (0, 255, 0)     # Green
            elif event.key == pygame.K_3:
                color_brush = (0, 0, 255)     # Blue
            elif event.key == pygame.K_4:
                color_brush = (255, 0, 0)     # Red
            elif event.key == pygame.K_5:
                color_brush = (255, 255, 0)   # Yellow

    # Отображаем холст
    screen.blit(canvas, (0, 0))

    # Отображаем значки
    screen.blit(image_rectangle, rectangle_rect)
    screen.blit(image_circle, circle_rect)

    # Отображаем палитру цветов
    for rect, color in palette_rects:
        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()