#!/usr/bin/python3.5

import os


class DbMatcher:
    db = None
    suffixes = None
    prefixes = None
    DIR = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def get_rows(cls, filename, split=True):
        if not os.path.isfile(filename):
            raise Exception('File not exists')
        rows = []
        with open(filename) as fp:
            for line in fp:
                l = cls.process_line(line)
                if l is not None:
                    rows.append(l.split('-') if split else l)
        return rows

    @staticmethod
    def process_line(line):
        l = line.strip()
        if len(l) > 0 and l[0] != '#':
            if ' ' in l:
                raise Exception('Contains space')
            return l
        return None

    def char_concord(self, word):

        def get_char_concord(x, y):
            """Find how many chars are same from start in x, y."""
            same = 0
            for i in range(min(len(x), len(y))):
                if x[i] == y[i]:
                    same += 1
                else:
                    break
            return same

        best = 0
        for line in self.db:
            w = ''.join(line)
            best = max(best, get_char_concord(w, word))
        return best

    def get_syllable_concord(x, y):
        """Find how many syllables are same. x and y are syllables group (like word)."""
        # x should be longer
        if len(x) < len(y):
            x, y = y, x  # swap

        count = 0
        for i in range(len(x)):
            for j in range(len(y)):
                c = 0
                for k in range(min(len(x) - i, len(y) - j)):
                    if str(x[i+k]) != str(y[j+k]):
                        break
                    c += 1
                count = max(count, c)

        return count

    def syllable_concord(self, syll_group):

        def get_syllable_concord(x, y):
            """Find how many syllables are same. x and y are syllables group (like word)."""
            # x should be longer
            if len(x) < len(y):
                x, y = y, x  # swap

            count = 0
            for i in range(len(x)):
                for j in range(len(y)):
                    c = 0
                    for k in range(min(len(x) - i, len(y) - j)):
                        if str(x[i + k]) != str(y[j + k]):
                            break
                        c += 1
                    count = max(count, c)

            return count

        best = 0
        for line in self.db:
            best = max(best, get_syllable_concord(syll_group, line))
        return best

    def is_suffix(self, x):
        return x in self.suffixes

    def is_prefix(self, x):
        return x in self.prefixes

DbMatcher.suffixes = DbMatcher.get_rows(DbMatcher.DIR + '/suff.txt', False)
DbMatcher.prefixes = DbMatcher.get_rows(DbMatcher.DIR + '/pre.txt', False)
