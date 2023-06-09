from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # Since he can't be both types he's obviously a Knave
    Implication(And(AKnight, AKnave), AKnight),
    Implication(Not(And(AKnight, AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # If A's statement were true he'd be a knight, which is impossible
    Implication(And(AKnave, BKnave), AKnight),
    Implication(Not(And(AKnave, BKnave)), AKnave)
    # I think we don't have enough information about B though
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # Validate A's statement
    Implication(And(AKnight, BKnight), And(AKnight, BKnave)),
    Implication(And(AKnave, BKnave), And(AKnight, BKnave)),
    # Validate B's statement
    Implication(Not(And(AKnight, BKnight)), And(BKnight, AKnave)),
    Implication(Not(And(AKnave, BKnave)), And(BKnight, AKnave))    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    
    # If C called right A then both are knights
    Biconditional(AKnight, CKnight),
    # If B is knight then both A and C are Knaves
    Implication(BKnight, And(CKnave, AKnight)),
    # If A is knight the B can't be knight and also proves that C is indeed knight
    Implication(AKnight, And(BKnave, CKnight)),
    # Finally if A is somehow knave then B would be knight
    Implication(AKnave, BKnight)
     
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
