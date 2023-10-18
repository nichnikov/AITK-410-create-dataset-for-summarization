import os
import pandas as pd
import requests

queies_df = pd.read_csv(os.path.join("data", "LongQueries.csv"), sep="\t")
print(queies_df)
queries_dicts = queies_df.to_dict(orient="records")
test_results = []
for num, d in enumerate(queries_dicts):
    try:
        q = d["Query"]
        print(num, "/", len(queries_dicts), q)
        q_request = {"pubid": 9, "text": q}
        res = requests.post("http://srv01.nlp.dev.msk2.sl.amedia.tech:4002/api/search", json=q_request)
        res_d = res.json()
        test_results.append({**d, **res_d})
    except:
        print("There is problem witgh input dict {}".format(d))

test_results_df = pd.DataFrame(test_results)
print(test_results_df)
test_results_df.to_csv(os.path.join("results", "queries_with_answers.csv"), sep="\t", index=False)