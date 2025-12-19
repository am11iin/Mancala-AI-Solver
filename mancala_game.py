import pygame
import sys
import copy
import math
import random
import time

# --- CONSTANTES GLOBALES ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550 
FPS = 30
MAX_DEPTH = 4 # Profondeur maximale pour l'IA

# Joueurs
PLAYER_1 = 1  # MAX
PLAYER_2 = -1 # MIN

# Couleurs
BG_COLOR = (36, 40, 48)            
BOARD_COLOR = (0, 119, 144)        
PIT_COLOR = (200, 200, 200)        
STORE_COLOR = (0, 75, 95)         
SCORE_BOX_COLOR = (240, 240, 240)  
SEED_COLORS = [
    (255, 99, 71),   
    (255, 204, 0),  
    (60, 179, 113),  
    (70, 130, 180)   
]
HIGHLIGHT_COLOR = (255, 230, 0)   
LABEL_COLOR = (255, 255, 255)
MENU_COLOR = (25, 25, 30)         
BTN_COLOR = (0, 179, 100)        
BTN_HOVER = (0, 219, 130)         

# --- LOGIQUE DU JEU ---
class MancalaBoard:
    def __init__(self):
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,
            '1': 0, '2': 0
        }
        self.p1_pits = ['A', 'B', 'C', 'D', 'E', 'F']
        self.p2_pits = ['G', 'H', 'I', 'J', 'K', 'L']
        
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L',
            'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G', 'G': '2',
            '2': 'A'
        }
        self.opposite_pit = {
            'A': 'G', 'G': 'A', 'B': 'H', 'H': 'B', 'C': 'I', 'I': 'C',
            'D': 'J', 'J': 'D', 'E': 'K', 'K': 'E', 'F': 'L', 'L': 'F'
        }

    def possibleMoves(self, player_idx):
        pits = self.p1_pits if player_idx == 1 else self.p2_pits
        return [p for p in pits if self.board[p] > 0]

    def doMove(self, player_idx, pit):
        seeds = self.board[pit]
        self.board[pit] = 0
        current_pit = pit
        
        opponent_store = '2' if player_idx == 1 else '1'
        own_store = '1' if player_idx == 1 else '2'
        
        while seeds > 0:
            current_pit = self.next_pit[current_pit]
            if current_pit == opponent_store: continue
            self.board[current_pit] += 1
            seeds -= 1

        extra_turn = (current_pit == own_store)

        is_own_pit = (current_pit in self.p1_pits if player_idx == 1 else current_pit in self.p2_pits)
        
        if not extra_turn and self.board[current_pit] == 1 and is_own_pit:
            opposite = self.opposite_pit.get(current_pit)
            if opposite:
                captured = self.board[opposite]
                if captured > 0:
                    self.board[own_store] += captured + 1 
                    self.board[opposite] = 0
                    self.board[current_pit] = 0
                
        return extra_turn

#  LOGIQUE DE LA PARTIE 
class Game:
    def __init__(self, mode="HvC"):
        self.state = MancalaBoard()
        self.mode = mode 
        
    def gameOver(self):
        p1_empty = all(self.state.board[p] == 0 for p in self.state.p1_pits)
        p2_empty = all(self.state.board[p] == 0 for p in self.state.p2_pits)

        if p1_empty or p2_empty:
            remaining_p1 = sum(self.state.board[p] for p in self.state.p1_pits)
            remaining_p2 = sum(self.state.board[p] for p in self.state.p2_pits)
            self.state.board['1'] += remaining_p1
            self.state.board['2'] += remaining_p2
            for p in self.state.p1_pits + self.state.p2_pits:
                self.state.board[p] = 0
            return True
        return False

    def findWinner(self):
        s1, s2 = self.state.board['1'], self.state.board['2']
        p1_name = "Human (P1)" if self.mode == "HvC" else "Comp 1 (P1)"
        p2_name = "Comp (P2)" if self.mode == "HvC" else "Comp 2 (P2)"
        
        if s1 > s2: return p1_name, s1
        if s2 > s1: return p2_name, s2
        return "Draw", s1

    # --- HEURISTICS ---
    def evaluate(self, player_perspective, heuristic_type=1):
        s1 = self.state.board['1']
        s2 = self.state.board['2']
        score = (s1 - s2) if player_perspective == 1 else (s2 - s1)

        if heuristic_type == 1:
            # H1: Heuristique Simple (Différence de magasins seulement)
            return score
            
        elif heuristic_type == 2:
            # H2: Heuristique Stratégique (Différence de magasins + contrôle du plateau)
            my_pits = self.state.p1_pits if player_perspective == 1 else self.state.p2_pits
            opp_pits = self.state.p2_pits if player_perspective == 1 else self.state.p1_pits
            
            my_seeds = sum(self.state.board[p] for p in my_pits)
            opp_seeds = sum(self.state.board[p] for p in opp_pits)
            
            # Poids 0.1 pour le score en magasin, Poids 0.1 pour les graines sur le plateau.
            return score + (0.1 * my_seeds) - (0.1 * opp_seeds)
        

