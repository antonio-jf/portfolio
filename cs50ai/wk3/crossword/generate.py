import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Check variable length
        for var in self.domains:
            l = var.length
            # Get all possible domain values
            # Copied due to iterable changing size during loop
            doms = [k for k in self.domains[var]]
            for dom in doms:
                # If length is not consistent with domain value, remove it
                if len(dom) != l:
                    self.domains[var].remove(dom)
                    
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]

        if not overlap:
            return False
        
        # Grab each component of the overlap
        xth = overlap[0]
        yth = overlap[1]
        
        # Revision flag
        revision = False
        
        # Get domain of y
        ywords = self.domains[y]
        # Look at all possible letters on Y's overlap position
        yletters = [word[yth] for word in ywords]
        
        # Grab X and look at all possible letters on X's overlap position
        words = [w for w in self.domains[x]]
        for word in words:
            # Compare to Y's to only keep possible values
            if word[xth] not in yletters:
                self.domains[x].remove(word)
                # Update flag
                revision = True
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        if arcs == None:
            # Populate arcs initially to contain all arcs
            arcs = []
            for var1 in self.domains:                    
                neighbors = self.crossword.neighbors(var1)
                for neighbor in neighbors:
                    arcs.append((var1, neighbor))
                    
                if not neighbors:
                    continue
    
        # Iterate over all arcs and enforce arc consistency
        while len(arcs) != 0:
            # After every iteration slice array
            current = arcs[0]    
            arcs = arcs[1:]
            
            # Make variables arc consistent
            if self.revise(current[0], current[1]):
                # Not all variables should be removed from domain
                if len(self.domains[current[0]]) == 0:
                    return False
                
                # Get neighbors for current variable
                neighbors = self.crossword.neighbors(current[0])
                
                # Add arcs for neighbors to check again after removing variables
                ArcsToAdd = []
                for neighbor in neighbors:
                    if neighbor != current[1]:
                        ArcsToAdd.append((neighbor, current[0]))
                
                for i in ArcsToAdd:
                    arcs.append(i)
                        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for ky in self.domains.keys():
            # A particular key is not in the assignment
            if ky not in assignment.keys():
                return False
            
            # There is no assignment for a key
            if not assignment[ky]:
                return False
        
        # All variables have been assigned
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # Assignment must be unique
        avail_words = set(self.crossword.words)
        for ky in assignment.keys():
            if assignment[ky] in avail_words:
                avail_words.remove(assignment[ky])
            else:
                return False
        # Assignment must fit the amount of letters
            if ky.length != len(assignment[ky]):
                return False
        # No character conflicts
            # Get key neighbors
            nvals = self.crossword.neighbors(ky)
            # If there are neighbors check for overlapping cell
            if nvals:
                for nval in nvals:
                    # Check wether variable is already in assignment
                    if nval in assignment.keys():
                        # Get overlap of variable with current key
                        ovlp = self.crossword.overlaps[ky, nval]
                        if assignment[ky][ovlp[0]] != assignment[nval][ovlp[1]]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """        
        # Get a variables domain
        possibles = self.domains[var]
        
        rules_out = []
        # Get overlaps for particular variable
        for possible in possibles:
            possible_count = 0
            # Get also neighbors
            for neighbor in self.crossword.neighbors(var):
                # Only consider neighbors who are not already in the assignment
                if neighbor in assignment.keys():
                    continue
                
                overlap = self.crossword.overlaps[var, neighbor]   
                neighbor_possibles = self.domains[neighbor]      
                   
                # Iterate over neighbors' domain values
                for neighbor_possible in neighbor_possibles:
                    # Check every neighbor to see how many variables it would rule out
                    if possible[overlap[0]] != neighbor_possible[overlap[1]]:
                        possible_count += 1
                
            rules_out.append((possible, possible_count))
                        
        # Reorder values
        rules_out = sorted(rules_out, key=lambda x: x[1])
        rules = [r[0] for r in rules_out]
        
        return rules
        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        availables = []
        
        for var in self.domains.keys():
            # Add all variables not assigned
            if var not in assignment.keys():
                # Also add number of domains available and number of neighbors for tiebreakers
                availables.append((var, len(self.domains[var]), len(self.crossword.neighbors(var))))
    
        # Reorder values by amount of domain values and neighbors
        avails = []
        min = float('inf')
        
        for available in availables:
            if available[1] < min:
                min = available[1]
                avails = [available]
            elif available[1] == min:
                avails.append(available)
                        
        if len(avails) > 1:
            avails = sorted(avails, key=lambda x: x[2], reverse=True)
        
        # Return the first element
        return avails[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check for complete assignment
        if self.assignment_complete(assignment):
            return assignment
    
        # Select available variable
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            # Create copy to not affect original assignment
            AssignmentCopy = copy.copy(assignment)
            AssignmentCopy[var] = val
            # Check for consistency
            if self.consistent(AssignmentCopy):
                # Assign in original assignment
                assignment[var] = val
                # Recursion for next unassigned variables
                result = self.backtrack(assignment)
                # There are no more variables to assign, return assignment
                if result:
                    return assignment
            # No consistency, delete assignment and try again
            del AssignmentCopy[var]
        # An assignment was not found
        return False 
        

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
