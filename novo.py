import pygame
import sys
import random
from enum import Enum

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Batalha Naval")

# Cores
BLUE = (64, 128, 255)
DARK_BLUE = (0, 32, 96)
RED = (220, 20, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
LIGHT_BLUE = (173, 216, 230)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)

# Fontes
title_font = pygame.font.SysFont("arial", 48, bold=True)
menu_font = pygame.font.SysFont("arial", 32)
game_font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 18)

# Tamanho do tabuleiro
BOARD_SIZE = 10
CELL_SIZE = 40
BOARD_MARGIN = 50
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE

# Tipos de navios e seus tamanhos
SHIP_TYPES = {
    "Porta-aviões": 5,
    "Navio de Guerra": 4,
    "Cruzador": 3,
    "Submarino": 3,
    "Destroyer": 2
}

class GameState(Enum):
    MAIN_MENU = 0
    GAME_MODE_SELECT = 1
    SHIP_PLACEMENT = 2
    PLAYER_TURN = 3
    BOT_TURN = 4
    GAME_OVER = 5

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = 0
    
    def is_sunk(self):
        return self.hits >= self.size

class Player:
    def __init__(self, name, is_bot=False):
        self.name = name
        self.is_bot = is_bot
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.target_board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ships = []
        self.ships_placed = False
        
    def place_ship(self, ship, row, col, horizontal):
        positions = []
        for i in range(ship.size):
            r = row
            c = col
            if horizontal:
                c += i
            else:
                r += i
            
            # Verificar se está dentro do tabuleiro
            if r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE:
                return False
            
            # Verificar se não há sobreposição com outros navios
            if self.board[r][c] is not None:
                return False
            
            positions.append((r, c))
        
        # Se todas as posições são válidas, colocar o navio
        for r, c in positions:
            self.board[r][c] = ship
        
        ship.positions = positions
        self.ships.append(ship)
        return True
    
    def auto_place_ships(self):
        self.ships = []
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        for ship_name, ship_size in SHIP_TYPES.items():
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - 1)
                
                # Ajustar para não ultrapassar os limites
                if horizontal:
                    if col + ship_size > BOARD_SIZE:
                        col = BOARD_SIZE - ship_size
                else:
                    if row + ship_size > BOARD_SIZE:
                        row = BOARD_SIZE - ship_size
                
                ship = Ship(ship_name, ship_size)
                placed = self.place_ship(ship, row, col, horizontal)
        
        self.ships_placed = True
    
    def all_ships_sunk(self):
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

class Game:
    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.winner = None
        self.selected_ship = None
        self.ship_orientation = True  # True para horizontal, False para vertical
        self.placement_index = 0
    
    def start_new_game(self, pvp_mode):
        self.player1 = Player("Player 1")
        self.player2 = Player("Bot", not pvp_mode) if not pvp_mode else Player("Player 2")
        
        if not pvp_mode:
            self.player2.auto_place_ships()
        
        self.state = GameState.SHIP_PLACEMENT
        self.current_player = self.player1
        self.winner = None
        self.selected_ship = list(SHIP_TYPES.keys())[0]
        self.ship_orientation = True
        self.placement_index = 0
    
    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            if self.player2.is_bot:
                self.state = GameState.BOT_TURN
            else:
                self.state = GameState.PLAYER_TURN
        else:
            self.current_player = self.player1
            self.state = GameState.PLAYER_TURN
    
    def make_move(self, row, col):
        if self.current_player.target_board[row][col] is not None:
            return False  # Já foi feito um movimento aqui
        
        opponent = self.player2 if self.current_player == self.player1 else self.player1
        hit = opponent.board[row][col] is not None
        
        if hit:
            self.current_player.target_board[row][col] = 'hit'
            ship = opponent.board[row][col]
            ship.hits += 1
            if ship.is_sunk():
                print(f"{self.current_player.name} afundou o {ship.name}!")
        else:
            self.current_player.target_board[row][col] = 'miss'
        
        # Verificar se o jogo terminou
        if opponent.all_ships_sunk():
            self.winner = self.current_player
            self.state = GameState.GAME_OVER
            return True
        
        # Se não foi um acerto, mudar de turno
        if not hit:
            self.switch_turn()
        
        return True
    
    def bot_move(self):
        # Estratégia simples para o bot: escolher uma célula aleatória
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            
            if self.player2.target_board[row][col] is None:
                self.make_move(row, col)
                break

# Instância do jogo
game = Game()

# Funções de desenho
def draw_main_menu():
    screen.fill(DARK_BLUE)
    
    # Título
    title_text = title_font.render("BATALHA NAVAL", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Navio desenhado
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 150, 180, 300, 60))
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 240, 200, 30))
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 120, 270, 240, 30))
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 80, 300, 160, 30))
    
    # Ondas
    for i in range(20):
        pygame.draw.arc(screen, LIGHT_BLUE, 
                       (i * 50, 550, 50, 30), 
                       3.14, 6.28, 3)
    
    # Opções do menu
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 150, 400, 300, 60), border_radius=10)
    new_game_text = menu_font.render("Novo Jogo", True, WHITE)
    screen.blit(new_game_text, (SCREEN_WIDTH // 2 - new_game_text.get_width() // 2, 415))
    
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 150, 480, 300, 60), border_radius=10)
    quit_text = menu_font.render("Sair", True, WHITE)
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 495))

