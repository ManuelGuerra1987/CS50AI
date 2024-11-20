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

    {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
    """
    probability_distribution = {}

    links_current_page = corpus[page]
    num_links = len(links_current_page)
    num_all_pages = len(corpus)

    #With probability `damping_factor`, choose a link at random linked to by `page`
    for link in links_current_page:
        probability_distribution[link] = damping_factor/num_links


    #With probability `1 - damping_factor`, choose a link at random chosen from all pages in the corpus
    for key,value in corpus.items():

        if key in probability_distribution:
            probability_distribution[key] += (1-damping_factor)/num_all_pages

        else:
            probability_distribution[key] = (1-damping_factor)/num_all_pages

    return probability_distribution       


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    first_sample = random.choice(list(corpus.keys()))

    frequency_dict = {}

    frequency_dict[first_sample] = 1

    page = first_sample

    for i in range(n-1):

        probability_distribution = transition_model(corpus,page,damping_factor)
        pages = []
        weights = []
        for key,value in probability_distribution.items():
            pages.append(key)
            weights.append(value)

        page_list = random.choices(pages,weights=weights, k=1)  
        page = page_list[0]

        if page in frequency_dict:
            frequency_dict[page] += 1
        else:
            frequency_dict[page] = 1

    pagerank_dict = {}

    for key,value in frequency_dict.items():

        pagerank_dict[key] = value/n

    return pagerank_dict

def incoming_pages(corpus,page):
    """
    Return a set with each possible page i that links to page p
    """

    incoming_pages_set = set()

    for key,value in corpus.items():

        if page in value:
            incoming_pages_set.add(key)

    return incoming_pages_set     


def delta_greater_than_001(current_rank_values, new_rank_values):

    result = {key: abs(current_rank_values[key] - new_rank_values[key]) for key in current_rank_values}    

    for key, value in result.items():

        if value > 0.001:
            return True
        

    return False

def num_links(corpus,page):
    """
    Return number of links on page i
    """

    links = corpus[page]

    return len(links)



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_number_pages = len(corpus)

    pages = set(corpus.keys())

    corpus2 = {}

    for key,value in corpus.items():

        if len(value) == 0:
            corpus2[key] = pages
        else:
            corpus2[key] = value



    current_rank_values = {}
    new_rank_values = {}

    for key,value in corpus2.items():

        current_rank_values[key] = 1 / total_number_pages


    while True:

        for page,value in current_rank_values.items():

            sumatoria = 0
            all_pages_linking_to_page = incoming_pages(corpus2,page)

            for page_linking in all_pages_linking_to_page:

                sumatoria += current_rank_values[page_linking] / num_links(corpus2,page_linking)

            new_rank_values[page] = (1-damping_factor)/total_number_pages + damping_factor*sumatoria

       
        if not delta_greater_than_001(current_rank_values, new_rank_values):
            break

        for key in new_rank_values:
            current_rank_values[key] = new_rank_values[key]




    return current_rank_values





if __name__ == "__main__":
    main()
