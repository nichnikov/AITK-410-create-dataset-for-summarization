import os
import json
import pandas as pd
from texts_processing import TextsTokenizer
from data_types import Parameters

with open(os.path.join(os.getcwd(), "data", "config.json"), "r") as jf:
    config_dict = json.load(jf)

parameters = Parameters.parse_obj(config_dict)

stopwords = []
if parameters.stopwords_files:
    for filename in parameters.stopwords_files:
        root = os.path.join(os.getcwd(), "data", filename)
        stopwords_df = pd.read_csv(root, sep="\t")
        stopwords += list(stopwords_df["stopwords"])


# model = SentenceTransformer(os.path.join(PROJECT_ROOT_DIR, "models", "new_paraphrase.transformers")) # новый обученный трансформер
tokenizer = TextsTokenizer()
tokenizer.add_stopwords(stopwords)

queries_with_answers_df = pd.read_csv(os.path.join("data", "queries_with_answers_all.csv"), sep="\t")
queries_with_answers_dicts = queries_with_answers_df.to_dict(orient="records")

lem_queries_with_answers = []
for d in queries_with_answers_dicts:
    tokens = tokenizer([d["Query"]])[0]
    d["LemQuery"] = " ".join(tokens)
    d["LenQuery"] = len(tokens)
    d["LenEtalon"] = len(d["lem_etalon"].split())
    lem_queries_with_answers.append(d)

lem_queries_with_answers_df = pd.DataFrame(lem_queries_with_answers)
print(lem_queries_with_answers_df)

lem_queries_with_answers_df.to_csv(os.path.join("results", "lem_queries_with_answers.csv"), sep="\t", index=False)

etalons_df = pd.read_csv(os.path.join("data", "queries.tsv"), sep="\t")
etalons_tokens = [l_tx for l_tx in tokenizer(list(etalons_df["query"]))]
lem_etalons = [" ".join(l_tx) for l_tx in etalons_tokens]
len_etalons = [len(l_tx) for l_tx in etalons_tokens]

lem_etalons_df = pd.DataFrame(lem_etalons, columns=["lem_etalon"])
len_etalons_df = pd.DataFrame(len_etalons, columns=["len"])
etalons_df = pd.concat([etalons_df, lem_etalons_df, len_etalons_df], axis=1)
print(etalons_df)
etalons_df.to_csv(os.path.join("results", "lem_etalons_with_len.csv"), sep="\t", index=False)