def draw_game_mode_select():
    screen.fill(DARK_BLUE)
    
    title_text = title_font.render("Selecionar Modo de Jogo", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 200, 250, 400, 80), border_radius=15)
    pvp_text = menu_font.render("Player vs Player", True, WHITE)
    screen.blit(pvp_text, (SCREEN_WIDTH // 2 - pvp_text.get_width() // 2, 275))
    
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 200, 370, 400, 80), border_radius=15)
    pvb_text = menu_font.render("Player vs Bot", True, WHITE)
    screen.blit(pvb_text, (SCREEN_WIDTH // 2 - pvb_text.get_width() // 2, 395))
    
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 500, 200, 60), border_radius=10)
    back_text = menu_font.render("Voltar", True, WHITE)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 515))

def draw_ship_placement():
    screen.fill(DARK_BLUE)
    
    title_text = title_font.render("Posicionar Navios", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
    
    player_text = menu_font.render(f"Jogador: {game.current_player.name}", True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 2 - player_text.get_width() // 2, 80))
    
    # Desenhar tabuleiro
    draw_board(game.current_player.board, BOARD_MARGIN, 150, True)
    
    # Painel de navios para posicionar
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - 300, 150, 250, 400), border_radius=10)
    
    ships_text = menu_font.render("Navios", True, WHITE)
    screen.blit(ships_text, (SCREEN_WIDTH - 225, 160))
    
    y_offset = 210
    for i, (ship_name, ship_size) in enumerate(SHIP_TYPES.items()):
        color = YELLOW if ship_name == game.selected_ship else WHITE
        ship_text = game_font.render(f"{ship_name} ({ship_size})", True, color)
        screen.blit(ship_text, (SCREEN_WIDTH - 280, y_offset))
        y_offset += 40
    
    # Botão de orientação
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 280, 500, 200, 40), border_radius=10)
    orientation_text = game_font.render(
        "Orientação: " + ("Horizontal" if game.ship_orientation else "Vertical"), 
        True, WHITE
    )
    screen.blit(orientation_text, (SCREEN_WIDTH - 270, 508))
    
    # Botão de pronto
    if game.placement_index >= len(SHIP_TYPES):
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, 600, 200, 50), border_radius=10)
        ready_text = menu_font.render("Pronto", True, WHITE)
        screen.blit(ready_text, (SCREEN_WIDTH // 2 - ready_text.get_width() // 2, 610))

def draw_game_board():
    screen.fill(DARK_BLUE)
    
    title_text = title_font.render("BATALHA NAVAL", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
    
    turn_text = menu_font.render(f"Vez de: {game.current_player.name}", True, WHITE)
    screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 80))
    
    # Tabuleiro do jogador atual
    player_label = game_font.render("Seu Tabuleiro", True, WHITE)
    screen.blit(player_label, (BOARD_MARGIN, 120))
    draw_board(game.current_player.board, BOARD_MARGIN, 150, True)
    
    # Tabuleiro de alvo (oponente)
    opponent = game.player2 if game.current_player == game.player1 else game.player1
    opponent_label = game_font.render(f"Tabuleiro de {opponent.name}", True, WHITE)
    screen.blit(opponent_label, (SCREEN_WIDTH - BOARD_MARGIN - BOARD_WIDTH, 120))
    draw_board(game.current_player.target_board, SCREEN_WIDTH - BOARD_MARGIN - BOARD_WIDTH, 150, False)

def draw_game_over():
    screen.fill(DARK_BLUE)
    
    title_text = title_font.render("FIM DE JOGO", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    
    winner_text = menu_font.render(f"Vencedor: {game.winner.name}", True, YELLOW)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, 200))
    
    # Desenhar fogos de artifício
    for i in range(5):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(300, 500)
        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        for j in range(8):
            angle = j * 45
            rad = angle * 3.14159 / 180
            length = random.randint(20, 40)
            end_x = x + length * pygame.math.Vector2(pygame.math.cos(rad), pygame.math.sin(rad))[0]
            end_y = y + length * pygame.math.Vector2(pygame.math.cos(rad), pygame.math.sin(rad))[1]
            pygame.draw.line(screen, color, (x, y), (end_x, end_y), 2)
    
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 150, 550, 300, 60), border_radius=10)
    menu_text = menu_font.render("Voltar ao Menu", True, WHITE)
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 565))

