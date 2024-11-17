import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

        return set()    


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()
    

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_neighbors(self, cell):
        """
        Returns all valid neighbors of a given cell.
        """
        row, col = cell
        neighbors = set()
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # Skip the cell itself
                if (i, j) == cell:
                    continue
                # Check bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))
        return neighbors

    def check_safes_and_mines(self, cells):
        """
        Removes cells that are known to be mines or safe from the input set.
        """
        filtered_cells = set()
        for cell in cells:
            if cell not in self.mines and cell not in self.safes:
                filtered_cells.add(cell)
        return filtered_cells
    
    def update_kb(self):

        changes_made = True
        while changes_made:
            changes_made = False   

              
            for sentence in self.knowledge[:]:
                # Marcar celdas como minas si todas las celdas de la sentencia son minas
                known_mines = sentence.known_mines()
                if known_mines:
                    for mine in known_mines.copy():
                        if mine not in self.mines:
                            self.mark_mine(mine)
                            changes_made = True 

                # Marcar celdas como seguras si todas las celdas de la sentencia son seguras
                known_safes = sentence.known_safes()
                if known_safes:
                    for safe in known_safes.copy():
                        if safe not in self.safes:
                            self.mark_safe(safe)
                            changes_made = True   

            # Inferir nuevas sentencia
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                        # Inferir nueva sentencia
                        inferred_cells = sentence2.cells - sentence1.cells
                        inferred_count = sentence2.count - sentence1.count
                        inferred_sentence = Sentence(inferred_cells, inferred_count)
                        
                        # Agregar nueva sentencia si no está en el conocimiento
                        if inferred_sentence not in self.knowledge:
                            self.knowledge.append(inferred_sentence)
                            changes_made = True 
            

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made
        if cell not in self.moves_made:
            self.moves_made.add(cell)

        # mark the cell as safe
        if cell not in self.safes:
            self.mark_safe(cell)  

        # Add a new sentence to the AI's knowledge
        neighbors = self.get_neighbors(cell)
        filtered_neighbors = self.check_safes_and_mines(neighbors)
        new_sentence = Sentence(filtered_neighbors,count)

        if count == 0:
            for cell in filtered_neighbors:
                self.mark_safe(cell)
                self.update_kb()

        elif len(filtered_neighbors) == count:
            for cell in filtered_neighbors:
                self.mark_mine(cell)
                self.update_kb()

        else:
            self.knowledge.append(new_sentence) 
            self.update_kb()

                                               

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []

        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    possible_moves.append((i,j))

        if len(possible_moves) > 0:
            return random.choice(possible_moves)
        else:
            return None