# --- MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING ---
def Minimax(game_node, max_player_idx, current_player, depth, alpha, beta, heuristic_id):
    if depth == 0 or game_node.gameOver():
        return game_node.evaluate(max_player_idx, heuristic_id), None

    possible_moves = game_node.state.possibleMoves(current_player)
    if not possible_moves:
        return game_node.evaluate(max_player_idx, heuristic_id), None

    bestPit = None

    if current_player == max_player_idx:
        bestValue = -math.inf
        for pit in possible_moves:
            child = copy.deepcopy(game_node)
            extra = child.state.doMove(current_player, pit)
            
            next_p = current_player if extra else (-1 if current_player == 1 else 1)
            
            value, _ = Minimax(child, max_player_idx, next_p, depth - 1, alpha, beta, heuristic_id)
            
            if value > bestValue:
                bestValue = value
                bestPit = pit
            alpha = max(alpha, bestValue)
            if bestValue >= beta: break
        return bestValue, bestPit

    else: # MIN player's turn
        bestValue = math.inf
        for pit in possible_moves:
            child = copy.deepcopy(game_node)
            extra = child.state.doMove(current_player, pit)
            
            next_p = current_player if extra else (-1 if current_player == 1 else 1)
            
            value, _ = Minimax(child, max_player_idx, next_p, depth - 1, alpha, beta, heuristic_id)
            
            if value < bestValue:
                bestValue = value
                bestPit = pit
            beta = min(beta, bestValue)
            if bestValue <= alpha: break
        return bestValue, bestPit
    


