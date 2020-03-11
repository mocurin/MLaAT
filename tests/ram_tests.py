from sources.ram import RAM
import unittest


class RAMTests(unittest.TestCase):
    def test_n_pow_n(self):
        program = """
        read(0)
        jgtz(a)
        write(=0)
        halt
  a:    store(1)
        store(2)
        load(=1)
        store(3)
  b:    mult(2)
        store(3)
        load(1)
        sub(=1)
        jzero(end)
        store(1)
        load(3)
        jump(b)
  end:  write(3)
        """
        ram = RAM(program, verbose=True)
        lam = lambda x: x**x if x > 0 else 0
        for i in range(2, 5):
            res = ram([str(i)])
            self.assertEqual(int(res[0]), lam(i))


if __name__ == '__main__':
    unittest.main()
