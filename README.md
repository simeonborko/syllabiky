# syllabiky
Recognize syllables in words, adjusted to Slovak language rules and heuristics.

(It should be useful also for Czech language.)

Author: Simeon Borko, simeon.borko@gmail.com

Date: Sep 01, 2017

Usage:

split_phrase('phrase to be processed') -> returns string where words syllables are delimited by hyphen (-)

split_word('wordtobesplit') -> returns string where word syllables are delimited by hyphen (-)

split_word('wordtobesplit', True) -> returns list of Syllable objects; you can convert them to string using str(syllableObj)
