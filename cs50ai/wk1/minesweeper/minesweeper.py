import itertools
import random
from termcolor import colored


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
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)
            self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.safes.add(cell)
        

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
            
    
    def updater(self):
        """
        Updates sentences if new safe cells mines can be added.
        """
        for sntc in self.knowledge:
            # Check if length of set of cells equals count
            if sntc.count == len(sntc.cells):
                # If it does then go ahead and mark all cells therein as mines
                # List needs to be created due to iterable changing size
                CellsToMark = []
                for c in sntc.cells:
                    CellsToMark.append(c)
                
                for c in CellsToMark:
                    self.mark_mine(c)
                    
            # Check if count equals zero and there are still cells remaining
            if sntc.count == 0 and len(sntc.cells) != 0:
                # If so mark all cells as safe
                # List needs to be created due to iterable changing size
                CellsToMark = []
                for c in sntc.cells:
                    CellsToMark.append(c)

                for c in CellsToMark:
                    self.mark_safe(c)
            

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function:
            1) marks the cell as a move that has been made
            2) marks the cell as safe
            3) adds a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
            5) marks any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
        """
        # Add current move to moves made and mark as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        # Iterate over a 3x3 surrounding move and add cells if they're in bounds        
        CellsToAdd = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                
                if cell[0] + i > (self.height - 1) or cell[0] + i < 0:
                    continue
                elif cell[1] + j > (self.width - 1) or cell[1] + j < 0:
                    continue
                else:
                   CellsToAdd.add((cell[0] + i, cell[1] + j))
        
        # If count is zero mark everything surrounding as safe
        if count == 0:
            for c in CellsToAdd:
                self.mark_safe(c)
        
        InvalidCells = set()
        # For each cell added make sure to only add cells that are uncertain
        for c in CellsToAdd:
            if c in self.mines:
                count -= 1
                InvalidCells.add(c)
                
            elif c in self.safes:
                InvalidCells.add(c)
        
        for c in InvalidCells:
            CellsToAdd.remove(c)
            
        # Add sentence to KB
        self.knowledge.append(Sentence(CellsToAdd, count))
        
        # Keep track of difference sets created, avoid loop
        down_to = []
        
        # Grab sentence1
        for sntc1 in self.knowledge:
            # Grab sentence2
            for sntc2 in self.knowledge:
                # If the sentences are equal
                if sntc1.cells == sntc2.cells:
                    # Move on
                    continue
                # If sentence1 is subset of sentence2
                elif sntc1.cells.issubset(sntc2.cells):
                    # If subset hasn't been created before
                    if (sntc2.cells.difference(sntc1.cells)) not in down_to:
                        down_to.append((sntc2.cells.difference(sntc1.cells)))
                        # Get the difference of sentence2 with respect to sentence1
                        diff = sntc2.cells.difference(sntc1.cells)
                        # Assign the count resulting of subtracting count of sentence1 from count of sentence2
                        if sntc2.count > sntc1.count:
                            cnt = sntc2.count - sntc1.count
                        else:
                            cnt = sntc1.count - sntc2.count
                        # Create a new sentence for the difference
                        self.knowledge.append(Sentence(diff, cnt))
                elif sntc2.cells.issubset(sntc1.cells):
                    # If subset hasn't been created before
                    if (sntc1.cells.difference(sntc2.cells)) not in down_to:
                        down_to.append((sntc1.cells.difference(sntc2.cells)))
                        # Get the difference of sentence1 with respect to sentence2
                        diff = sntc1.cells.difference(sntc2.cells)
                        # Assign the count resulting of subtracting count of sentence1 from count of sentence2
                        if sntc2.count > sntc1.count:
                            cnt = sntc2.count - sntc1.count
                        else:
                            cnt = sntc1.count - sntc2.count
                        # Create a new sentence for the difference
                        self.knowledge.append(Sentence(diff, cnt))
                        
        # Update safe cells and mines
        self.updater()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        """
        for saf in self.safes:
            if saf not in self.moves_made:
                return saf
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Chooses a move at random if no mades have been made.
        Chooses among non-made non-mines if moves have already been made.
        """
        if len(self.moves_made) == 0:
            return (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
        
        possible = []
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    possible.append(move)
                    
        
        if len(possible) != 0:
            move = possible[random.randint(0, len(possible) - 1)]
            return move    
        
        return None    
