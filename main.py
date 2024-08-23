import pygame 
import random
import json

# Цвета для интерфейса и плиток
BACKGROUND = (252, 247, 241)
BOARD_BACKGROUND = (186, 174, 164)

TILE_2_4_TEXT = (118, 111, 102)
EMPTY_TILE = (205, 193, 181)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Цвета плиток по значениям
COLORS={2:    (238,228,218),
        4:    (237,224,202),
        8:    (242,177,121),
        16:   (245, 149, 101),
        32:   (245,124, 95),
        64:   (246,93, 59),
        128:  (237, 206, 113),
        256:  (237,204, 99),
        512:  (237, 200, 80),
        1024: (237, 197, 63) ,
        2048: (238, 194, 46)
        }

# Цвет для выигрышного экрана
WIN_COLOR = (237,198,8)
LOSE_COLOR = COLORS[16]

# Настройки размера поля и плиток
SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * TILE_MARGIN
DIFF = 400
HEIGHT = WIDTH + DIFF
WIN_SCORE = 2048

# Прямоугольник кнопки "Попробовать снова"
rect_rest = pygame.Rect(130, 95, 310,30)


# Функция для сохранения статистики игры
def save_statistics(board, score, best_score):
    statistics = {
        'board': board,
        'score': score,
        'best_score': best_score
    }
    with open('statistics.json', 'w') as file:
        json.dump(statistics, file)
    

# Функция для загрузки статистики игры
def load_statistics():
    try:
        with open('statistics.json', 'r') as file:
            statistics = json.load(file)
            board = statistics['board']
            score = statistics['score']
            best_score = statistics['best_score']
            return board, score, best_score
    except FileNotFoundError:
        return None, None, 0 


# Инициализация Pygame
pygame.init()

# Загрузка иконок
icon = pygame.image.load(r'gallery\icon.png')
restart_btn_icon = pygame.image.load(r'gallery\restart.png')
restart_mini = pygame.image.load(r'gallery\restart_mini.png')

# Установка иконки и создание окна
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 by ROVA")

# Настройка шрифтов
font = pygame.font.Font(None, 48)
help_font = pygame.font.Font(None, 25)
small_font = pygame.font.Font(None, 20)
medium_font = pygame.font.Font(None, 35)
font_2048 = pygame.font.Font(None, 50)


