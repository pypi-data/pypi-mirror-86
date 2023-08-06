import numpy as np
from collections import Counter

from .ngram import NGramFrequenzy

__all__ = ["NaiveNGram", "StupidBackoff"]


class BaseStatisticalModel(object):
    """Base class for all statistical models.
    """

    def __init__(self, n_max=2, frequencies=None):
        self.n_max = n_max
        self.model_frequencies = frequencies
    
    def _generate_freq(self, corpus):
        self.model_frequencies = { 
            n: NGramFrequenzy(corpus=corpus, ngram_range=( n, n ) ) 
            for n in range(1, self.n_max + 1)
        }

    @classmethod
    def __get_classname(cls):
        return cls.__name__

    def __make_ngram_stats(self):
        default = f"{ self.__get_classname() }: n_max = { self.n_max }"
        if self.model_frequencies:
            ngram_stats = "\n".join([
                f"  {n}-grams: count={ len( freq.keys() ) }, freq={ sum( freq.values() ) }" 
                 for n, freq in self.model_frequencies.items()
            ])
            return f"{default}\n{ngram_stats} "    
        else:
            return f"{default}, not fitted"

    def __repr__(self):
        return self.__make_ngram_stats()

    def __add__(self, other):
        left_max_n = len(self.model_frequencies.keys())
        right_max_n = len(other.model_frequencies.keys())
        common_max_n = max( left_max_n, right_max_n )
        return BaseStatisticalModel(frequencies={
            n: self.model_frequencies.get(n, NGramFrequenzy() ) + other.model_frequencies.get(n, NGramFrequenzy() )
            for n in range(1, common_max_n + 1)
        })

    def summary(self):
        """ Make summary statistics of fitted model

            Returns:
                str: summary as formatted string
        """
        return self.__make_ngram_stats()

    def ngram_frequency(self, ngram_seq, normalize=False):
        """ Obtain frequency of N-Gram from fitted model.

            Args:
                ngram_seq (str): N-Gram as a string
            
            Returns:
                int: Frequency if N-Gram
        """
        if self.model_frequencies:
            ngram_seq_parsed = ngram_seq.split(" ")
            ngram_seq_len = len(ngram_seq_parsed)

            if ngram_seq_len in self.model_frequencies:
                # search for ngrams with matching degree
                return self.model_frequencies[ ngram_seq_len ].search_ngrams(query=ngram_seq_parsed, normalize=normalize)
            else:
                return 0
        else:
            return 0


