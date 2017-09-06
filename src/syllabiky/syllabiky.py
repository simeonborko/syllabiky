#!/usr/bin/python3.5

"""

Recognize syllables in words, adjusted to Slovak language rules and heuristics.

Author: Simeon Borko, simeon.borko@gmail.com
Date: Sep 01, 2017

Usage:

split_phrase('phrase to be processed') -> returns string where words syllables are delimited by hyphen (-)

split_word('wordtobesplit') -> returns string where word syllables are delimited by hyphen (-)

split_word('wordtobesplit', True) -> returns list of Syllable objects; you can convert them to string using str(syllableObj)

You can adjust functionality by editing queries.csv, pre.txt, suff.txt.

"""

diphthong = True


class Char:
    prev = None
    next = None
    syllable = None

    def __init__(self, text):
        self.text = text
        if self.text == ' ':
            raise Exception('Text cannot be space')

    def vowel(self):
        vowels = ('a', 'á', 'ä', 'e', 'é', 'i', 'í', 'o', 'ó', 'u', 'ú', 'y', 'ý', 'ô')
        return self.text.lower() in vowels or diphthong and self.text.lower() in ('ia', 'ie', 'iu')

    def syllabic_consonant(self):
        return self.text.lower() in ('r', 'ŕ', 'l', 'ĺ')

    def neighbours_consonants(self, distance, vowel=True, syllabic=True):
        """
        Find if all neighbours given by distance are consonants (not a vowel).
        distance 0 means this Char
        minus distance means left neighbours
        plus distance means right neighbours
        if neighbour not found, return false
        """

        if vowel == False and self.vowel():
            return False

        if syllabic == False and self.syllabic_consonant_in_the_middle():
            return False

        elif distance == 0:
            return True

        elif distance < 0:
            if self.prev:
                return self.prev.neighbours_consonants(distance + 1, vowel=False, syllabic=syllabic)
            return False  # if prev not exists

        elif distance > 0:
            if self.next:
                return self.next.neighbours_consonants(distance - 1, vowel=False, syllabic=syllabic)
            return False

    def syllabic_consonant_in_the_middle(self):
        """Find if object is syllabic consonant between two consonants."""
        return self.syllabic_consonant() and self.neighbours_consonants(-1) and self.neighbours_consonants(1)

    def __str__(self):
        return self.text

    def get_word(self):
        if self.next:
            return self.text + self.next.get_word()
        return self.text

    def to_list(self):
        if self.next:
            return [self] + self.next.to_list()
        return [self]


class Syllable:
    def __init__(self, char):
        self.chars = [char]

    def add_char(self, char, as_first=False):
        if as_first:
            self.chars.insert(0, char)
        else:
            self.chars.append(char)
        char.syllable = self

    def __str__(self):
        l = []
        for char in self.chars:
            l.append(str(char))
        return ''.join(l)

    def prev(self):
        """Find left syllable neighbour.
        Return syllable or None if not found."""
        if self.chars[0].prev is None:
            return None
        return self.chars[0].prev.syllable

    def next(self):
        """Find right syllable neighbour.
        Return syllable or None if not found."""
        char = self.chars[len(self.chars) - 1]  # last char in this syllable
        if char.next is None:
            return None
        return char.next.syllable

    def left_neighbours(self, append=''):
        """Return left neighbours and self as list of strings. If append is set, append it to this syllable."""
        sl = [str(self) + str(append)]  # sl - self list
        prev = self.prev()
        if prev:
            return prev.left_neighbours() + sl
        return sl

    def right_neighbours(self, prepend='', objects=False):
        """Return self and right neighbours.
        If objects is False, return list of string. If prepend is set, prepend it before this syllable.
        If objects is True, return list of Syllable objects and ignore prepend."""
        this = self if objects else str(prepend) + str(self)  # this = objects ? self : str(prepend) + str(self)
        next = self.next()
        if next:
            return [this] + next.right_neighbours(objects=objects)
        return [this]

    def is_last(self):
        """Check if syllable is the last syllable.
        Note: this implementation is not equal to simply check if self.next() exists,
        because there may be a hole between syllables."""
        node = self.chars[len(self.chars) - 1]
        while node.next:
            node = node.next
        # node is now last char is word
        return node.syllable is self  # if node.syllable is None, returns False, because None is not self

    def is_first(self):
        """Check if syllable is the first syllable.
        Note: this implementation is not equal to simply check if self.prev() exists,
        because there may be a hole between syllables."""
        node = self.chars[0]
        while node.prev:
            node = node.prev
        return node.syllable is self


    def merge_with_next(self):
        """Merge syllable with right syllable neighbour.
        If the neighbour does not exist or
        both syllables do not have exactly one char, raise Exception."""
        next = self.next()

        if next is None:
            raise Exception('No syllable neighbour')
        if len(str(self)) != 1 or len(str(next)) != 1:
            raise Exception('Bad syllable lengths')

        self.add_char(next.chars[0])


