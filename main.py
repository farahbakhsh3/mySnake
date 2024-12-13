import pygame
import random


class SnakeGame:
    def __init__(self):
        self.init_game()

    def init_game(self):
        pygame.init()

        self.block_size = 30
        self.width, self.height = 20 * self.block_size, 20 * self.block_size
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)

        self.snake_pos = [0, 0]
        self.snake_body = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.speed = 5
        self.max_Speed = 15

        self.walls = []
        self.wall_speed = 2

        self.difficulty = self.select_difficulty()
        if self.difficulty == "MEDIUM":
            self.max_Speed = 20
            self.create_walls(movable=False)
        elif self.difficulty == "HARD":
            self.max_Speed = 30
            self.create_walls(movable=True)

        self.fruit_pos = self.random_fruit_pos()
        self.fruit_spawn = True

        self.score = 0
        self.game_over = False

    def select_difficulty(self):
        difficulty = None
        while difficulty not in ["EASY", "MEDIUM", "HARD"]:
            self.win.fill(self.black)
            message = self.font.render(
                "Select Difficulty: EASY, MEDIUM, HARD", True, self.white
            )
            self.win.blit(message, [self.width // 6, self.height // 3])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        difficulty = "EASY"
                    elif event.key == pygame.K_m:
                        difficulty = "MEDIUM"
                    elif event.key == pygame.K_h:
                        difficulty = "HARD"
        return difficulty

    def create_walls(self, movable=False):
        y = random.randrange(0, self.height, self.block_size)
        direction = "UP"
        for i in range(0, self.width, self.block_size):
            x = random.randint(0, 10) > 9
            if x:
                y = random.randrange(0, self.height, self.block_size)
                direction = random.choice(["UP", "DOWN"])

            wall = pygame.Rect(i, y,
                               self.block_size, self.block_size)
            self.walls.append(
                {
                    "rect": wall,
                    "movable": movable,
                    "direction": direction,
                }
            )

    def random_fruit_pos(self):
        should_Make_New_Apple = True
        while should_Make_New_Apple:
            pos = [random.randrange(0, self.width, self.block_size),
                   random.randrange(0, self.height, self.block_size)]

            if pos in self.snake_body:
                continue

            should_Make_New_Apple = False
            for wall in self.walls:
                if wall["rect"].colliderect(pygame.Rect(*pos,
                                                        self.block_size,
                                                        self.block_size)):
                    should_Make_New_Apple = True
                    break

        return pos

    def show_score(self, color):
        score_surf = self.font.render("Score: " + str(self.score), True, color)
        score_rect = score_surf.get_rect()
        self.win.blit(score_surf, score_rect)

    def show_speed(self, color):
        speed_surf = self.font.render("Speed: " + str(self.speed), True, color)
        speed_rect = speed_surf.get_rect()
        speed_rect.x = self.width - speed_rect.width
        self.win.blit(speed_surf, speed_rect)

    def game_over_message(self):
        self.win.fill(self.black)
        message = self.font.render(
            "Do you want to play again? Y/N", True, self.white)
        self.win.blit(message, [self.width // 6, self.height // 3])
        pygame.display.update()

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != "DOWN":
                self.change_to = "UP"
            elif event.key == pygame.K_DOWN and self.direction != "UP":
                self.change_to = "DOWN"
            elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                self.change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                self.change_to = "RIGHT"

    def update_direction(self):
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move_snake(self):
        if self.direction == "UP":
            self.snake_pos[1] -= self.block_size
        elif self.direction == "DOWN":
            self.snake_pos[1] += self.block_size
        elif self.direction == "LEFT":
            self.snake_pos[0] -= self.block_size
        elif self.direction == "RIGHT":
            self.snake_pos[0] += self.block_size

        if self.snake_pos[0] < 0:
            self.snake_pos[0] = self.width - self.block_size
        elif self.snake_pos[0] > self.width - self.block_size:
            self.snake_pos[0] = 0
        elif self.snake_pos[1] < 0:
            self.snake_pos[1] = self.height - self.block_size
        elif self.snake_pos[1] > self.height - self.block_size:
            self.snake_pos[1] = 0

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.fruit_pos:
            self.score += 1
            self.speed += 1
            self.speed = min(self.speed, self.max_Speed)
            self.fruit_spawn = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawn:
            self.fruit_pos = self.random_fruit_pos()
        self.fruit_spawn = True

    def move_walls(self):
        for wall in self.walls:
            if wall["movable"]:
                if wall["direction"] == "UP":
                    wall["rect"].y -= self.wall_speed
                    if wall["rect"].y <= 0:
                        wall["direction"] = "DOWN"
                elif wall["direction"] == "DOWN":
                    wall["rect"].y += self.wall_speed
                    if wall["rect"].y >= self.height - self.block_size:
                        wall["direction"] = "UP"

    def check_collision(self):
        for block in self.snake_body[1:]:
            if self.snake_pos == block:
                self.game_over = True

        for wall in self.walls:
            for block in self.snake_body:
                if wall["rect"].colliderect(pygame.Rect(*block,
                                                        self.block_size,
                                                        self.block_size)):
                    self.game_over = True

    def draw_elements(self):
        self.win.fill(self.black)

        for wall in self.walls:
            pygame.draw.rect(self.win, self.white, wall["rect"])
            pygame.draw.rect(self.win, self.black, wall["rect"], 1)

        pygame.draw.rect(self.win, self.red,
                         pygame.Rect(*self.fruit_pos,
                                     self.block_size,
                                     self.block_size))
        pygame.draw.rect(self.win, self.black,
                         pygame.Rect(*self.fruit_pos,
                                     self.block_size,
                                     self.block_size), 1)

        first = True
        for pos in self.snake_body:
            color = self.green
            if first:
                color = self.yellow
                first = False
            pygame.draw.rect(self.win, color,
                             pygame.Rect(*pos,
                                         self.block_size,
                                         self.block_size))
            pygame.draw.rect(self.win, self.black,
                             pygame.Rect(*pos,
                                         self.block_size,
                                         self.block_size), 1)

        self.show_score(self.white)
        self.show_speed(self.white)

        pygame.display.update()

    def reset_game(self):
        self.init_game()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.handle_keys(event)

            self.update_direction()
            self.move_snake()
            if self.difficulty == "HARD":
                self.move_walls()

            self.draw_elements()
            self.check_collision()

            if self.game_over:
                pygame.time.wait(1000)
                self.win.fill(self.black)
                self.show_score(self.red)
                pygame.display.flip()
                self.game_over_message()
                play_again = False
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                play_again = True
                            elif event.key == pygame.K_n:
                                pygame.quit()
                                quit()
                    if play_again:
                        self.reset_game()
                        break

            self.clock.tick(self.speed)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
