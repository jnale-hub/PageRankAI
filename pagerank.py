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
    
    File structure
    {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

    """

    # Initialize the probability distribution
    prob_distribution = {}

    # Get the current page 
    current_page = corpus[page]
    # Links from current page
    num_links = len(current_page)

    # Get the number of pages on corpus
    num_pages = len(corpus)

    # Probability of all pages in the corpus
    all_page_prob = (1 - damping_factor) / num_pages

    for prob_value in corpus:  # Assign the prob value of pages in corpus
        prob_distribution[prob_value] = all_page_prob

    if current_page:
        for prob_value in current_page:  # Assign the prob value of the links in the current page
            prob_distribution[prob_value] += damping_factor / num_links

    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Create a dictionary from the page in the corpus with a default value of 0
    pagerank = dict.fromkeys(corpus, 0)

    # Create a list of all page names
    all_pages = list(corpus.keys())

    # Get a random page choice
    page = random.choice(all_pages)

    # Iterate for n 
    for i in range(n):
        
        # Use the transition_model function
        current_dist = transition_model(corpus, page, damping_factor)

        # Calculate the pagerank estimates
        # (5 * 0.2 + 0.1) / 6 = 0.25
        for page_value in pagerank:
            pagerank[page_value] = (i * pagerank[page_value] + current_dist[page_value]) / (i + 1)

        # Choose the next page based in probabilities
        page = random.choices(all_pages, weights=[pagerank[p] for p in all_pages])[0]

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)

    # Initialize a distribution dictionary, with equal value on each page
    distribution = {page: (1.0 / num_pages) for page in corpus}

    # Set a stopping point if the changes are not greater 
    threshold = 0.001

    while True:
        new_distribution = {}
        max_change = 0

        for page in corpus:
            # Calculate the new pagerank value for the current page
            new_rank = ((1 - damping_factor)/num_pages) + (damping_factor * get_sum(corpus, distribution, page))
            
            new_distribution[page] = new_rank

            # Use abs to either positive or negative
            change = abs(distribution[page] - new_rank)

            # Get the maximum number among them
            max_change = max(max_change, change)

        distribution = new_distribution

        # If the chane is smaller than the threshold, stop the loop
        if max_change < threshold:
            break

    return distribution

def get_sum(corpus, distribution, page):
    result = 0
    for p in corpus:
        if page in corpus[p]:
            result += distribution[p] / len(corpus[p])
    return result

if __name__ == "__main__":
    main()
