from typing import Dict, List
import json

import requests


URL = "https://model-apis.semanticscholar.org/specter/v1/invoke"
MAX_BATCH_SIZE = 16


def chunks(lst, chunk_size=MAX_BATCH_SIZE):
    """Splits a longer list to respect batch size"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i: i + chunk_size]


# SAMPLE_PAPERS = [
#     {
#         "paper_id": "A",
#         "title": "Hello world!",
#         "abstract": "Hello world!",
#     }
# ]


def embed(papers):
    embeddings_by_paper_id: Dict[str, List[float]] = {}

    for chunk in chunks(papers):
        # Allow Python requests to convert the data above to JSON
        response = requests.post(URL, json=chunk)

        if response.status_code != 200:
            raise RuntimeError(
                "Sorry, something went wrong, please try later!")

        for paper in response.json()["preds"]:
            embeddings_by_paper_id[paper["paper_id"]] = paper["embedding"]

    return embeddings_by_paper_id


def Embeddings(SAMPLE_PAPERS):
    all_embeddings = embed(SAMPLE_PAPERS)

    # Prints { 'A': [4.089589595794678, ...], 'B': [-0.15814849734306335, ...]
    # }
    print(all_embeddings)
    return all_embeddings
