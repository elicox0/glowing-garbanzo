# Presidential Candidate Summarizer
A Python module for investigating presidential campaign websites.

## Getting Started
To use this module, make sure you have the NLTK, Gensim, and Beautiful Soup libraries installed. This module currently can only be imported from the same directory as your own script. Run the following code from a directory that can have corpus files added to it:

## Usage
```python
>>> import presidential_candidates as pc
>>> start_site = "https://www.donaldjtrump.com/"
>>> info = pc.political_info(start_site, 'Donald Trump', '.', n_topic=5)
>>> info[0][1] # List of words representing topic #1

loading, distancing, vulnerable, protocol, adhere, physical, eg, area