class NaiveNGram(BaseStatisticalModel):
    """ Model which determines next word of a sequence by finding N-Gram with most matching words. 
        It does not apply any smoothing to probability or scores (equivalent to Stupid Backoff with alpha=1).

        Args:
            n_max (int): Maximum n-gram degree
            threshold (int): Lowest n-gram degree to search in. If threshold reached, default to empty NGramFrequency.
    """
    def __init__(self, n_max, threshold=0, **kwargs):
        super(NaiveNGram, self).__init__(n_max, **kwargs)
        assert threshold >= 0
        self.threshold = threshold

    def _recursive_search(self, parsed_query, n, **kwargs):
        search_result = self.model_frequencies[ n ].search_ngrams(query=parsed_query, **kwargs)
        if not search_result.is_empty():
            return search_result
        else:
            n -= 1
            if n > self.threshold:
                # enter recursion with first word removed from query
                return self._recursive_search( parsed_query[ 1: ], n, **kwargs)
            else:
                return NGramFrequenzy()

    def _query_model(self, query, **kwargs):
        """ Query model to obtain longest matching ngram.

            Args:
                query (str): 

            Returns:
                NGramFrequenzy
        """
        parsed_query = query.split(" ")
        query_len = len(parsed_query)
        if query_len > self.n_max - 1:
            # if query longer than n_max + 1, then adjust 
            adjusted_query = parsed_query[ -(self.n_max -1): ]
            return self._recursive_search(adjusted_query, n=len(adjusted_query) + 1, **kwargs)
        else:
            return self._recursive_search(parsed_query, n=len(parsed_query) + 1, **kwargs)

    def fit(self, corpus):
        """ Fit model by generating word frequencies from input corpus.

            Args:
                corpus (iterable): Corpus as a sequence of docs each of type string
            
            Returns: 
                self
        """
        self._generate_freq(corpus)
        return self

    def score(self, queries, completions):
        """ Score completion for a given query.

            Args:
                queries (iterable): sequence of queries as strings
                completions (iterable): sequence of completions as strings for a given query

            Returns:
                list: score for each completion for a query
        """
        scores = []
        for query, comp in zip(queries, completions):
            search_result = self._query_model(query, normalize=True)._endswith( comp )
            if not search_result.is_empty():
                pred = search_result.most_common(1, counts=True)[0][1]
                scores.append( pred )
            else:
                scores.append(0)
        return scores

    def predict(self, queries):
        """ Model predictions based on input queries

            Args:
                queries (iterable): sequence queries each of type string

            Returns:
                list: prediction for each query as list of words each of type string
        """
        predictions = []
        for query in queries:
            search_result = self._query_model(query)
            if search_result.is_empty():
                predictions.append( np.NaN)
            else:
                # take last word ngram
                pred = search_result.most_common(1, counts=False)[0].split(" ")[-1]
                predictions.append( pred )
        return predictions

    def predict_proba(self, queries, top_n=1):
        """ Model predictions and its conditional probability based on input queries.

            Args:
                queries (iterable): sequence queries each of type string

            Returns:
                list: prediction for each query as list of words each of type string
        """
        probas = []
        for query in queries:
            search_result = self._query_model(query, normalize=True)
            if search_result.is_empty():
                probas.append( np.NaN )
            else:
                pred = search_result.most_common(1, counts=True)[0]
                probas.append( pred )
        return probas


class StupidBackoff(NaiveNGram):
    """ Stupid Backoff model as described in its original paper (https://www.aclweb.org/anthology/D07-1090.pdf)
        It recursively assigns a score to a word depending on its context which is further smoothed by parameter alpha.

        Args:
            n_max (int): Maximum n-gram degree
            threshold (int): Lowest n-gram degree to search in. If threshold reached, default to empty NGramFrequency.
            alpha (float): Smoothing parameter within range (0,1]
    """    
    def __init__(self, n_max, alpha=0.4, threshold=0, **kwargs):
        super(StupidBackoff, self).__init__(n_max, threshold, **kwargs)
        assert 0 < alpha <= 1
        self.alpha = alpha

    def _recursive_search(self, parsed_query, n, threshold=0, **kwargs):
        search_result = self.model_frequencies[ n ].search_ngrams(
            query=parsed_query, 
            smoothing=self.alpha**(self.n_max - n),
            **kwargs
        )
        if not search_result.is_empty():
            return search_result
        else:
            n -= 1
            if n > self.threshold:
                # enter recursion with first word removed from query
                return self._recursive_search( parsed_query[ 1: ], n, **kwargs)
            else:
                return NGramFrequenzy()            



# TODO: 
#     - additional language models (markov chain, backoff etc)
#     - methods for exploring word freq
#     - improve efficiency of ngram-search (e.g make ngram comparison more efficient by comparing lists instead of strings)
#     - add type checking

if __name__ == "__main__":
    test_corpus = [
        "let us see were this project leads us",
        "we are having great fun so far",
        "we are actively developing",
        "it is getting tougher but it is still fun",
        "this project teaches us how to construct test cases",
    ]        
    sb = StupidBackoff(n_max=3, alpha=0.4, threshold=0)
    sb.fit( test_corpus )
    infer_doc = [
        # "let us see were that project",
        # "they are",
        # "it is",
        "it should be",
        # "we",
    ]
    print(sb)
    print(sb.predict(infer_doc))
    print(sb.predict_proba(infer_doc))
    print(sb.score(["they are"], ["actively"]))
