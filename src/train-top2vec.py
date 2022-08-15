from top2vec import Top2Vec
import pandas as pd

documents = pd.read_json("data/vol7.json").descriptions.tolist()
model = Top2Vec(documents, speed="deep-learn")
model.save("data/top2vec-model")
