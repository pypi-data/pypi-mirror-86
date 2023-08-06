******
statLM
******

statLM (Statistical Language Models) is a library for classical as well as modern language models.

Example Usage
#############

Train a language model and make predictions based on queries i.e. test data.

.. code-block:: python

    corpus = ["let us see were this project leads us",
                "we are having great fun so far",
                "we are actively developing",
                "it is getting tougher but it is still fun",
                "this project teaches us how to construct test cases"] 

    nng = NaiveNGram(n_max=3)
    # fit model on corpus
    nng.fit( corpus )
    # make predictions
    queries = ["let us see were that project", "but it"]
    nng.predict(queries)


In Progress
###########

* more language models e.g. (Stupid) Backoff, N-Gram Model
* improve efficiency of ngram comparisons
* construct CD/CI tests via github action

Copyright
#########

Copyright (C) 2020 statLM Raphael Redmer

For license information, see LICENSE.txt.
