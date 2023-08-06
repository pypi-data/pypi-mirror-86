# -*- coding: utf-8 -*-
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from collections.abc import Iterable
from types import GeneratorType


__all__ = ["NGramFrequenzy"]


class NGramFrequenzy(object):
    """ Ngram frequencies from corpus.
    Args:
        corpus (iterable): Corpus as a sequence of docs each of type string
        frequency (dict or Counter, optional): ngram frequencies

    Raises:
        ValueError: Submitted frequency has to be either dict or Counter object

    """
    def __init__(self, corpus=[], frequency={}, **kwargs):
        if corpus:
            self.__ngram_freq = self.__extract_ngram_frequency(corpus=corpus, **kwargs)
        elif frequency:
            if isinstance(frequency, dict) or isinstance(frequency, GeneratorType):
                self.__ngram_freq = Counter(frequency)
            elif isinstance(frequency, Counter):
                self.__ngram_freq = frequency
            else:
                raise ValueError("Submitted frequency has to be either dict or Counter object")
        else:
            self.__ngram_freq =  Counter()

    @staticmethod
    def __extract_ngram_frequency(corpus, **kwargs):
        """ Count occurences for each word in the whole corpus.
            Arg:
                corpus (iterable): Series of documents each formatted as string
                
            Returns:
                pd.Series: Counts indexed by its respective word
        """
        cv = CountVectorizer(**kwargs)
        # get bag-of-words as sparse matrix
        bow = cv.fit_transform( corpus )
        # obtain list of feature names
        vocab = list( cv.get_feature_names() )
        # # word occurence for each column and collapse to vector
        word_counts = bow.sum(axis=0).A1
        # map word to its counts
        freq_distribution = Counter( dict( zip( vocab, word_counts) ) )
        return freq_distribution

    @classmethod
    def from_corpus(cls, corpus, **kwargs):
        """ Generate ngram frequencies from corpus

            Args:
                corpus (iterable): Series of documents each formatted as string

            Returns:
                NGramFrequenzy
        """
        if isinstance(corpus, list):
            return cls( frequency=cls.__extract_ngram_frequency(corpus, **kwargs) )
        else:
            raise  ValueError("Corpus has to be a list object")

    @classmethod
    def from_frequency(cls, frequency):
        """ Instantiate class by ngram frequencies

            Args:
                frequency (dict or Counter, optional): ngram frequencies

            Returns:
                NGramFrequenzy
        """
        if isinstance(frequency, dict) or isinstance(frequency, Counter):
            return cls( frequency = frequency )
        else:
            raise ValueError("N-Gram Frequency has to be either dict or Counter object")

    @property
    def degree(self):
        if self.is_empty():
            return 0
        else:
            for ngram in self.keys():
                return ngram.count(" ") + 1

    @property
    def total_frequency(self):
        if self.is_empty():
            return 0
        else:
            return sum( self.__ngram_freq.values() )

    @property
    def total_ngrams(self):
        if self.is_empty():
            return 0
        else:
            return len( self.__ngram_freq.keys() )

    def __repr__(self):
        if self.__ngram_freq:
            return str(self.__ngram_freq)

    def __str__(self):
        if self.__ngram_freq:
            return str( dict(self.__ngram_freq) )
        else:
            return str( dict() )

    def __add__(self, other):
        return NGramFrequenzy(frequency=self.__ngram_freq + other.__ngram_freq)

    def __iter__(self):
        for ngram, count in self.__ngram_freq.items():
            yield ngram, count

    def __getitem__(self, val):
        if isinstance(val, str):
            return self.__ngram_freq[val]
        elif isinstance(val, list):
            return self.search_ngrams(query=val)
        else:
            raise ValueError("Subcription value has to be either str or list")

    def keys(self):
        """ Iterator over ngrams """
        return self.__ngram_freq.keys()

    def values(self):
        """ Iterator over counts """
        return self.__ngram_freq.values()        

    def items(self):
        """ Iterator over ngram, counts tuples """
        return self.__ngram_freq.items()

    def search_ngrams(self, query, normalize=False, smoothing=1):
        """ Search ngrams which match the query from start.

            Args:
                query (str): query as string with blank as delimiter between token
                normalize (bool, optional): Normalize ngram frequencies. Defaults to False.

            Returns:
                NGramFrequenzy
        """
        parsed_query = query.split(" ") if isinstance(query, str) else query
        word_num = len(parsed_query)
        query_result = NGramFrequenzy(frequency={
            ngram: count
            for ngram, count in self.__ngram_freq.items() 
            if ngram.split(" ")[ :word_num ] == parsed_query
        })
        if not normalize:
            return query_result
        else:
            # if 1-gram take total frequency and do not apply smoothing
            if query_result.degree == 1:
                total = self.total_frequency
                smoothing = 1
            else: 
                total = query_result.total_frequency
            return NGramFrequenzy( frequency= { ngram: (count / total) * smoothing for ngram, count in query_result.items() } )

    def most_common(self, top_n=1, counts=True):
        """ Obtain most common ngrams and their respective counts in descending order.

        Args:
            top_n (int, optional): Number of top most ngrams. Defaults to 1.
            counts (bool, optional): Whether to also include counts. Defaults to True.

        Returns:
            list: If counts, then list of ngram with their respective counts as tuples,
                  else only ngrams
        """
        top_ngram_scores = self.__ngram_freq.most_common(top_n)
        if counts:
            return top_ngram_scores
        else:
            return list( ngram_score[0] for ngram_score in top_ngram_scores )            
            
    def _endswith(self, ending):
        return NGramFrequenzy(frequency={
            ngram: count
            for ngram, count in self.__ngram_freq.items() 
            if ngram.split(" ")[ -1 ] == ending
        })

    def is_empty(self):
        """ Check if there are any ngram frequency counts.

        Returns:
            bool
        """
        if not self.__ngram_freq.keys():
            return True
        else:
            return False

# TODO:
# - try to inherit from Counter
# - make compatible with generator
# - change object repr
# - implement collection class FrequencyCollection consting of multiple NGramFrequency 

if __name__ == "__main__":
    test_corpus = [
        "let us see were this project leads us",
        "we are having great fun so far",
        "we are having even greater fun now",
        "we are actively developing",
        "it is getting tougher but it is still fun",
        "this project teaches us how to construct test cases",
        "this project teaches us how to construct a package",
        "this project teaches us how to construct a setup tool",
        "this project teaches us how to build an api documentations",
    ]   
    ngfreq = NGramFrequenzy(corpus=test_corpus, ngram_range=(2,2))

    print(ngfreq.is_empty())
    print(ngfreq.degree)
    print(ngfreq.total_frequency)

    # print(ngfreq["are having"])
    # print( ngfreq.most_common(2, counts=True) )
    print(ngfreq.search_ngrams("are", normalize=True, smoothing=0.4))
