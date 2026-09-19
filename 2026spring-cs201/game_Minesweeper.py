# 看到力扣这个题目，因此pygame一个扫雷游戏。M529.扫雷游戏
# dfs, bfs, https://leetcode.cn/problems/minesweeper/

#!/usr/bin/env python3
import pygame
import random
import sys
import time

# ================= 配置 =================
ROWS = 10
COLS = 10
MINE_COUNT = 15
CELL_SIZE = 40
HEADER_HEIGHT = 80

WINDOW_WIDTH = COLS * CELL_SIZE + 40
WINDOW_HEIGHT = ROWS * CELL_SIZE + HEADER_HEIGHT + 20

# 颜色定义
COLOR_BG = (250, 248, 239)
COLOR_GRID_BG = (187, 173, 160)
COLOR_UNKNOWN = (205, 193, 180)  # 未挖开
COLOR_REVEALED = (238, 228, 218)  # 已挖开 (B)
COLOR_TEXT_DARK = (119, 110, 101)
COLOR_MINE = (246, 94, 59)
COLOR_FLAG = (242, 177, 121)
BUTTON_COLOR = (143, 122, 102)

# 数字颜色
NUM_COLORS = {
    1: (65, 105, 225), 2: (34, 139, 34), 3: (178, 34, 34),
    4: (0, 0, 128), 5: (128, 0, 0), 6: (0, 128, 128),
    7: (0, 0, 0), 8: (128, 128, 128)
}


