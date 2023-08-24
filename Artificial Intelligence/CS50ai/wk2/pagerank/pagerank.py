import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Probability distribution dictionary
    probs = {}
    n_links = len(corpus[page])
    
    # Follow formula if n_links is not 0
    if n_links != 0:
        # Assign a random factor to all keys in dict
        for p in corpus.keys():
            probs[p] = (1 - damping_factor)/len(corpus.keys())

        # Get outgoing links from a page and add probability of visiting each link
        for link in corpus[page]:
            probs[link] += damping_factor/n_links

    # Assign every page equal probability since no outgoin links were found
    else:
        for p in corpus.keys():
            probs[p] = 1/len(corpus.keys())
    
    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # What you want to do is start at a page selected at random
    # Make n moves around the corpus
    # For each step make sure to record the result
    # Return the proportions of times every page was visited
    
    # Select a page at random
    pages = [p for p in corpus.keys()]
    page = random.choice(pages)
    moves = [page]
    count = {page: 1}
    
    # Iterate n times and move along corpus
    for i in range(n - 1):
        # Get probability distribution
        distribution = transition_model(corpus, page, damping_factor)
        
        # Get probabilities and keys from distribution
        weights = [w for w in distribution.values()]
        ks = [k for k in distribution.keys()]
        
        # Select page according to probability
        page = random.choices(ks, weights)
        page = page[0]
        
        moves.append(page)
        
        # Add to count dictionary
        if page in list(count.keys()):
            count[page] += 1
        else:
            count[page] = 1
        
    # Get values as coefficients
    tot = 0
    for key, value in count.items():
        count[key] = value / 10000
        tot += count[key]
    
    return count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Return theoretical PageRank value
    length = len(corpus.keys())
    probs = {}
    
    # Assign each page a rank of 1/(n_pages)
    for k in corpus.keys():
        probs[k] = 1/length
    
    flag = True
    # Iteratively update each rank until no further significative changes are made
    while flag:
        # Grab a page
        for p in probs.keys():
            # Grab old proability
            old_prob = probs[p]
            # Calculate first part of equation
            new_prob = (1 - damping_factor)/length
            weights = 0
            
            for page in probs.keys():
                if page == p:
                    continue
                
                links_to = corpus[page]
                if p not in links_to:
                    continue
                
                n_links = len(corpus[page])
                        
                if n_links != 0:
                    weights += probs[page] / n_links
                else:
                    weights += probs[page] / length
            
            new_prob = new_prob + damping_factor * weights
            probs[p] = new_prob
                        
            # If changes in probability are no longer significant break loop
            if abs(old_prob - new_prob) < 0.0000000001:
                flag = False
    
    return probs


if __name__ == "__main__":
    main()
