from sources.turing import Tape, Move, Turing
import unittest


class TuringTests(unittest.TestCase):
    def test_tape(self):
        string = 'test string'
        dummy = Tape(string)
        dummy[-1] = 'b'
        dummy[-10] = 'a'
        dummy[-100] = 'a'
        dummy[100] = 'b'
        dummy[200] = 'a'
        dummy[300] = 'a'
        self.assertEqual(str(dummy), 'aabtest stringbaa')

    def test_turing(self):
        program = [
            ((0, 'a'), (0, 'b', Move.R)),
            ((0, 'b'), (0, 'a', Move.R))
        ]
        t = Turing(program, verbose=True)
        self.assertEqual(t('aabbabab'), 'bbaababa')


if __name__ == '__main__':
    unittest.main()
