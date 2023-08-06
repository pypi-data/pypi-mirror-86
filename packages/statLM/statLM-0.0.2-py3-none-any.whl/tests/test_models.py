# -*- coding: utf-8 -*-

import unittest
import numpy as np


from statLM import statistical_models as sm

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def __init__(self, *args, **kwargs):
        super(BasicTestSuite, self).__init__(*args, **kwargs)
        self.test_corpus = [
            "let us see were this project leads us",
            "we are having great fun so far",
            "we are actively developing",
            "it is getting tougher but it is still fun",
            "this project teaches us how to construct test cases",
        ]
        self.test_queries = [
            "let us see were that project",
            "we are",
            "it is",
            "it should be",
            "we",
        ]
        self.test_completions = ["leads", "actively", "getting", "us", "are"]

    def test_naive_ngram(self):
        # Naive Ngram
        nn = sm.NaiveNGram(n_max=3, threshold=1)
        nn.fit( self.test_corpus )
        self.assertEqual(
            nn.predict(self.test_queries), 
            ['leads', 'actively', 'getting', np.NaN, "are"]
        )
        self.assertEqual(
            nn.predict_proba(self.test_queries), 
            [('project leads', 0.5), ('we are actively', 0.5),
             ('it is getting', 0.5), np.NaN, ('we are', 1.0)]
        )
        self.assertEqual(
            nn.score( 
                queries=self.test_queries,
                completions=self.test_completions
            ),
            [0.5, 0.5, 0.5, 0, 1.0]
        )

    def test_naive_ngram_no_threshold(self):
        # Naive Ngram
        nn = sm.NaiveNGram(n_max=3, threshold=0)
        nn.fit( self.test_corpus )
        self.assertEqual(
            nn.predict(self.test_queries), 
            ['leads', 'actively', 'getting', "us", "are"]
        )
        self.assertEqual(
            nn.predict_proba(self.test_queries), 
            [('project leads', 0.5), ('we are actively', 0.5),
             ('it is getting', 0.5), ("us", 3/37), ('we are', 1.0)]
        )        

    def test_stupid_backoff(self):
        sb = sm.StupidBackoff(n_max=3, alpha=0.4, threshold=1)
        sb.fit( self.test_corpus )
        self.assertEqual(
            sb.predict(self.test_queries), 
            ['leads', 'actively', 'getting', np.NaN, "are"]
        )
        self.assertEqual(
            sb.predict_proba(self.test_queries), 
            [('project leads', 0.2), ('we are actively', 0.5), ('it is getting', 0.5), np.NaN, ('we are', 0.4)]
        )        
        self.assertEqual(
            sb.score( 
                queries=self.test_queries,
                completions=self.test_completions
            ),
            [0.2, 0.5, 0.5, 0, 0.4]
        )        

    def test_stupid_backoff_no_threshold(self):
        sb = sm.StupidBackoff(n_max=3, alpha=0.4, threshold=0)
        sb.fit( self.test_corpus )
        self.assertEqual(
            sb.predict(self.test_queries), 
            ['leads', 'actively', 'getting', "us", "are"]
        )
        self.assertEqual(
            sb.predict_proba(self.test_queries), 
            [('project leads', 0.2), ('we are actively', 0.5), ('it is getting', 0.5), ("us", 3/37), ('we are', 0.4)]
        )        
        self.assertEqual(
            sb.score( 
                queries=self.test_queries,
                completions=self.test_completions
            ),
            [0.2, 0.5, 0.5, 3/37, 0.4]
        )   

# TODO: 
#     - construct more test cases
    # - automate test via github action

if __name__ == '__main__':
    unittest.main()