import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP PP | NP VP ConjP
NP -> N | Det NP | Det AdjP NP | AdjP NP 
AdjP -> Adj | Adj AdjP | AdjP Conj AdjP
AdvP -> Adv | Adv AdvP | Adv ConjP
ConjP -> Conj | Conj NP | Conj VP | Conj NP VP
PP -> P | P NP | P AdvP | P VP | P NP AdvP
VP -> V | VP NP | AdvP VP NP | VP AdvP NP | VP PP | VP AdvP VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Parses sentence as subsentences according to punctuation
    words = nltk.tokenize.word_tokenize(sentence)
    # List for words containing at least one letter
    contains_letter = []
    for word in words:
        # Flag for keeping track of wether it has a letter
        alphabetical = False
        for letter in word:
            if letter.isalpha():
                # If letter is found break and add letter
                alphabetical = True
                break
            
        if alphabetical:
            contains_letter.append(word.lower())
                
    return contains_letter


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    # Look at all available subtrees
    subtrees = tree.subtrees()
    for subtree in subtrees:
        # Only add nouns
        if subtree.label() == "N":
            chunks.append(subtree)
    
    return chunks


if __name__ == "__main__":
    main()