def get_linked_chars(word):
    """Create doubly linked list of Char objects, return head Char."""

    # Load chars in word as python list.
    l = []
    for char in word:
        if diphthong:
            length = len(l)
            if length > 0 and (
                                    l[length - 1].lower() == 'i' and char.lower() in ('a', 'e', 'u') or
                                    l[length - 1].lower() == 'c' and char.lower() == 'h' or
                                l[length - 1].lower() == 'd' and char.lower() in ('z', 'ž')
            ):
                l[length - 1] += char
                continue
        l.append(char)

    if len(l) == 0:
        return None

    head = Char(l[0])
    last = head

    for char in l[1:]:  # for each char in input list except first char
        node = Char(char)
        node.prev = last
        last.next = node
        last = node

    return head


def find_vowels(head):
    """Load list of Char objects that are vowels or syllabic consonants in the middle"""
    vowels = []
    node = head
    while node:
        if node.vowel() or node.syllabic_consonant_in_the_middle():
            vowels.append(node)
        node = node.next
    return vowels


def create_syllables(vowels):
    """
    Create syllables for vowels and apply consonant neighbour rule.
    If left neighbour is consonant, add it to vowel's syllable.
    """
    for v in vowels:
        v.syllable = Syllable(v)
        if v.neighbours_consonants(-1):
            v.syllable.add_char(v.prev, True)


def process_remaining(head, vowels, matcher, r=1):
    """Remaining consonants add preferred to right syllable, if cannot do that, add to left syllable.
    When left is syllabic-consonant-in-the-middle and right is a consonant, add to left syllable.
    TODO: pripony - i.e. mas-tný namiesto mast-ný
    """

    def add_to_suitable_syllable(node, vowels, matcher, r):
        """Add to suitable syllable.
        Return True if success or char has already syllable,
        return False if waiting"""
        if node.syllable is not None:
            return True

        side = get_side(node, vowels, matcher, r)
        if side is None:
            return False
        elif side < 0:
            node.prev.syllable.add_char(node)
        else:
            node.next.syllable.add_char(node, True)
        return True

    if r > 10:
        raise Exception('Too many repetitions')

    repeat = False
    node = head
    while node:
        if add_to_suitable_syllable(node, vowels, matcher, r) is False:
            repeat = True
        node = node.next

    if repeat:
        process_remaining(head, vowels, matcher, r+1)

# Get side functions - START

def get_side(node, vowels, matcher, r):
    """Get side to which char should be added. r means round (or repeat).
    Return 0 or plus int to add char to right,
    minus int to left,
    None if char node should be avoided.
    """

    # check if node has both char neighbours
    if node.next is None:
        if node.prev is None:
            raise Exception()
        elif node.prev.syllable:
            return -1
        else:
            return None
    elif node.prev is None:
        if node.next.syllable:
            return 1
        else:
            return None

    # node has both left and right char neighbours

    # check if node has at least one syllable neighbour
    if node.prev.syllable is None and node.next.syllable is None:
        return None

    # char matching
    right_db = get_db_right_side(node, matcher)
    if right_db == 2:
        return right_db
    elif right_db == 1 and r < 3:
        return None

    # suffix
    suff = get_suffix_side(node, matcher)
    if suff != 0:
        syllable = node.prev.syllable if suff < 0 else node.next.syllable
        return suff if syllable is not None else None

    # prefix
    pre = get_prefix_side(node, matcher)
    if pre != 0:
        syllable = node.prev.syllable if pre < 0 else node.next.syllable
        return pre if syllable is not None else None

    # syllable matching
    if node.prev.syllable and node.next.syllable:
        sdb = get_db_syllable_side(node, matcher) / 2 + right_db
        if abs(sdb) >= 1:
            return sdb

    # no match in db nor suffixes nor prefixes

    if r < 3:
        return None

    if node.prev in vowels and node.prev.neighbours_consonants(2, syllabic=False):
        return -1

    # this condition is for c in jablcko
    if node.prev.syllabic_consonant_in_the_middle() and node.neighbours_consonants(1):
        return -1
    elif node.next.syllable:
        return 1
    elif node.prev.syllable:
        return -1

    return 0


