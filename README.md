# PageRankAI

Search engines like Google display search results in order of importance using a page-ranking algorithm. The Google PageRank algorithm considers a website as more important (higher page rank), when it is linked to by other imporant websites. Links from less important websites have a lower importance weighting.

## Task:

Using a Random Surfer Markov Chain and an Iterative Algorithm, write an AI to rank web pages by importance.

```
$ python pagerank.py corpus0
PageRank Results from Sampling (n = 10000)
  1.html: 0.2223
  2.html: 0.4303
  3.html: 0.2145
  4.html: 0.1329
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
```
[View the full assignment description on CS50's OpenCourseWare](https://cs50.harvard.edu/ai/2023/projects/2/pagerank/)

## Usage:

Requires Python(3) to run:

```python pagerank.py (corpus_directory)```