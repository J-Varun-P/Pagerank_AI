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
    probability_distribution = {}
    if len(corpus[page]) == 0:
        for i in corpus:
            probability_distribution[i] = 1 / len(corpus)
        return probability_distribution
    n1 = len(corpus[page])
    n2 = len(corpus)
    for i in corpus[page]:
        print(f"In corpus page {i}")
        probability_distribution[i] = damping_factor / n1
    for i in corpus:
        if i not in probability_distribution:
            probability_distribution[i] = (1 - damping_factor) / n2
        else:
            probability_distribution[i] = probability_distribution[i] + (1 - damping_factor) / n2
    return probability_distribution
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print("-------corpus-------")
    print("\n\n")
    print(corpus)
    print("\n\n")
    print("-------corpus-------")
    print("\n\n\n")
    corpus_page = []
    for i in corpus:
        corpus_page.append(i)
    #print(corpus[0])
    page = corpus_page[random.randint(0,len(corpus_page)-1)]
    print("-------corpus page-------")
    print("\n\n")
    print(page)
    print("\n\n")
    print("-------corpus page-------")
    print("\n\n\n")
    z = {}
    for i in corpus:
        z[i] = 0
    for i in range(n):
        probability_distribution = transition_model(corpus,page,damping_factor)
        print("-------probability distribution-------")
        print("\n\n")
        print(probability_distribution)
        print("\n\n")
        delete_me_later = 0
        for i1 in probability_distribution:
            delete_me_later += probability_distribution[i1]
        print(f"The value added is {delete_me_later}")
        print("-------probability distribution-------")
        print("\n\n\n")
        x1 = []
        x2 = []
        for y in probability_distribution:
            x1.append(y)
        for y in x1:
            x2.append(probability_distribution[y])
        """
        for y in range(len(probability_distribution)):
            x1.append(probability_distribution[y][0])
            x2.append(probability_distribution[y][1])
        """
        page = random.choices(x1, weights=x2)[0]
        z[page] += 1
    for i in corpus:
        z[i] /= n
    print("-------z-------")
    print("\n\n")
    print(z)
    print("\n\n")
    print("-------z-------")
    print("\n\n\n")
    return z

    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    x1 = {}
    z = []
    for x in corpus:
        x1[x] = 1 / len(corpus)
        z.append(x)
    check = 1
    while check == 1:
        check = 0
        for x in z:
            temp1 = ( 1 - damping_factor ) / len(corpus)
            for y in z:
                if x in corpus[y]:
                    temp1 = temp1 + (damping_factor) * x1[y] / len(corpus[y])
                elif len(corpus[y]) == 0:
                    temp1 = temp1 + ( damping_factor * x1[y] / len(corpus) )
            if x1[x] - temp1 >= 0.001 or temp1 - x1[x] >= 0.001:
                check = 1
            x1[x] = temp1
    for x in corpus:
        print(x,len(corpus[x]))
    return x1
    #raise NotImplementedError


if __name__ == "__main__":
    main()
