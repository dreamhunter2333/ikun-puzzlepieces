import os
import random
import pygame

ROOT_DIR = os.path.dirname(__file__)


class Config():
    # FPS
    FPS = 60
    # 定义一些颜色
    BACKGROUNDCOLOR = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    # 随机打乱拼图次数
    NUMRANDOM = 100
    # 屏幕大小
    SCREENSIZE = (640, 640)
    # 标题
    TITLE = '拼图小游戏 - 鸡你太美 ikun 版'
    # 游戏图片路径
    IMAGE_PATH = os.path.join(ROOT_DIR, 'resources/image.png')
    # 字体路径
    FONT_PATH = os.path.join(
        ROOT_DIR, 'resources/fonts/LXGWWenKai-Regular.ttf'
    )
    START_KEYMAP = {ord("l"): 3, ord("m"): 4, ord("h"): 5}


class PuzzlePiecesGame:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(Config.TITLE)
        self.screen = pygame.display.set_mode(Config.SCREENSIZE)
        self.image = pygame.transform.scale(
            pygame.image.load(Config.IMAGE_PATH),
            Config.SCREENSIZE
        )
        self.min_font = pygame.font.Font(
            Config.FONT_PATH, Config.SCREENSIZE[0] // 20
        )
        self.mid_font = pygame.font.Font(
            Config.FONT_PATH, Config.SCREENSIZE[0] // 15
        )
        self.max_font = pygame.font.Font(
            Config.FONT_PATH, Config.SCREENSIZE[0] // 10
        )

    def run(self):
        # 游戏开始界面
        size = self.ShowStartInterface()
        if size <= 0:
            return False
        num_rows, num_cols = size, size
        num_cells = size * size
        # 使用的图片
        game_img_used_rect = self.image.get_rect()
        # 计算Cell大小
        cell_width = game_img_used_rect.width // num_cols
        cell_height = game_img_used_rect.height // num_rows
        # 避免初始化为原图
        while True:
            game_board, blank_cell_idx = self.CreateBoard(
                num_rows, num_cols, num_cells)
            if not self.isGameOver(game_board, size):
                break
        # 游戏主循环
        is_running = True
        is_restart = False
        clock = pygame.time.Clock()
        while is_running and not is_restart:
            # --事件捕获
            for event in pygame.event.get():
                # ----退出游戏
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                # ----键盘操作
                elif event.type == pygame.KEYDOWN:
                    if event.key == ord('r'):
                        is_restart = True
                        break
                    elif event.key == pygame.K_LEFT or event.key == ord('a'):
                        blank_cell_idx = self.moveL(
                            game_board, blank_cell_idx, num_cols)
                    elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                        blank_cell_idx = self.moveR(
                            game_board, blank_cell_idx, num_cols)
                    elif event.key == pygame.K_UP or event.key == ord('w'):
                        blank_cell_idx = self.moveU(
                            game_board, blank_cell_idx, num_rows, num_cols)
                    elif event.key == pygame.K_DOWN or event.key == ord('s'):
                        blank_cell_idx = self.moveD(
                            game_board, blank_cell_idx, num_cols)
                # ----鼠标操作
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x_pos = x // cell_width
                    y_pos = y // cell_height
                    idx = x_pos + y_pos * num_cols
                    if idx == blank_cell_idx-1:
                        blank_cell_idx = self.moveR(
                            game_board, blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx+1:
                        blank_cell_idx = self.moveL(
                            game_board, blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx+num_cols:
                        blank_cell_idx = self.moveU(
                            game_board, blank_cell_idx, num_rows, num_cols)
                    elif idx == blank_cell_idx-num_cols:
                        blank_cell_idx = self.moveD(
                            game_board, blank_cell_idx, num_cols)
            if is_restart:
                break
            # --判断游戏是否结束
            if self.isGameOver(game_board, size):
                game_board[blank_cell_idx] = num_cells - 1
                is_running = False
                break
            # --更新屏幕
            self.screen.fill(Config.BACKGROUNDCOLOR)
            for i in range(num_cells):
                if game_board[i] == -1:
                    continue
                x_pos = i // num_cols
                y_pos = i % num_cols
                rect = pygame.Rect(
                    y_pos * cell_width,
                    x_pos * cell_height,
                    cell_width, cell_height
                )
                img_area = pygame.Rect(
                    (game_board[i] % num_cols) * cell_width,
                    (game_board[i] // num_cols) * cell_height,
                    cell_width, cell_height
                )
                self.screen.blit(self.image, rect, img_area)
            for i in range(num_cols+1):
                pygame.draw.line(
                    self.screen, Config.BLACK, (i*cell_width, 0),
                    (i*cell_width, game_img_used_rect.height)
                )
            for i in range(num_rows+1):
                pygame.draw.line(
                    self.screen, Config.BLACK, (0, i*cell_height),
                    (game_img_used_rect.width, i*cell_height)
                )
            pygame.display.update()
            clock.tick(Config.FPS)
        # 游戏结束界面
        if self.ShowEndInterface():
            return False

    def isGameOver(self, board, size):
        '''判断游戏是否结束'''
        num_cells = size * size
        for i in range(num_cells-1):
            if board[i] != i:
                return False
        return True

    def moveR(self, board, blank_cell_idx, num_cols):
        '''将空白Cell左边的Cell右移到空白Cell位置'''
        if blank_cell_idx % num_cols == 0:
            return blank_cell_idx
        board[blank_cell_idx -
              1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-1]
        return blank_cell_idx - 1

    def moveL(self, board, blank_cell_idx, num_cols):
        '''将空白Cell上边的Cell下移到空白Cell位置'''
        if (blank_cell_idx+1) % num_cols == 0:
            return blank_cell_idx
        board[blank_cell_idx +
              1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+1]
        return blank_cell_idx + 1

    def moveD(self, board, blank_cell_idx, num_cols):
        if blank_cell_idx < num_cols:
            return blank_cell_idx
        board[blank_cell_idx-num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-num_cols]
        return blank_cell_idx - num_cols

    def moveU(self, board, blank_cell_idx, num_rows, num_cols):
        '''将空白Cell下边的Cell上移到空白Cell位置'''
        if blank_cell_idx >= (num_rows-1) * num_cols:
            return blank_cell_idx
        board[blank_cell_idx+num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+num_cols]
        return blank_cell_idx + num_cols

    def CreateBoard(self, num_rows, num_cols, num_cells):
        '''获得打乱的拼图'''
        board = []
        for i in range(num_cells):
            board.append(i)
        # 去掉右下角那块
        blank_cell_idx = num_cells - 1
        board[blank_cell_idx] = -1
        for i in range(Config.NUMRANDOM):
            # 0: left, 1: right, 2: up, 3: down
            direction = random.randint(0, 3)
            if direction == 0:
                blank_cell_idx = self.moveL(board, blank_cell_idx, num_cols)
            elif direction == 1:
                blank_cell_idx = self.moveR(board, blank_cell_idx, num_cols)
            elif direction == 2:
                blank_cell_idx = self.moveU(
                    board, blank_cell_idx, num_rows, num_cols)
            elif direction == 3:
                blank_cell_idx = self.moveD(board, blank_cell_idx, num_cols)
        return board, blank_cell_idx

    def ShowEndInterface(self) -> bool:
        self.screen.blit(self.image, (0, 0))
        title = self.min_font.render(
            '恭喜，你是真正的 ikun, R键 - 重新开始', True, Config.RED
        )
        rect = title.get_rect()
        rect.midtop = (Config.SCREENSIZE[0] / 2, Config.SCREENSIZE[1] / 2)
        self.screen.blit(title, rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN and event.key == ord('r'):
                    return False

    def ShowStartInterface(self) -> int:
        '''显示游戏开始界面'''
        mid_width = Config.SCREENSIZE[0] / 2
        mid_high = Config.SCREENSIZE[1] / 2.0
        self.screen.blit(self.image, (0, 0))
        title = self.max_font.render('拼图游戏 - ikun 版', True, Config.RED)
        content1 = self.min_font.render('R键 - 重新开始', True, Config.BLUE)
        content2 = self.min_font.render('H键 - 5*5模式', True, Config.BLUE)
        content3 = self.min_font.render('M键 - 4*4 模式', True, Config.BLUE)
        content4 = self.min_font.render('L键 - 3*3 模式', True, Config.BLUE)
        trect = title.get_rect()
        trect.midtop = (mid_width, Config.SCREENSIZE[1] / 10)
        crect1 = content1.get_rect()
        crect1.midtop = (mid_width, mid_high)
        crect2 = content2.get_rect()
        crect2.midtop = (mid_width, mid_high * 1.2)
        crect3 = content3.get_rect()
        crect3.midtop = (mid_width, mid_high * 1.4)
        crect4 = content4.get_rect()
        crect4.midtop = (mid_width, mid_high * 1.6)
        self.screen.blit(title, trect)
        self.screen.blit(content1, crect1)
        self.screen.blit(content2, crect2)
        self.screen.blit(content3, crect3)
        self.screen.blit(content4, crect4)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                elif event.type == pygame.KEYDOWN and event.key in Config.START_KEYMAP:
                    return Config.START_KEYMAP[event.key]
            pygame.display.update()


while PuzzlePiecesGame().run():
    print("重新开始")
