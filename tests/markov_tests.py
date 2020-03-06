from sources.markov import Markov
from sources.tools import to_ones, from_ones
import random
import unittest


class MarkovTests(unittest.TestCase):
    def test_simple_expression(self):
        """(2x + 3) / 7"""
        rules = [
            ('#1', '11#'),
            ('#', '111'),
            ('*1111111', '1*'),
            ('*1', '*'),
            ('*', '.1'),
            ('1', '*#')
        ]
        m = Markov(rules)
        f = lambda x: (2 * x + 3) // 7
        for i in range(100):
            self.assertEqual(
                from_ones(m(to_ones(i))),
                f(i)
            )

    def test_word_reverse(self):
        rules = [
            ('*aa', 'a*a'),
            ('*bb', 'b*b'),
            ('*ab', 'b*a'),
            ('*ba', 'a*b'),
            ('**a*', 'a**'),
            ('**b*', 'b**'),
            ('**', '.'),
            ('', '*')
        ]
        m = Markov(rules)
        f = lambda: ''.join('a' if x > random.randrange(0, 25) else 'b'
                            for x in random.sample(range(0, 25), 25))
        for _ in range(0, 100):
            s = f()
            self.assertEqual(m(s), s[::-1])


if __name__ == '__main__':
    unittest.main()



