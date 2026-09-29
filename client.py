"""Pure Python BM25 Okapi Memory Retrieval Engine.
100% Python Standard Library.
"""

import math
import collections
import re

class BM25MemoryBuffer:
    """In-memory BM25 Okapi ranking engine for fast keyword retrieval without vector DBs."""
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = []
        self.doc_lens = []
        self.avg_dl = 0.0
        self.df = collections.defaultdict(int)

    def add_document(self, doc_id, text):
        words = re.findall(r'\b\w+\b', text.lower())
        self.docs.append({"id": doc_id, "text": text, "words": words})
        self.doc_lens.append(len(words))
        self.avg_dl = sum(self.doc_lens) / len(self.doc_lens)
        for w in set(words):
            self.df[w] += 1

    def search(self, query, top_k=2):
        q_words = re.findall(r'\b\w+\b', query.lower())
        scores = []
        n_docs = len(self.docs)
        for i, doc in enumerate(self.docs):
            score = 0.0
            doc_words = doc["words"]
            counts = collections.Counter(doc_words)
            dl = len(doc_words)
            for qw in q_words:
                if qw in self.df:
                    idf = math.log((n_docs - self.df[qw] + 0.5) / (self.df[qw] + 0.5) + 1.0)
                    tf = counts[qw]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * (dl / (self.avg_dl or 1)))
                    score += idf * (numerator / denominator)
            scores.append((score, doc["id"], doc["text"]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [{"id": sid, "score": round(sc, 4), "text": txt} for sc, sid, txt in scores[:top_k]]