# =============== 逻辑类 ===============
class Minesweeper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines_total = mines
        self.reset()

    def reset(self):
        # board 存储状态: 'M'(地雷), 'E'(未挖空方块)
        self.board = [['E' for _ in range(self.cols)] for _ in range(self.rows)]
        # status 存储显示状态: 'hidden', 'revealed', 'flagged'
        self.status = [['hidden' for _ in range(self.cols)] for _ in range(self.rows)]
        self.mine_positions = set()
        self.game_over = False
        self.won = False
        self.first_click = True
        self.start_time = None
        self.flags = set()

    def _place_mines(self, exclude_r, exclude_c):
        """在第一次点击后放置地雷，确保第一下不是雷"""
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                     if (r, c) != (exclude_r, exclude_c)]
        self.mine_positions = set(random.sample(positions, self.mines_total))
        for r, c in self.mine_positions:
            self.board[r][c] = 'M'

    def _get_neighbors(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def _count_adjacent_mines(self, r, c):
        count = 0
        for nr, nc in self._get_neighbors(r, c):
            if self.board[nr][nc] == 'M':
                count += 1
        return count

    def reveal(self, r, c):
        if self.game_over or self.won or (r, c) in self.flags:
            return

        if self.first_click:
            self._place_mines(r, c)
            self.first_click = False
            self.start_time = time.time()

        if self.board[r][c] == 'M':
            self.game_over = True
            self.status[r][c] = 'revealed'
            return

        if self.status[r][c] == 'revealed':
            return

        # 核心算法 (同 LeetCode 529)
        mines = self._count_adjacent_mines(r, c)
        if mines > 0:
            self.board[r][c] = str(mines)
            self.status[r][c] = 'revealed'
        else:
            self.board[r][c] = 'B'
            self.status[r][c] = 'revealed'
            for nr, nc in self._get_neighbors(r, c):
                if self.status[nr][nc] == 'hidden':
                    self.reveal(nr, nc)

        self._check_win()

    def toggle_flag(self, r, c):
        if self.game_over or self.won or self.status[r][c] == 'revealed':
            return
        if (r, c) in self.flags:
            self.flags.remove((r, c))
        else:
            if len(self.flags) < self.mines_total:
                self.flags.add((r, c))

    def _check_win(self):
        unrevealed_count = sum(row.count('hidden') for row in self.status)
        if unrevealed_count == self.mines_total:
            self.won = True


# =============== 绘图函数 ===============
def draw(screen, game, fonts):
    screen.fill(COLOR_BG)

    # 标题与状态
    title_text = "MINES"
    if game.won: title_text = "YOU WIN!"
    if game.game_over: title_text = "BOOM!"

    title = fonts["title"].render(title_text, True, COLOR_TEXT_DARK)
    screen.blit(title, (20, 10))

    # 计数器与计时
    mine_info = fonts["small"].render(f"Mines: {game.mines_total - len(game.flags)}", True, COLOR_TEXT_DARK)
    screen.blit(mine_info, (20, 55))

    elapsed = 0
    if game.start_time and not game.game_over and not game.won:
        elapsed = int(time.time() - game.start_time)
    elif game.game_over or game.won:
        # 这里可以固定显示结束时的时间（如果需要）
        pass

    timer_info = fonts["small"].render(f"Time: {elapsed}s", True, COLOR_TEXT_DARK)
    screen.blit(timer_info, (WINDOW_WIDTH - 100, 55))

    # 重开按钮
    restart_btn = pygame.Rect(WINDOW_WIDTH - 100, 15, 80, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_btn, border_radius=5)
    r_text = fonts["small_bold"].render("Reset", True, (255, 255, 255))
    screen.blit(r_text, (restart_btn.x + 15, restart_btn.y + 5))

    # 棋盘绘制
    board_rect = pygame.Rect(20, HEADER_HEIGHT, COLS * CELL_SIZE, ROWS * CELL_SIZE)
    pygame.draw.rect(screen, COLOR_GRID_BG, board_rect, border_radius=2)

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(20 + c * CELL_SIZE + 2, HEADER_HEIGHT + r * CELL_SIZE + 2,
                               CELL_SIZE - 4, CELL_SIZE - 4)

            curr_status = game.status[r][c]
            val = game.board[r][c]

            if curr_status == 'hidden':
                color = COLOR_UNKNOWN
                pygame.draw.rect(screen, color, rect, border_radius=3)
                if (r, c) in game.flags:
                    f_text = fonts["mid"].render("F", True, COLOR_FLAG)
                    screen.blit(f_text, f_text.get_rect(center=rect.center))
            else:  # revealed
                color = COLOR_REVEALED
                if val == 'M': color = COLOR_MINE
                pygame.draw.rect(screen, color, rect, border_radius=3)

                if val.isdigit():
                    num_color = NUM_COLORS.get(int(val), COLOR_TEXT_DARK)
                    text = fonts["mid"].render(val, True, num_color)
                    screen.blit(text, text.get_rect(center=rect.center))
                elif val == 'M':
                    m_text = fonts["mid"].render("X", True, (255, 255, 255))
                    screen.blit(m_text, m_text.get_rect(center=rect.center))

    pygame.display.flip()
    return restart_btn


# =============== 主循环 ===============
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper Python")

    fonts = {
        "title": pygame.font.SysFont("arial", 32, True),
        "mid": pygame.font.SysFont("arial", 24, True),
        "small": pygame.font.SysFont("arial", 18, False),
        "small_bold": pygame.font.SysFont("arial", 18, True)
    }

    game = Minesweeper(ROWS, COLS, MINE_COUNT)
    clock = pygame.time.Clock()

    while True:
        restart_btn = draw(screen, game, fonts)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # 点击重置按钮
                if restart_btn.collidepoint(mouse_pos):
                    game.reset()
                    continue

                # 点击棋盘
                if HEADER_HEIGHT <= mouse_pos[1] < HEADER_HEIGHT + ROWS * CELL_SIZE:
                    if 20 <= mouse_pos[0] < 20 + COLS * CELL_SIZE:
                        c = (mouse_pos[0] - 20) // CELL_SIZE
                        r = (mouse_pos[1] - HEADER_HEIGHT) // CELL_SIZE

                        if event.button == 1:  # 左键
                            game.reveal(r, c)
                        elif event.button == 3:  # 右键
                            game.toggle_flag(r, c)

        clock.tick(30)


if __name__ == "__main__":
    main()
