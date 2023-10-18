import os
from random import choice
import pandas as pd

etalons_df = pd.read_csv(os.path.join("data", "lem_etalons_with_len.csv"), sep="\t")

es_queries_df = pd.read_csv(os.path.join("results", "lem_queries_with_answers.csv"), sep="\t")
es_queries_dicts = es_queries_df.to_dict(orient="records")

lem_queries_with_short_etalons = []
for d in es_queries_dicts:
    temp_df = etalons_df[etalons_df["id"] == d["templateId"]]
    temp_df_ = temp_df[temp_df["len"] == 5]
    if temp_df.shape[0] > 0:
        if temp_df_.shape[0] == 0:
            temp_df = temp_df[temp_df["len"] == temp_df["len"].min()]
        temp_tuples = list(temp_df.itertuples())
        short_etalon = choice(temp_tuples)
        d["ShortEtalon"] = short_etalon.query
        d["ShortLemEtalon"] = short_etalon.lem_etalon
        d["LenShortEtalon"] = short_etalon.len
        lem_queries_with_short_etalons.append(d)
        print(short_etalon)

print(lem_queries_with_short_etalons)
lem_queries_with_short_etalons_df = pd.DataFrame(lem_queries_with_short_etalons)
lem_queries_with_short_etalons_df.to_csv(os.path.join("results", "lem_queries_with_short_etalons.csv"), sep='\t', index=False)