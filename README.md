# syllabiky
Recognize syllables in words, adjusted to Slovak language rules and heuristics.

(It should be useful also for Czech language.)

Author: Simeon Borko, simeon.borko@gmail.com

Date: Sep 06, 2017

## Installation

```
pip3 install git+git://github.com/simeonborko/syllabiky.git
```

## Usage:

```python
# BASIC USAGE

from syllabiky.syllabiky import split_phrase
from syllabiky.DbMatcher import DbMatcher

matcher = DbMatcher()
foo = split_phrase("zirafa", matcher) # zi-ra-fa

# ADVANCED

from syllabiky.syllabiky import split_word

# returns string where words syllables are delimited by hyphen (-)
split_phrase('phrase to be processed', matcher)

# returns string where word syllables are delimited by hyphen (-)
split_word('wordtobesplit', matcher)

# returns list of Syllable objects; you can convert them to string using str(syllableObj)
split_word('wordtobesplit', matcher, True)

```


