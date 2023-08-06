# -*- coding: utf-8 -*-

# from .context import statLM

from statLM import statistical_models as sm
import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_statistical_models(self):
        test_corpus = [
            "let us see were this project leads us",
            "we are having great fun so far",
            "we are actively developing",
            "it is getting tougher but it is still fun",
            "this project teaches us how to construct test cases",
        ]        
        sb = sm.NaiveNGram(n_max=3)
        sb._generate_freq( test_corpus )
        infer_doc = ["let us see were that project"]
        sb.predict(infer_doc)
        assert sb.predict(infer_doc) == ["leads"]


if __name__ == '__main__':
    unittest.main()