def get_db_right_side(node, matcher):
    """Find if adding to right syllable would cause matching syllable with known word.
    Return 2 if surely add to right syllable,
    1 if maybe add to right syllable,
    0 if not know."""

    score = matcher.char_concord(node.text + str(node.next.syllable)) if node.next.syllable else 0

    if score >= 4:
        return 2
    elif score == 3:
        return 1
    else:
        return 0


def get_db_syllable_side(node, matcher):
    """
    Get which side is suitable according to syllable matching.
    This function expect node to have both syllable neighbours.
    Return minus int if char node should be added to left neighbour,
    plus int if to right,
    0 if not determined.
    """

    if node.prev.syllable is None or node.next.syllable is None:
        raise Exception('Char node does not have both syllable neighbours')

    left_opt_sylls = node.prev.syllable.left_neighbours(node) + node.next.syllable.right_neighbours()
    right_opt_sylls = node.prev.syllable.left_neighbours() + node.next.syllable.right_neighbours(node)

    left_score = matcher.syllable_concord(left_opt_sylls)
    right_score = matcher.syllable_concord(right_opt_sylls)

    return right_score - left_score


def get_suffix_side(node, matcher):
    """Check if (not) adding char node to right syllable would cause creating word suffix.
    Return 1 if char node should be added to right,
    -1 if to left,
    0 if cannot determine."""
    if node.next.syllable is None or node.next.syllable.is_last() is False:
        return 0
    left_score = matcher.is_suffix(str(node.next.syllable))
    right_score = matcher.is_suffix(str(node) + str(node.next.syllable))
    return right_score - left_score


def get_prefix_side(node, matcher):
    """Check if (not) adding char node to left syllable would cause creating word prefix.
    Return 1 if char node should be added to right,
    -1 if to left,
    0 if cannot determine."""
    if node.prev.syllable is None or node.prev.syllable.is_first() is False:
        return 0
    left_score = matcher.is_prefix(str(node.prev.syllable) + str(node))
    right_score = matcher.is_prefix(str(node.prev.syllable))
    return right_score - left_score

# Get side function - END

def get_all_syllables(head, vowels=None):
    if head.prev:
        raise Exception('Not given head')
    if head.syllable is None:
        raise Exception('Head syllable is None')

    syllables = head.syllable.right_neighbours(objects=True)

    if vowels is not None and len(syllables) != len(vowels):
        raise Exception('Number if syllables is unexpected')

    return syllables

def auto_phenomenon(syllables):
    """Treat syllable neighbours that are made up from exactly one char. Merge them.
    Function name is related to example: auto should be split as au-to, not a-u-to (also eucalyptus)."""
    for syll in syllables:
        if syll.next() and len(str(syll)) == 1 and len(str(syll.next())) == 1:
            syll.merge_with_next()
            syllables = auto_phenomenon(get_all_syllables(syllables[0].chars[0]))
            break
    return syllables

"""def print_syllables(vowels):
    l = []
    for v in vowels:
        l.append(str(v.syllable))
    print('-'.join(l))"""


def split_phrase(phrase, matcher):
    words = []
    for word in phrase.split(' '):
        split = split_word(word, matcher)
        words.append(split if split is not None else word)
    return ' '.join(words)


def split_word(word, matcher, objects=False):
    """Split given word into syllables. 'matcher' is instance of DbMatcher.
    If objects, return list of Syllable objects,
    else return string, where syllables are delimited by hyphen (-)."""
    head = get_linked_chars(word)
    vowels = find_vowels(head)

    if len(vowels) == 0:
        return None

    create_syllables(vowels)
    process_remaining(head, vowels, matcher)
    syllables = get_all_syllables(head, vowels)
    syllables = auto_phenomenon(syllables)
    if objects:
        return syllables
    str_sylls = []
    for syll in syllables:
        str_sylls.append(str(syll))
    return '-'.join(str_sylls)