# Функция для отрисовки игрового поля
def draw_board(board, score, best_score):
    screen.fill(BACKGROUND)

    # Отображение справочного текста
    help_text = help_font.render('Join the numbers and get to the 2048 tile!', True, BOARD_BACKGROUND)

    # Отображение текста "2048"
    text_2048 = font_2048.render('2048', True, BACKGROUND)
    rect_2048 = pygame.Rect(TILE_MARGIN, 25, 100,100)
    r_2048 = text_2048.get_rect(center=rect_2048.center)
    pygame.draw.rect(screen, COLORS[WIN_SCORE], rect_2048)

    # Отображение текущего счета
    score_text = small_font.render('SCORE', True, COLORS[4])
    score_int = medium_font.render(f'{score}', True, BACKGROUND)
    rect_score = pygame.Rect(130, 25, 150,60)
    r_score = score_int.get_rect(center=rect_score.center)
    pygame.draw.rect(screen, BOARD_BACKGROUND, rect_score)

    # Отображение лучшего счета
    best_text = small_font.render('BEST', True, COLORS[4])
    best_int = medium_font.render(f'{best_score}', True, BACKGROUND)
    rect_best = pygame.Rect(WIDTH - 10 - 150, 25, 150,60)
    r_best = best_int.get_rect(center=rect_best.center)
    pygame.draw.rect(screen, BOARD_BACKGROUND, rect_best) 

    # Отображение кнопки "Попробовать снова"
    rest_text = medium_font.render('TRY AGAIN', True, BACKGROUND)
    r_rest = rest_text.get_rect(center=rect_rest.center)
    pygame.draw.rect(screen, COLORS[16], rect_rest)

    # Рендеринг текста и кнопок
    screen.blit(text_2048, r_2048)
    screen.blit(score_text, (180,30))
    screen.blit(score_int, r_score)
    screen.blit(best_text, (350, 30))
    screen.blit(best_int, r_best)
    screen.blit(rest_text, r_rest)
    screen.blit(help_text, (TILE_MARGIN, 155))

    # Отрисовка фона игрового поля
    board_back = pygame.Rect(0, DIFF//2, WIDTH, WIDTH)
    pygame.draw.rect(screen, BOARD_BACKGROUND, board_back)

    # Отображение плиток на игровом поле
    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            color = COLORS.get(value, EMPTY_TILE)
            rect = pygame.Rect(
                col * TILE_SIZE + (col+1) * TILE_MARGIN,
                row * TILE_SIZE + (row+1) * TILE_MARGIN + DIFF//2,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(screen, color, rect)
            
            if value:
                text = font.render(str(value), True, TILE_2_4_TEXT if value <= 4 else WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    
    # Обновление экрана
    pygame.display.flip()


# Функция для изменения экрана в случае выигрыша или поражения
def screen_changing(color, color_alpha, text, text_color, best_score, board):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(color_alpha) 
    overlay.fill(color)  

    # Настройка шрифта и текста для отображения
    win_font = pygame.font.Font(None, 100)
    win_text = win_font.render(text, True, text_color)
    win_text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80 ))

    # Отображение кнопки перезапуска
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 , 100, 100)
    pygame.draw.rect(screen, BLACK, button_rect)

    # Отображение наложения и текста на экране
    screen.blit(overlay, (0, 0))
    screen.blit(win_text, win_text_rect)
    screen.blit(restart_btn_icon, (WIDTH // 2 - 50, HEIGHT // 2))

    # Обновление экрана
    pygame.display.flip()

    # Обработка событий после окончания игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for r in board:
                    if WIN_SCORE in r:
                        board = [[0] * SIZE for i in range(SIZE)]
                        add_new_tile(board)
                        add_new_tile(board)
                save_statistics(board, 0, best_score) 

                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Перезапустить игру


# Функция для перемещения плиток влево
def move_left(board):
    new_board = [[0] * SIZE for i in range(SIZE)]
    delta = 0

    for row in range(SIZE):
        col_new = 0
        last = 0
        for col in range(SIZE):
            if board[row][col] != 0:
                if last == 0:
                    last = board[row][col]
                elif last == board[row][col]:
                    new_board[row][col_new] = 2 * last
                    delta += 2 * last
                    col_new += 1
                    last = 0
                else:
                    new_board[row][col_new] = last
                    col_new += 1
                    last = board[row][col]
        
        if last != 0:
            new_board[row][col_new] = last
    


    return new_board, delta


# Функция для поворота игрового поля на 90 градусов
def rotate_board(board):
    return [[board[col][row] for col in range(SIZE)] for row in range(SIZE -1, -1, -1)]


# Функция для добавления новой плитки на игровое поле
def add_new_tile(board):
    empty_tiles = [(row, col) for row in range(SIZE) for col in range(SIZE) if board[row][col] == 0]

    if empty_tiles:
        row, col = random.choice(empty_tiles)
        board[row][col] = 2 if random.random() < 0.9 else 4


# Функция проверки на проигрыш
def game_over(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                return False
            if col < SIZE -1 and board[row][col] == board[row][col + 1]:
                return False
            if row < SIZE -1 and board[row][col] == board[row + 1][col]:
                return False
    
    return True


# Функция проверки на выигрыш
def is_win(board, score, best_score):
    for r in board:
        if WIN_SCORE in r:
            draw_board(board, score, best_score)  
            screen_changing(color=WIN_COLOR, color_alpha=120, text="You Win!", text_color=WHITE, best_score=best_score, board=board)
            return [[0] * SIZE for i in range(SIZE)]


# Главная функция  
def main():
    board, score, best_score = load_statistics()
    if board is None:
        board = [[0] * SIZE for _ in range(SIZE)]
        add_new_tile(board)
        add_new_tile(board)
        score = 0

    running = True
    
    while running:
        draw_board(board, score, best_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_statistics(board, score, best_score) 
                running = False
            elif event.type == pygame.KEYDOWN:
                
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    board, delta = move_left(board)
                
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board, delta = move_left(board)
                    board = rotate_board(board)
                    board = rotate_board(board)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board, delta = move_left(board)
                    board = rotate_board(board)
 
                elif event.key in (pygame.K_UP, pygame.K_w):
                    board = rotate_board(board)
                    board, delta = move_left(board)
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board = rotate_board(board)

                score += delta
                if score > best_score:
                    best_score = score

                rest = is_win(board, score, best_score)
                if rest:
                    board = rest
                    score = 0
                    add_new_tile(board)
                add_new_tile(board) 

                if game_over(board):
                    board = [[0] * SIZE for _ in range(SIZE)]
                    add_new_tile(board)
                    add_new_tile(board)
                    screen_changing(color=LOSE_COLOR, color_alpha=120, text='Game over!', text_color=WHITE, best_score=best_score, board=board)
                    score = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if rect_rest.collidepoint(pos):
                    board = [[0] * SIZE for _ in range(SIZE)]
                    add_new_tile(board)
                    add_new_tile(board)
                    score = 0
                    draw_board(board, score, best_score)
                
                restart_button_rect = pygame.Rect(WIDTH - 100, HEIGHT - 90, 80, 80)
                if restart_button_rect.collidepoint(pos):
                    board = [[0] * SIZE for _ in range(SIZE)]
                    add_new_tile(board)
                    add_new_tile(board)
                    score = 0
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()