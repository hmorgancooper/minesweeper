import itertools
import random
#from typing_extensions import clear_overloads


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

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # cell is a known mine from list of mines from MinesweeperAI.mines
        # unknown cell is list of cells from Sentence (self.cells)
        tmp = []
        for unknown_cell in self.cells:
            tmp.append(unknown_cell)
        for unknown_cell in tmp:
            if unknown_cell == cell:
                self.cells.remove(cell)
                self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        tmp = []
        for unknown_cell in self.cells:
            tmp.append(unknown_cell)
        for unknown_cell in tmp:
            if unknown_cell == cell:
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
        self.moves_made.add(cell)
        # mark the cell as safe
        self.mark_safe(cell)
        adj_cells = []
        for a in range(-1, 2, 1):
            for b in range(-1, 2, 1):
                if ((cell[0]+a) in range(self.height) and (cell[1]+b) in range(self.width)) and (a != 0 or b != 0):
                    adj_cells.append((cell[0]+a, cell[1]+b))
        self.generate_new_knowledge_sentence(adj_cells, count)

        # Add new sentences to AI knowledge base if they can be inferred
        changes = 1
        while (changes > 0):
            changes = self.update_with_inferred_sentences()
        return None

    def generate_new_knowledge_sentence(self, adj_cells, count):
        new_knowledge = Sentence(adj_cells, count)
        # Mark additional cells as safe or mines
        for mine in self.mines:
            new_knowledge.mark_mine(mine)
        for safe in self.safes:
            new_knowledge.mark_safe(safe)

        # check if mines or safes can be found from sentence
        if new_knowledge.known_safes():
            tmp = new_knowledge.known_safes().copy()
            for cell in tmp:
                self.mark_safe(cell)
            return
        if new_knowledge.known_mines():
            tmp = new_knowledge.known_mines().copy()
            for cell in tmp:
                self.mark_mine(cell)
            return
        if new_knowledge not in self.knowledge:
            self.knowledge.append(new_knowledge)

    def update_with_inferred_sentences(self):
        changes = self.check_all_sentences_for_known_safes_and_mines()
        changes += self.find_subsets_and_create_new_sentences()
        return changes

    def find_subsets_and_create_new_sentences(self):
        original = len(self.knowledge)
        for i in range(0, len(self.knowledge)):
            for j in range(0, len(self.knowledge)):
                if (i != j):
                    # find matching set
                    matching = self.knowledge[i].cells.intersection(
                        self.knowledge[j].cells).copy()
                    if self.knowledge[j].cells.issubset(self.knowledge[i].cells):
                        not_matching = (
                            self.knowledge[i].cells - self.knowledge[j].cells).copy()
                        if not_matching:
                            new_count = abs(
                                self.knowledge[i].count - self.knowledge[j].count)
                            self.generate_new_knowledge_sentence(
                                not_matching, new_count)
        end = len(self.knowledge)
        return original - end

    def check_all_sentences_for_known_safes_and_mines(self):
        ''' 
        for sentence in knowledge run Sentence.known_safes and Sentence.known_mines
        if not null add to safes/mines
        update all sentences with known safes/ mines
        '''
        changes = 0
        for sentence in self.knowledge:
            if sentence.known_safes():
                changes += 1
                tmp = sentence.known_safes().copy()
                for cell in tmp:
                    self.mark_safe(cell)
            if sentence.known_mines():
                changes += 1
                tmp = sentence.known_mines().copy()
                for cell in tmp:
                    self.mark_mine(cell)
        return changes

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if (cell not in self.moves_made) and (cell not in self.mines):
                return cell
        else:
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
                if ((i, j) not in self.moves_made) and ((i, j) not in self.mines):
                    possible_moves.append((i, j))
        return random.choice(possible_moves)
