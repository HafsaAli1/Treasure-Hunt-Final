import random
from collections import deque

# Initialise the grid size, number of traps, and power-ups
class TreasureHunt:
    def __init__(self, size=5, traps=2, powerups=2):
        self.size = size
        self.traps = traps
        self.powerups = powerups
    # Make the placeholders a dash
        self.grid = [["-" for _ in range(size)] for _ in range(size)]
        self.players = []
    # Place the treasure, traps, and power-ups on the grid
        self.treasure = self.place("T")
        [self.place("L") for _ in range(traps)]
        [self.place("X") for _ in range(powerups)]
        self.turn_index = 0

# Randomly places item on the grid
    def place(self, item):
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            # Check if the cell is empty
            if self.grid[x][y] == "-":
                self.grid[x][y] = item
                return x, y

# Adds a player to the game with a starting position and health.
    def addPlayer(self, name, start_x, start_y):
        if 0 <= start_x < self.size and 0 <= start_y < self.size:
            self.players.append({"name": name, "position": (start_x, start_y), "health": 5})

# Moves the player in the direction you want
    def move(self, player_index, direction):
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        player = self.players[player_index]
        if direction in moves:
            dx, dy = moves[direction]
            x, y = player["position"]
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                player["position"] = (nx, ny)
                self.spaceFunction(player, nx, ny)
            else:
                print("Wrong Move.")

    def spaceFunction(self, player, x, y):
        # Handles the effects of the cell the player lands on.
        cell = self.grid[x][y]
        # If Player finds treasure
        if cell == "T":
            print(f"{player['name']} found the treasure! They win!")
            exit()
        # If player lands on trap
        elif cell == "L":
            player["health"] -= 1
            print(f"{player['name']} stepped on a trap! Health: {player['health']}")
            if player["health"] <= 0:
                print(f"{player['name']} is eliminated.")
                self.players.remove(player)
        # If player lands on powerup
        elif cell == "X":
            player["health"] += 2
            self.grid[x][y] = "-"
            print(f"{player['name']} found a power-up! Health: {player['health']}")

# Displays the grid, including player positions.
    def showGrid(self):
        grid_copy = [row[:] for row in self.grid]
        for i, player in enumerate(self.players):
            x, y = player["position"]
            grid_copy[x][y] = f"P{i + 1}"
        print("\n".join(" ".join(row) for row in grid_copy))

# Performs a binary search on a specific row to find a target.
    def binary(self, row, target):
        start, end = 0, self.size - 1
        while start <= end:
            mid = (start + end) // 2
            if self.grid[row][mid] == target:
                return mid
            elif self.grid[row][mid] < target:
                start = mid + 1
            else:
                end = mid - 1
        return -1

# Finds the shortest path to the treasure using BFS.
    def bfs(self, start):
        queue = deque([start])
        visited = set()
        parent_map = {}
        while queue:
            x, y = queue.popleft()
            # Skip already visited cells
            if (x, y) in visited:
                continue
            visited.add((x, y))
            # Found the treasure
            if self.grid[x][y] == "T":
                path = []
                while (x, y) in parent_map:
                    path.append((x, y))
                    x, y = parent_map[(x, y)]
                return path[::-1]
            # Explore cells that are near
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    parent_map[(nx, ny)] = (x, y)
        return []

# Explores paths using DFS.
    def dfs(self, current, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        x, y = current
        # Found the treasure
        if self.grid[x][y] == "T":
            return path + [current]
        visited.add(current)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                result = self.dfs((nx, ny), visited, path + [current])
                if result: return result
        return []

# Starts the game
    def play(self):
        while self.players:
            self.showGrid()
            player = self.players[self.turn_index]
            print(f"{player['name']}'s turn (Health: {player['health']})")
            action = input("Choose action: \n1-Move \n2-BFS \n3-DFS \n4-Binary Search ").strip()
            if action == "1":
                direction = input("Enter direction (up/down/left/right): ").strip()
                self.move(self.turn_index, direction)
            elif action == "2":
                print("Path:", self.bfs(player["position"]))
            elif action == "3":
                print("Path:", self.dfs(player["position"]))
            elif action == "4":
                row = int(input("Enter row to search: "))
                target = input("Enter target (T/X): ")
                print("Found at column:", self.binary(row, target))
            else:
                print("Invalid action.")
            self.turn_index = (self.turn_index + 1) % len(self.players)


game = TreasureHunt()
game.addPlayer("Player 1", 0, 0)
game.addPlayer("Player 2", 4, 4)
game.play()
