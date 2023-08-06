# -*- coding: utf-8 -*-

# from .context import statLM

# from statLM.statistical_models import RecursiveNextWord
import unittest
import numpy as np

from statLM import statistical_models as sm

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
        sb.fit( test_corpus )
        test_queries = [
            "let us see were that project",
            "we are",
            "it is",
            "it should be",
            "we",
        ]
        self.assertEqual(
            sb.predict(test_queries), 
            ['leads', 'actively', 'getting', np.NaN, "are"]
        )
        self.assertEqual(
            sb.predict_proba(test_queries), 
            [('project leads', 1), ('we are actively', 0.5),
             ('it is getting', 0.5), np.NaN, ('we are', 1.0)]
        )
# TODO: 
#     - construct more test cases
    # - automate test via github action

if __name__ == '__main__':
    unittest.main()