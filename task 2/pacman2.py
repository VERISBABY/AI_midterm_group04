import heapq
import pygame
import math

class Maze:
    def __init__(self, grid, pacman_pos, food_positions, pie_positions, teleport_corners):
        self.grid = grid
        self.pacman_pos = pacman_pos
        self.food_positions = set(food_positions)
        self.pie_positions = set(pie_positions)
        self.teleport_corners = teleport_corners

    def is_wall(self, x, y):
        return self.grid[x][y] == '%'

    def teleport(self, x, y):
        return self.teleport_corners.get((x, y), (x, y))

class PacmanAI:
    def __init__(self, maze):
        self.maze = maze

    def heuristic(self, state):
        x, y, food_left, _ = state
        if not food_left:
            return 0
        return min(abs(x - fx) + abs(y - fy) for fx, fy in food_left)

    def a_star_search(self):
        start_state = (self.maze.pacman_pos[0], self.maze.pacman_pos[1],
                       frozenset(self.maze.food_positions), 0)
        frontier = [(self.heuristic(start_state), 0, start_state, [])]
        explored = set()

        while frontier:
            _, cost, current_state, path = heapq.heappop(frontier)
            x, y, food_left, _ = current_state

            if not food_left:
                return path, cost  # Return path and total cost

            if current_state in explored:
                continue
            explored.add(current_state)

            for successor, action, step_cost in self.get_successors(current_state):
                new_cost = cost + step_cost
                heapq.heappush(frontier, (new_cost + self.heuristic(successor),
                               new_cost, successor, path + [action]))

        return None

    def get_successors(self, state):
        x, y, food_left, pie_steps = state
        successors = []
        moves = [(-1, 0, "North"), (1, 0, "South"), (0, -1, "West"), (0, 1, "East")]

        for dx, dy, action in moves:
            nx, ny = x + dx, y + dy
            # Apply teleportation first
            tx, ty = self.maze.teleport(nx, ny)
            # Check if teleported position is within bounds
            if 0 <= tx < len(self.maze.grid) and 0 <= ty < len(self.maze.grid[0]):
                # Check if passable (not wall or pie steps active)
                if not self.maze.is_wall(tx, ty) or pie_steps > 0:
                    new_food = food_left - {(tx, ty)} if (tx, ty) in food_left else food_left
                    new_pie_steps = max(0, pie_steps - 1)
                    if (tx, ty) in self.maze.pie_positions:
                        new_pie_steps = 5
                    successors.append(((tx, ty, new_food, new_pie_steps), action, 1))
        return successors

    def visualize(self, path, pie_image):
        pygame.init()
        cell_size = 30
        width = len(self.maze.grid[0]) * cell_size
        height = len(self.maze.grid) * cell_size
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

        try:
            pie_img = pygame.image.load(pie_image)
            pie_img = pygame.transform.scale(pie_img, (30, 30))
        except Exception as e:
            print(f"Error loading pie image: {e}")
            pie_img = pygame.Surface((30, 30))
            pie_img.fill((255, 0, 255))  # Fallback color

        waiting = True
        font = pygame.font.Font(None, 36)
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

            screen.fill((10, 0, 50))
            text = font.render("Press SPACE to start", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width//2, height//2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            clock.tick(10)

        pacman_x, pacman_y = self.maze.pacman_pos
        food_positions = set(self.maze.food_positions)
        pie_positions = set(self.maze.pie_positions)
        direction = 0
        frame = 0

        for move in path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill((10, 0, 50))

            for i in range(len(self.maze.grid)):
                for j in range(len(self.maze.grid[0])):
                    if self.maze.grid[i][j] == '%':
                        pygame.draw.rect(screen, (0, 128, 0), (j*cell_size, i*cell_size, cell_size, cell_size))
                    elif (i, j) in food_positions:
                        pulse_size = 5 + 3 * math.sin(pygame.time.get_ticks() * 0.005)
                        pygame.draw.circle(screen, (255, 255, 0), (j * cell_size + 15, i * cell_size + 15), int(pulse_size))
                    elif (i, j) in pie_positions:
                        pie_scale = 1 + 0.2 * math.sin(pygame.time.get_ticks() * 0.01)
                        scaled_pie = pygame.transform.scale(pie_img, (int(30 * pie_scale), int(30 * pie_scale)))
                        screen.blit(scaled_pie, (j * cell_size + (30 - scaled_pie.get_width()) // 2, i * cell_size + (30 - scaled_pie.get_height()) // 2))

            if move == "North":
                direction = 90
            elif move == "South":
                direction = 270
            elif move == "West":
                direction = 180
            elif move == "East":
                direction = 0

            center = (pacman_y * cell_size + 15, pacman_x * cell_size + 15)
            eye_offset_x = int(6 * math.cos(math.radians(direction)))
            eye_offset_y = int(-6 * math.sin(math.radians(direction))) - 10  # Adjusted to ensure visibility
            eye_position = (int(center[0] + eye_offset_x), int(center[1] + eye_offset_y))

            mouth_open = (frame % 10) < 4  # Open and close mouth every few frames
            mouth_angle = 30 if mouth_open else 5  # Reduced mouth opening further

            pygame.draw.circle(screen, (255, 255, 0), center, 15)
            pygame.draw.circle(screen, (0, 0, 0), eye_position, 3)
            mouth_rect = pygame.Rect(center[0] - 15, center[1] - 15, 30, 30)
            pygame.draw.arc(screen, (15, 0, 50), mouth_rect,
                            math.radians(direction - mouth_angle),
                            math.radians(direction + mouth_angle), 15)

            pygame.display.flip()
            clock.tick(5)


            if move == "North":
                pacman_x -= 1
            elif move == "South":
                pacman_x += 1
            elif move == "West":
                pacman_y -= 1
            elif move == "East":
                pacman_y += 1

            food_positions.discard((pacman_x, pacman_y))
            pie_positions.discard((pacman_x, pacman_y))
            frame += 1

        pygame.quit()


def parse_maze(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.strip()) for line in f]

    pacman_pos = None
    food = set()
    pies = set()
    teleport_corners = {}

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if rows > 0 and cols > 0:
        corners = [(0, 0), (0, cols-1), (rows-1, 0), (rows-1, cols-1)]
        # Map each corner to its opposite
        teleport_corners[corners[0]] = corners[-1]
        teleport_corners[corners[-1]] = corners[0]
        teleport_corners[corners[1]] = corners[2]
        teleport_corners[corners[2]] = corners[1]

    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell == 'P':
                pacman_pos = (i, j)
            elif cell == '.':
                food.add((i, j))
            elif cell == 'O':
                pies.add((i, j))

    return Maze(grid, pacman_pos, food, pies, teleport_corners)

def pacman():
    file_path = "midterm_04_523K0047/task 2/task02_pacman_example_map.txt"
    maze = parse_maze(file_path)
    pacman_ai = PacmanAI(maze)
    result = pacman_ai.a_star_search()

    if result:
        path, total_cost = result
        print("Solution Path:", path)
        print("Total Cost:", total_cost)
        pacman_ai.visualize(path, 'midterm_04_523K0047/task 2/pie.jpg')
    else:
        print("No solution found.")

if __name__ == "__main__":
    pacman()