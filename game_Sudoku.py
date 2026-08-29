import pygame
import sys
import random

# ================= 配置 =================
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
OFFSET_X = (WIDTH - GRID_SIZE) // 2
OFFSET_Y = 50

# 颜色
COLOR_BG = (255, 255, 255)
COLOR_GRID = (0, 0, 0)
COLOR_SELECTED = (187, 222, 251)  # 浅蓝色选中
COLOR_FIXED_TEXT = (0, 0, 0)  # 初始数字（黑色）
COLOR_USER_TEXT = (33, 150, 243)  # 玩家输入（蓝色）
COLOR_ERROR = (244, 67, 54)  # 错误冲突（红色）
COLOR_HIGHLIGHT = (232, 240, 254)  # 同行同列高亮


# ================= 逻辑类 =================
class Sudoku:
    def __init__(self):
        self.reset()

    def reset(self):
        # 1. 生成一个完整的合法数独表
        base = self.generate_solved_board()
        # 2. 随机挖洞
        self.initial_board = [row[:] for row in base]
        self.board = [row[:] for row in base]
        self.fixed = [[False for _ in range(9)] for _ in range(9)]

        # 难度设置：随机移除 45-55 个数字
        holes = random.randint(45, 55)
        while holes > 0:
            r, c = random.randint(0, 8), random.randint(0, 8)
            if self.board[r][c] != 0:
                self.board[r][c] = 0
                self.initial_board[r][c] = 0
                self.fixed[r][c] = False
                holes -= 1

        for r in range(9):
            for c in range(9):
                if self.board[r][c] != 0:
                    self.fixed[r][c] = True

        self.selected = None

    def generate_solved_board(self):
        """生成一个随机的完整数独盘面"""

        def is_valid(board, r, c, n):
            for i in range(9):
                if board[r][i] == n or board[i][c] == n: return False
            start_r, start_c = 3 * (r // 3), 3 * (c // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_r + i][start_c + j] == n: return False
            return True

        def solve(board):
            for r in range(9):
                for c in range(9):
                    if board[r][c] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for n in nums:
                            if is_valid(board, r, c, n):
                                board[r][c] = n
                                if solve(board): return True
                                board[r][c] = 0
                        return False
            return True

        board = [[0] * 9 for _ in range(9)]
        solve(board)
        return board

    def is_conflict(self, r, c, val):
        """检查 (r,c) 填入 val 是否与盘面已有数字冲突"""
        if val == 0: return False
        # 检查行和列
        for i in range(9):
            if i != c and self.board[r][i] == val: return True
            if i != r and self.board[i][c] == val: return True
        # 检查 3x3 宫
        sr, sc = 3 * (r // 3), 3 * (c // 3)
        for i in range(sr, sr + 3):
            for j in range(sc, sc + 3):
                if (i != r or j != c) and self.board[i][j] == val:
                    return True
        return False


# ================= 绘图函数 =================
def draw(screen, game, fonts):
    screen.fill(COLOR_BG)

    # 绘制标题
    title = fonts['title'].render("SUDOKU", True, COLOR_GRID)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 5))

    # 绘制高亮和选中
    if game.selected:
        sel_r, sel_c = game.selected
        # 绘制行/列高亮
        for i in range(9):
            pygame.draw.rect(screen, COLOR_HIGHLIGHT,
                             (OFFSET_X + i * CELL_SIZE, OFFSET_Y + sel_r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, COLOR_HIGHLIGHT,
                             (OFFSET_X + sel_c * CELL_SIZE, OFFSET_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # 绘制选中框
        pygame.draw.rect(screen, COLOR_SELECTED,
                         (OFFSET_X + sel_c * CELL_SIZE, OFFSET_Y + sel_r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # 绘制网格
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        # 横线
        pygame.draw.line(screen, COLOR_GRID, (OFFSET_X, OFFSET_Y + i * CELL_SIZE),
                         (OFFSET_X + GRID_SIZE, OFFSET_Y + i * CELL_SIZE), thickness)
        # 纵线
        pygame.draw.line(screen, COLOR_GRID, (OFFSET_X + i * CELL_SIZE, OFFSET_Y),
                         (OFFSET_X + i * CELL_SIZE, OFFSET_Y + GRID_SIZE), thickness)

    # 绘制数字
    for r in range(9):
        for c in range(9):
            val = game.board[r][c]
            if val != 0:
                # 冲突检查（红色）
                color = COLOR_ERROR if game.is_conflict(r, c, val) else (
                    COLOR_FIXED_TEXT if game.fixed[r][c] else COLOR_USER_TEXT)

                text = fonts['num'].render(str(val), True, color)
                rect = text.get_rect(
                    center=(OFFSET_X + c * CELL_SIZE + CELL_SIZE // 2, OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, rect)

    # 底部按钮/提示
    hint = fonts['small'].render("Click to select. 1-9 to input. Backspace to delete.", True, (100, 100, 100))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 80))

    restart_btn = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 50, 120, 40)
    pygame.draw.rect(screen, (50, 50, 50), restart_btn, border_radius=5)
    btn_text = fonts['small'].render("New Game", True, (255, 255, 255))
    screen.blit(btn_text,
                (restart_btn.centerx - btn_text.get_width() // 2, restart_btn.centery - btn_text.get_height() // 2))

    pygame.display.flip()
    return restart_btn


# ================= 主循环 =================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    fonts = {
        'title': pygame.font.SysFont("arial", 36, bold=True),
        'num': pygame.font.SysFont("arial", 32, bold=False),
        'small': pygame.font.SysFont("arial", 18, bold=False)
    }

    game = Sudoku()
    clock = pygame.time.Clock()

    while True:
        restart_btn = draw(screen, game, fonts)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # 检查网格点击
                if OFFSET_X <= x < OFFSET_X + GRID_SIZE and OFFSET_Y <= y < OFFSET_Y + GRID_SIZE:
                    c = (x - OFFSET_X) // CELL_SIZE
                    r = (y - OFFSET_Y) // CELL_SIZE
                    game.selected = (r, c)
                # 检查重启按钮
                elif restart_btn.collidepoint((x, y)):
                    game.reset()
                else:
                    game.selected = None

            if event.type == pygame.KEYDOWN and game.selected:
                r, c = game.selected
                if not game.fixed[r][c]:
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        game.board[r][c] = 1
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        game.board[r][c] = 2
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        game.board[r][c] = 3
                    elif event.key in [pygame.K_4, pygame.K_KP4]:
                        game.board[r][c] = 4
                    elif event.key in [pygame.K_5, pygame.K_KP5]:
                        game.board[r][c] = 5
                    elif event.key in [pygame.K_6, pygame.K_KP6]:
                        game.board[r][c] = 6
                    elif event.key in [pygame.K_7, pygame.K_KP7]:
                        game.board[r][c] = 7
                    elif event.key in [pygame.K_8, pygame.K_KP8]:
                        game.board[r][c] = 8
                    elif event.key in [pygame.K_9, pygame.K_KP9]:
                        game.board[r][c] = 9
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0]:
                        game.board[r][c] = 0

        clock.tick(30)


if __name__ == "__main__":
    main()
