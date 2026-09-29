from client import BM25MemoryBuffer

bm = BM25MemoryBuffer()
bm.add_document("doc1", "Distributed consensus algorithms: Raft and Paxos")
bm.add_document("doc2", "Convolutional neural network filter kernels")

hits = bm.search("Paxos consensus")
print("BM25 Search Hits:", hits)
