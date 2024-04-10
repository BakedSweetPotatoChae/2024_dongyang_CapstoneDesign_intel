import tkinter as tk
import random

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 색깔 정의
WHITE = "#ffffff"
BLACK = "#000000"

class BlockBreaker:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=WHITE)
        self.canvas.pack()

        self.ball = self.canvas.create_oval(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 10, fill=BLACK)
        self.paddle = self.canvas.create_rectangle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 20, SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT - 10, fill=BLACK)

        self.blocks = []
        block_width = 80
        block_height = 30
        for row in range(5):
            for col in range(10):
                x0 = col * (block_width + 5) + 30
                y0 = row * (block_height + 5) + 30
                x1 = x0 + block_width
                y1 = y0 + block_height
                block = self.canvas.create_rectangle(x0, y0, x1, y1, fill=BLACK)
                self.blocks.append(block)

        self.ball_speed = [5, 5]
        self.root.bind("<Left>", self.move_paddle_left)
        self.root.bind("<Right>", self.move_paddle_right)

    def move_paddle_left(self, event):
        self.canvas.move(self.paddle, -5, 0)

    def move_paddle_right(self, event):
        self.canvas.move(self.paddle, 5, 0)

    def update(self):
        self.canvas.move(self.ball, self.ball_speed[0], self.ball_speed[1])

        ball_pos = self.canvas.coords(self.ball)
        paddle_pos = self.canvas.coords(self.paddle)

        if ball_pos[0] <= 0 or ball_pos[2] >= SCREEN_WIDTH:
            self.ball_speed[0] *= -1
        if ball_pos[1] <= 0:
            self.ball_speed[1] *= -1
        if ball_pos[0] >= paddle_pos[0] and ball_pos[2] <= paddle_pos[2] and ball_pos[3] >= paddle_pos[1]:
            self.ball_speed[1] *= -1
        
        for block in self.blocks[:]:
            block_pos = self.canvas.coords(block)
            if ball_pos[0] >= block_pos[0] and ball_pos[2] <= block_pos[2] and ball_pos[3] >= block_pos[1] and ball_pos[1] <= block_pos[3]:
                self.blocks.remove(block)
                self.canvas.delete(block)
                self.ball_speed[1] *= -1

        if len(self.blocks) == 0:
            self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text="Game Over", fill=BLACK, font=("Helvetica", 24))
            self.root.after_cancel(self.update_job)

        self.update_job = self.root.after(16, self.update)

    def start(self):
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("블록깨기 게임")
    game = BlockBreaker(root)
    game.start()
    root.mainloop()