def draw_board(board, x, y, show_ships):
    # Desenhar fundo do tabuleiro
    pygame.draw.rect(screen, BLUE, (x - 5, y - 5, BOARD_WIDTH + 10, BOARD_HEIGHT + 10))
    
    # Desenhar células
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(x + col * CELL_SIZE, y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHT_BLUE, rect)
            pygame.draw.rect(screen, BLUE, rect, 1)
            
            cell_value = board[row][col]
            if cell_value is not None:
                if cell_value == 'hit':
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 3)
                elif cell_value == 'miss':
                    pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 4)
                elif show_ships and isinstance(cell_value, Ship):
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, BLUE, rect, 1)
                    
                    # Marcar partes atingidas
                    if (row, col) in cell_value.positions:
                        idx = cell_value.positions.index((row, col))
                        if idx < cell_value.hits:
                            pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 3)

# Loop principal do jogo
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if game.state == GameState.MAIN_MENU:
                # Botão de Novo Jogo
                if SCREEN_WIDTH // 2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 150 and 400 <= mouse_pos[1] <= 460:
                    game.state = GameState.GAME_MODE_SELECT
                
                # Botão de Sair
                elif SCREEN_WIDTH // 2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 150 and 480 <= mouse_pos[1] <= 540:
                    running = False
            
            elif game.state == GameState.GAME_MODE_SELECT:
                # Botão PvP
                if SCREEN_WIDTH // 2 - 200 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 200 and 250 <= mouse_pos[1] <= 330:
                    game.start_new_game(True)
                
                # Botão PvB
                elif SCREEN_WIDTH // 2 - 200 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 200 and 370 <= mouse_pos[1] <= 450:
                    game.start_new_game(False)
                
                # Botão Voltar
                elif SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and 500 <= mouse_pos[1] <= 560:
                    game.state = GameState.MAIN_MENU
            
            elif game.state == GameState.SHIP_PLACEMENT:
                # Clicou no tabuleiro para posicionar navio
                if BOARD_MARGIN <= mouse_pos[0] <= BOARD_MARGIN + BOARD_WIDTH and 150 <= mouse_pos[1] <= 150 + BOARD_HEIGHT:
                    if game.placement_index < len(SHIP_TYPES):
                        col = (mouse_pos[0] - BOARD_MARGIN) // CELL_SIZE
                        row = (mouse_pos[1] - 150) // CELL_SIZE
                        
                        ship_name = list(SHIP_TYPES.keys())[game.placement_index]
                        ship_size = SHIP_TYPES[ship_name]
                        ship = Ship(ship_name, ship_size)
                        
                        if game.current_player.place_ship(ship, row, col, game.ship_orientation):
                            game.placement_index += 1
                            if game.placement_index < len(SHIP_TYPES):
                                game.selected_ship = list(SHIP_TYPES.keys())[game.placement_index]
                
                # Clicou no botão de orientação
                elif SCREEN_WIDTH - 280 <= mouse_pos[0] <= SCREEN_WIDTH - 80 and 500 <= mouse_pos[1] <= 540:
                    game.ship_orientation = not game.ship_orientation
                
                # Clicou no botão de pronto
                elif game.placement_index >= len(SHIP_TYPES) and SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and 600 <= mouse_pos[1] <= 650:
                    if game.current_player == game.player1 and not game.player2.is_bot:
                        game.current_player = game.player2
                        game.placement_index = 0
                        game.selected_ship = list(SHIP_TYPES.keys())[0]
                    else:
                        game.state = GameState.PLAYER_TURN
                        game.current_player = game.player1
            
            elif game.state == GameState.PLAYER_TURN:
                # Clicou no tabuleiro do oponente
                opponent_x = SCREEN_WIDTH - BOARD_MARGIN - BOARD_WIDTH
                if opponent_x <= mouse_pos[0] <= opponent_x + BOARD_WIDTH and 150 <= mouse_pos[1] <= 150 + BOARD_HEIGHT:
                    col = (mouse_pos[0] - opponent_x) // CELL_SIZE
                    row = (mouse_pos[1] - 150) // CELL_SIZE
                    
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        game.make_move(row, col)
            
            elif game.state == GameState.GAME_OVER:
                # Botão de voltar ao menu
                if SCREEN_WIDTH // 2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 150 and 550 <= mouse_pos[1] <= 610:
                    game.state = GameState.MAIN_MENU
    
    # Lógica do bot
    if game.state == GameState.BOT_TURN:
        pygame.time.delay(500)  # Pequeno atraso para parecer que o bot está "pensando"
        game.bot_move()
    
    # Desenhar a tela atual
    if game.state == GameState.MAIN_MENU:
        draw_main_menu()
    elif game.state == GameState.GAME_MODE_SELECT:
        draw_game_mode_select()
    elif game.state == GameState.SHIP_PLACEMENT:
        draw_ship_placement()
    elif game.state in [GameState.PLAYER_TURN, GameState.BOT_TURN]:
        draw_game_board()
    elif game.state == GameState.GAME_OVER:
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()