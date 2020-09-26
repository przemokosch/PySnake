import pygame
import sys
import random


class Cube:
    def __init__(self, x, y, cell_size):
        self._cell_size = cell_size
        self._x = x
        self._y = y

    @property
    def position(self):
        return self._x, self._y

    def _rect(self):
        return (self._x * self._cell_size[0],
                self._y * self._cell_size[1],
                self._cell_size[0],
                self._cell_size[1])

    def collision(self, cube):
        if self.position == cube.position:
            return True
        return False

    def draw(self, surface, color=(255, 255, 255)):
        rect = pygame.Rect(self._rect())
        pygame.draw.rect(surface, color, rect)


def draw_grid(surface, size, cells):
    single_width = int(size[0] / cells[0])
    single_height = int(size[1] / cells[1])

    for i in range(0, size[0], single_width):
        pygame.draw.line(surface, (255, 255, 255), (i, 0), (i, size[1]))
    for j in range(0, size[1], single_height):
        pygame.draw.line(surface, (255, 255, 255), (0, j), (size[0], j))
    return single_width, single_height


class Snake:
    def __init__(self, cell_size, cells):
        self._cell_size = cell_size
        self._head = [Cube(10, 10, cell_size=self._cell_size)]
        self._dirx = 1
        self._diry = 0
        self.cells = cells
        self._grow = False

    def colides(self):
        for index, cube in enumerate(self._head):
            if index != 0 and self._head[0].position == cube.position:
                return True
        return False

    def set_direction(self, direction):
        if direction == "up" and self._diry != 1:
            self._dirx = 0
            self._diry = -1
            return
        if direction == "down" and self._diry != -1:
            self._dirx = 0
            self._diry = 1
            return
        if direction == "left" and self._dirx != 1:
            self._dirx = -1
            self._diry = 0
            return
        if direction == "right" and self._dirx != -1:
            self._dirx = 1
            self._diry = 0
            return

    def eat(self, snack):
        if snack.position == self._head[0].position:
            snack.randomize()
            self._grow = True

    def move(self):
        x, y = self._head[0].position
        x += self._dirx
        y += self._diry
        if x >= self.cells[0]:
            x = 0
        if x < 0:
            x = self.cells[0] - 1
        if y >= self.cells[1]:
            y = 0
        if y < 0:
            y = self.cells[1] - 1
        self._head.insert(0, Cube(x, y, cell_size=self._cell_size))
        if self._grow:
            self._grow = False
        else:
            self._head.pop()

    def draw(self, surface):
        for elem in self._head:
            elem.draw(surface, color=(0, 255, 0))


class Snack:
    def __init__(self, cell_size, cells):
        self.cells = cells
        self._cell_size = cell_size
        self.randomize()

    def randomize(self):
        x = random.randint(0, self.cells[0] - 1)
        y = random.randint(0, self.cells[0] - 1)
        self._snack = Cube(x, y, cell_size=self._cell_size)

    @property
    def position(self):
        return self._snack.position

    def draw(self, surface):
        self._snack.draw(surface, color=(0, 0, 255))


class GameEngine:
    def __init__(self, size):
        pygame.init()
        # speed = [2, 2]
        # black = 0, 0, 0
        self._cells = (20, 20)
        self._size = size
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._size)
        self._surface = pygame.Surface(self._screen.get_size())
        self._surface = self._surface.convert()
        self._single_size = draw_grid(self._surface, self._size, cells=self._cells)
        self._snake = Snake(self._single_size, self._cells)
        self._snack = Snack(self._single_size, self._cells)

    def update(self):
        self._snake.move()
        if self._snake.colides():
            self._snake = Snake(self._single_size, self._cells)
        self._snake.eat(self._snack)
        self._snake.draw(self._surface)
        self._snack.draw(self._surface)

    def run(self):
        while True:
            self._clock.tick(10)
            self._surface.fill((0, 0, 0))
            draw_grid(self._surface, self._size, self._cells)
            self.handle_keys()
            self.update()
            pygame.display.update()
            self._screen.blit(self._surface, (0, 0))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            if event.key == pygame.K_UP:
                self._snake.set_direction("up")
            if event.key == pygame.K_LEFT:
                self._snake.set_direction("left")
            if event.key == pygame.K_RIGHT:
                self._snake.set_direction("right")
            if event.key == pygame.K_DOWN:
                self._snake.set_direction("down")


def main():
    GameEngine((800, 600)).run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