# INTERFACE GRAPHIQUE UTILISATEUR (GUI)
class MancalaGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mancala: AI Analysis Tool")
        self.clock = pygame.time.Clock()
        
        self.font_large = pygame.font.SysFont('Calibri, Arial', 36, bold=True)
        self.font_med = pygame.font.SysFont('Calibri, Arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('Calibri, Arial', 16)

        self.state = "MENU" # MENU, GAME, GAMEOVER
        self.game = None
        self.turn = PLAYER_1
        self.status_msg = ""
        self.ai_thinking = False
        
        self.pit_rects = {}
        self.setup_layout()
        
        # Boutons
        self.btn_hvc = pygame.Rect(350, 200, 300, 60)
        self.btn_cvc = pygame.Rect(350, 300, 300, 60)
        self.btn_menu = pygame.Rect(SCREEN_WIDTH-120, 10, 100, 40)

    def setup_layout(self):
        bx, by, bw, bh = 50, 100, 900, 340
        self.board_rect = pygame.Rect(bx, by, bw, bh)
        
        start_x = bx + 120
        spacing = 100
        
        # P2 Pits (Top)
        for i, k in enumerate(['G','H','I','J','K','L']):
            self.pit_rects[k] = pygame.Rect(start_x + i*spacing, by + 40, 80, 80)
        # P1 Pits (Bottom)
        for i, k in enumerate(['A','B','C','D','E','F']):
            self.pit_rects[k] = pygame.Rect(start_x + i*spacing, by + 220, 80, 80)
            
        # Stores (Magasins)
        self.pit_rects['2'] = pygame.Rect(bx + 10, by + 40, 100, 280)
        self.pit_rects['1'] = pygame.Rect(bx + bw - 110, by + 40, 100, 280)

    def draw_seeds(self, rect, count, pit_name):
        if count == 0: return
        cx, cy = rect.center
        random.seed(ord(pit_name) + count * 555) # Rendu déterministe
        
        for i in range(count):
            col = SEED_COLORS[i % 4]
            
            if pit_name not in ['1', '2']:
                # Pits : Distribution circulaire
                angle = random.uniform(0, 6.28)
                dist = random.uniform(0, rect.width/2 - 12) 
                x = cx + dist * math.cos(angle)
                y = cy + dist * math.sin(angle)
            else:
                # Stores : Distribution sur toute la surface
                x = random.uniform(rect.left + 15, rect.right - 15)
                y = random.uniform(rect.top + 15, rect.bottom - 15)
                
            pygame.draw.circle(self.screen, col, (int(x), int(y)), 8)
            pygame.draw.circle(self.screen, (0,0,0), (int(x), int(y)), 8, 1)

    def draw_menu(self):
        self.screen.fill(MENU_COLOR)
        title = self.font_large.render("MANCALA AI SOLVER", True, HIGHLIGHT_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        # Boutons
        mx, my = pygame.mouse.get_pos()
        
        c1 = BTN_HOVER if self.btn_hvc.collidepoint((mx,my)) else BTN_COLOR
        c2 = BTN_HOVER if self.btn_cvc.collidepoint((mx,my)) else BTN_COLOR
        
        pygame.draw.rect(self.screen, c1, self.btn_hvc, border_radius=15)
        pygame.draw.rect(self.screen, c2, self.btn_cvc, border_radius=15)
        
        # Textes mis à jour pour refléter l'inversion des heuristiques en CvC
        t1 = self.font_med.render("Humain vs Ordinateur (P2: H1 Simple)", True, (255,255,255))
        t2 = self.font_med.render("Ordinateur vs Ordinateur (P1: H2 Strat. | P2: H1 Simple)", True, (255,255,255))
        
        self.screen.blit(t1, (self.btn_hvc.centerx - t1.get_width()//2, self.btn_hvc.centery - 12))
        self.screen.blit(t2, (self.btn_cvc.centerx - t2.get_width()//2, self.btn_cvc.centery - 12))
        
        sub = self.font_small.render("H1: Heuristique Simple (Diff. Stores) | H2: Heuristique Stratégique (Diff. Stores + Contrôle Plateau)", True, (150,150,150))
        self.screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 380))

    def draw_game(self):
        self.screen.fill(BG_COLOR)
        
        # Header
        mode_txt = "HvC (P2: H1 Simple)" if self.game.mode == "HvC" else "CvC (P1: H2 Strat. vs P2: H1 Simple)"
        h_s = self.font_med.render(mode_txt, True, BTN_COLOR)
        self.screen.blit(h_s, (30, 20))
        
        # Menu Btn
        pygame.draw.rect(self.screen, MENU_COLOR, self.btn_menu, border_radius=5)
        m_txt = self.font_small.render("MENU", True, (255,255,255))
        self.screen.blit(m_txt, (self.btn_menu.centerx-m_txt.get_width()//2, self.btn_menu.centery-8))
        
        # Status
        stat = self.font_med.render(self.status_msg, True, HIGHLIGHT_COLOR)
        self.screen.blit(stat, (SCREEN_WIDTH//2 - stat.get_width()//2, 60))

        # Board
        pygame.draw.rect(self.screen, BOARD_COLOR, self.board_rect, border_radius=20)
        pygame.draw.rect(self.screen, (0, 0, 0), self.board_rect, 3, border_radius=20)
        
        mx, my = pygame.mouse.get_pos()
        
        for k, r in self.pit_rects.items():
            color = PIT_COLOR
            # Highlight Logic (Surlignage)
            if not self.ai_thinking and not self.game.gameOver():
                if self.game.mode == "HvC" and self.turn == PLAYER_1:
                    if k in self.game.state.p1_pits and r.collidepoint((mx,my)) and self.game.state.board[k] > 0:
                        color = HIGHLIGHT_COLOR
                        
            if k in ['1','2']: 
                # Stores (Magasins) : Utilisation de STORE_COLOR
                color = HIGHLIGHT_COLOR if self.turn == (PLAYER_1 if k == '1' else PLAYER_2) and "Tour Supplémentaire" in self.status_msg else STORE_COLOR
                pygame.draw.rect(self.screen, color, r, border_radius=15)
                pygame.draw.rect(self.screen, (255, 255, 255), r, 2, border_radius=15) 
            else: 
                # Pits (Fosses)
                pygame.draw.circle(self.screen, BG_COLOR, r.center, r.width//2 + 2) 
                pygame.draw.ellipse(self.screen, color, r)
            
            self.draw_seeds(r, self.game.state.board[k], k)
            
            # Labels
            if k not in ['1','2']:
                lbl = self.font_small.render(k, True, LABEL_COLOR)
                off = 60 if k in self.game.state.p1_pits else -60
                self.screen.blit(lbl, (r.centerx-5, r.centery+off))

        # Scores
        s1 = self.game.state.board['1']
        s2 = self.game.state.board['2']
        lbl1 = "Human (P1)" if self.game.mode == "HvC" else "Comp 1 (P1)"
        lbl2 = "Comp (P2)" if self.game.mode == "HvC" else "Comp 2 (P2)"
        
        t1_col = HIGHLIGHT_COLOR if self.turn == PLAYER_1 else SCORE_BOX_COLOR
        t2_col = HIGHLIGHT_COLOR if self.turn == PLAYER_2 else SCORE_BOX_COLOR
        
        # Affichage des scores
        t1 = self.font_large.render(f"{lbl1}: {s1}", True, t1_col)
        t2 = self.font_large.render(f"{lbl2}: {s2}", True, t2_col)
        
        self.screen.blit(t2, (50, 480))
        self.screen.blit(t1, (SCREEN_WIDTH-250, 480))

    def run(self):
        while True:
            self.clock.tick(FPS)
            
            if self.state == "MENU":
                self.draw_menu()
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = e.pos
                        if self.btn_hvc.collidepoint((mx,my)):
                            self.game = Game("HvC")
                            self.turn = PLAYER_1
                            self.status_msg = "Tour Humain (P1)"
                            self.state = "GAME"
                        elif self.btn_cvc.collidepoint((mx,my)):
                            self.game = Game("CvC")
                            self.turn = PLAYER_1
                            self.status_msg = "Comp 1 Réfléchit... (P1: H2 Stratégique)"
                            self.state = "GAME"
                            self.ai_thinking = True

            elif self.state == "GAME":
                self.draw_game()
                
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if self.btn_menu.collidepoint(e.pos):
                            self.state = "MENU"
                            self.ai_thinking = False
                            self.game = None
                            break
                        
                        # Entrée Humaine (P1)
                        if self.game and self.game.mode == "HvC" and self.turn == PLAYER_1 and not self.ai_thinking:
                            for k in self.game.state.p1_pits:
                                if self.pit_rects[k].collidepoint(e.pos) and self.game.state.board[k] > 0:
                                    self.handle_move(PLAYER_1, k)
                                    break
                
                # Logique de l'IA
                if self.ai_thinking and not self.game.gameOver():
                    pygame.display.flip() 
                    time.sleep(0.5) 
                    
                    if self.turn == PLAYER_1: 
                        # CvC Mode: Comp 1 (H2 Stratégique)
                        if self.game.mode == "CvC":
                            # P1 utilise Heuristique 2 (Stratégique - le plus intelligent)
                            _, move = Minimax(self.game, PLAYER_1, PLAYER_1, MAX_DEPTH, -math.inf, math.inf, 2)
                            if move: self.handle_move(PLAYER_1, move)
                            else: self.pass_turn()
                        else:
                            self.ai_thinking = False
                        
                    elif self.turn == PLAYER_2:
                        # P2: Comp (H1 Simple) dans les deux modes (HvC et CvC)
                        # P2 utilise Heuristique 1 (Simple)
                        _, move = Minimax(self.game, PLAYER_2, PLAYER_2, MAX_DEPTH, -math.inf, math.inf, 1)
                        if move: self.handle_move(PLAYER_2, move)
                        else: self.pass_turn()
                    
                if self.game and self.game.gameOver():
                    w, s = self.game.findWinner()
                    self.status_msg = f"FIN DE PARTIE ! {w} Gagne ({s})"
                    self.ai_thinking = False

            pygame.display.flip()

    def handle_move(self, player, pit):
        extra = self.game.state.doMove(player, pit)
        if extra:
            if self.game.mode == "HvC" and player == PLAYER_1:
                self.status_msg = "Tour Supplémentaire! Humain (P1)"
                self.ai_thinking = False
            else:
                p_name = "Comp 1" if player == 1 else "Comp 2"
                h_name = "H2 Stratégique" if self.game.mode == "CvC" and player == 1 else "H1 Simple"
                self.status_msg = f"Tour Supplémentaire! {p_name} Réfléchit... ({h_name})"
                self.ai_thinking = True
            
        else:
            self.pass_turn()

    def pass_turn(self):
        self.turn = -1 if self.turn == 1 else 1
        
        if self.game.mode == "HvC":
            if self.turn == PLAYER_1:
                self.status_msg = "Tour Humain (P1)"
                self.ai_thinking = False
            else:
                self.status_msg = "Comp Réfléchit... (P2: H1 Simple)"
                self.ai_thinking = True
        else: # CvC
            p_name = "Comp 1" if self.turn == 1 else "Comp 2"
            h_name = "H2 Stratégique" if self.turn == 1 else "H1 Simple"
            self.status_msg = f"{p_name} Réfléchit... (Utilise {h_name})"
            self.ai_thinking = True

if __name__ == "__main__":
    MancalaGUI().run()