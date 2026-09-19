import pygame
import random
import sys

# ================= 配置 =================
WIDTH, HEIGHT = 800, 600
COLOR_BG = (0, 100, 0)  # 牌桌绿
COLOR_CARD = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_GOLD = (255, 215, 0)
COLOR_HOLD = (255, 50, 50)

# 扑克牌定义
SUITS = ['♠', '♥', '♦', '♣']
SUIT_COLORS = {'♠': (0, 0, 0), '♣': (0, 0, 0), '♥': (200, 0, 0), '♦': (200, 0, 0)}
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, 2)}

# 派彩表 (Jacks or Better)
PAYTABLE = [
    ("Royal Flush", 250), ("Straight Flush", 50), ("Four of a Kind", 25),
    ("Full House", 9), ("Flush", 6), ("Straight", 4),
    ("Three of a Kind", 3), ("Two Pair", 2), ("Jacks or Better", 1)
]


# ================= 逻辑类 =================
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.held = False


class PokerGame:
    def __init__(self):
        self.deck = [Card(r, s) for r in RANKS for s in SUITS]
        self.hand = []
        self.credits = 100
        self.bet = 1
        self.state = "IDLE"  # IDLE, DEALING, RESULT
        self.message = "PRESS DEAL TO START"
        self.win_type = ""

    def deal(self):
        if self.state == "IDLE":
            if self.credits < self.bet: return
            self.credits -= self.bet
            random.shuffle(self.deck)
            self.hand = [self.deck[i] for i in range(5)]
            self.state = "HOLDING"
            self.message = "SELECT CARDS TO HOLD"
        elif self.state == "HOLDING":
            # 替换没被 hold 的牌
            used_cards = 5
            for i in range(5):
                if not self.hand[i].held:
                    self.hand[i] = self.deck[used_cards]
                    used_cards += 1
            self.evaluate_hand()
            self.state = "RESULT"

    def evaluate_hand(self):
        ranks = sorted([RANK_VALUES[c.rank] for c in self.hand])
        suits = [c.suit for c in self.hand]
        counts = {r: ranks.count(r) for r in set(ranks)}
        freq = sorted(counts.values(), reverse=True)

        is_flush = len(set(suits)) == 1
        is_straight = len(set(ranks)) == 5 and (ranks[-1] - ranks[0] == 4)
        # 特殊处理 A,2,3,4,5 顺子
        if set(ranks) == {14, 2, 3, 4, 5}: is_straight = True

        win_amount = 0
        self.win_type = "NO WIN"

        if is_flush and is_straight and max(ranks) == 14:
            self.win_type, win_amount = PAYTABLE[0]
        elif is_flush and is_straight:
            self.win_type, win_amount = PAYTABLE[1]
        elif freq == [4, 1]:
            self.win_type, win_amount = PAYTABLE[2]
        elif freq == [3, 2]:
            self.win_type, win_amount = PAYTABLE[3]
        elif is_flush:
            self.win_type, win_amount = PAYTABLE[4]
        elif is_straight:
            self.win_type, win_amount = PAYTABLE[5]
        elif freq == [3, 1, 1]:
            self.win_type, win_amount = PAYTABLE[6]
        elif freq == [2, 2, 1]:
            self.win_type, win_amount = PAYTABLE[7]
        elif freq == [2, 1, 1, 1]:
            # 检查是否是 Jacks or Better
            pair_rank = [r for r, c in counts.items() if c == 2][0]
            if pair_rank >= 11:  # J=11
                self.win_type, win_amount = PAYTABLE[8]

        actual_win = win_amount * self.bet
        self.credits += actual_win
        self.message = f"{self.win_type}! +{actual_win}" if actual_win > 0 else "NO WIN"

    def reset(self):
        self.state = "IDLE"
        self.hand = []
        self.message = "PRESS DEAL TO START"


# ================= 绘图 =================
def draw_game(screen, game, fonts):
    screen.fill(COLOR_BG)

    # 绘制派彩表
    for i, (name, val) in enumerate(PAYTABLE):
        color = COLOR_GOLD if game.win_type == name else COLOR_TEXT
        txt = fonts['small'].render(f"{name:<15} {val * game.bet}", True, color)
        screen.blit(txt, (20, 20 + i * 25))

    # 绘制余额
    credits_txt = fonts['mid'].render(f"CREDITS: {game.credits}", True, COLOR_GOLD)
    screen.blit(credits_txt, (550, 30))

    # 绘制提示信息
    msg_txt = fonts['mid'].render(game.message, True, COLOR_TEXT)
    screen.blit(msg_txt, (WIDTH // 2 - msg_txt.get_width() // 2, 480))

    # 绘制卡牌
    card_w, card_h = 110, 160
    start_x = (WIDTH - (5 * card_w + 4 * 20)) // 2
    for i, card in enumerate(game.hand):
        x = start_x + i * (card_w + 20)
        y = 280
        rect = pygame.Rect(x, y, card_w, card_h)

        # 卡牌背景
        pygame.draw.rect(screen, COLOR_CARD, rect, border_radius=10)

        # 牌面文字
        rank_color = SUIT_COLORS[card.suit]
        r_txt = fonts['big'].render(card.rank, True, rank_color)
        s_txt = fonts['big'].render(card.suit, True, rank_color)
        screen.blit(r_txt, (x + 10, y + 10))
        screen.blit(s_txt, (x + card_w - 40, y + card_h - 50))

        # HOLD 标记
        if game.state == "HOLDING":
            if card.held:
                pygame.draw.rect(screen, COLOR_HOLD, (x, y + card_h + 10, card_w, 30), border_radius=5)
                h_txt = fonts['small'].render("HELD", True, COLOR_TEXT)
                screen.blit(h_txt, (x + 35, y + card_h + 15))
            else:
                hint = fonts['small'].render("Click to Hold", True, (150, 150, 150))
                screen.blit(hint, (x + 10, y + card_h + 15))

    # 绘制按钮
    btn_rect = pygame.Rect(WIDTH // 2 - 60, 520, 120, 50)
    pygame.draw.rect(screen, (100, 100, 255), btn_rect, border_radius=10)
    btn_label = "DRAW" if game.state == "HOLDING" else "DEAL"
    if game.state == "RESULT": btn_label = "NEXT"
    txt = fonts['mid'].render(btn_label, True, COLOR_TEXT)
    screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))

    pygame.display.flip()
    return btn_rect, start_x, card_w


# ================= 主循环 =================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Video Poker - Jacks or Better")

    fonts = {
        'small': pygame.font.SysFont("monospace", 18, bold=True),
        'mid': pygame.font.SysFont("arial", 32, bold=True),
        'big': pygame.font.SysFont("arial", 40, bold=True)
    }

    game = PokerGame()
    clock = pygame.time.Clock()

    while True:
        btn_rect, card_start_x, card_w = draw_game(screen, game, fonts)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # 点击按钮
                if btn_rect.collidepoint(pos):
                    if game.state == "RESULT":
                        game.reset()
                    else:
                        game.deal()

                # 点击卡牌进行 Hold
                if game.state == "HOLDING":
                    for i in range(5):
                        card_x = card_start_x + i * (card_w + 20)
                        card_rect = pygame.Rect(card_x, 280, card_w, 160)
                        if card_rect.collidepoint(pos):
                            game.hand[i].held = not game.hand[i].held

        clock.tick(30)


if __name__ == "__main__":
    main()
