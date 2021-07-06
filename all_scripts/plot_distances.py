import re
import pandas as pd
import matplotlib.pyplot as plt
import math
from collections import Counter
from statistics import mean

import gensim

import nltk
import numpy as np
import pandas as pd
import sklearn
from numpy import argmax
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')


def transform(lines):
    tokens = [w for s in lines for w in s]
    results = []
    label_enc = sklearn.preprocessing.LabelEncoder()
    onehot_enc = sklearn.preprocessing.OneHotEncoder()
    encoded_all_tokens = label_enc.fit_transform(list(set(tokens)))
    encoded_all_tokens = encoded_all_tokens.reshape(len(encoded_all_tokens), 1)
    onehot_enc.fit(encoded_all_tokens)
    for text_tokens in lines:
        encoded_words = label_enc.transform(text_tokens)
        encoded_words = encoded_words.reshape(len(encoded_words), 1)
        encoded_words = onehot_enc.transform(encoded_words)
        results.append(np.sum(encoded_words.toarray(), axis=0))
    return results


def calculate_position(values):
    x = []
    for pos, matrix in enumerate(values):
        if matrix > 0:
            x.append(pos)
    return x


def padding(sentence1, sentence2):
    x1 = sentence1.copy()
    x2 = sentence2.copy()
    diff = len(x1) - len(x2)
    if diff > 0:
        for i in range(0, diff):
            x2.append(-1)
    elif diff < 0:
        for i in range(0, abs(diff)):
            x1.append(-1)
    return x1, x2


def cosine(reviews):
    text_tokens = [nltk.word_tokenize(i) for i in reviews]
    transformed_results = transform([i for i in text_tokens])
    cosine_dist = []
    for i in range(len(reviews)):
        for j in range(len(reviews)):
            if i != j:
                score = sklearn.metrics.pairwise.cosine_similarity(
                    [transformed_results[i]], [transformed_results[j]])[0][0]
                rounded_score = "{:.2f}".format(score)
                cosine_dist.append(rounded_score)
    cosine_dist = list(map(float, cosine_dist))
    stats = {
        'min_val': min(cosine_dist),
        'max_val': max(cosine_dist),
        'mean_val': mean(cosine_dist)}
    return stats


def jaccard(reviews):
    text_tokens = [nltk.word_tokenize(i) for i in reviews]
    transformed_results = transform([i for i in text_tokens])
    jaccard_dist = []
    for i in range(len(reviews)):
        for j in range(len(reviews)):
            if i != j:
                y_actual = calculate_position(transformed_results[j])
                y_compare = calculate_position(transformed_results[i])
                x1, x2 = padding(y_actual, y_compare)
                score = 1 - gensim.matutils.jaccard(x1, x2)
                rounded_score = "{:.2f}".format(score)
                jaccard_dist.append(rounded_score)
    jaccard_dist = list(map(float, jaccard_dist))
    stats = {
        'min_val': min(jaccard_dist),
        'max_val': max(jaccard_dist),
        'mean_val': mean(jaccard_dist)}
    return stats


def cosine_rel(reviews):
    text_tokens = [nltk.word_tokenize(i) for i in reviews]
    transformed_results = transform([i for i in text_tokens])
    compare_with = transformed_results[0]
    cosine_dist = []
    for i in range(len(reviews)-1):
        score = sklearn.metrics.pairwise.cosine_similarity(
            compare_with, [transformed_results[i+1]])[0][0]
        rounded_score = "{:.2f}".format(score)
        cosine_dist.append(rounded_score)
    cosine_dist = list(map(float, cosine_dist))
    stats = {
        'min_val': min(cosine_dist),
        'max_val': max(cosine_dist),
        'mean_val': mean(cosine_dist)}
    return stats


def jaccard_rel(reviews):
    text_tokens = [nltk.word_tokenize(i) for i in reviews]
    transformed_results = transform([i for i in text_tokens])
    compare_with = transformed_results[0]
    y_actual = calculate_position(compare_with)
    jaccard_dist = []
    for i in range(len(reviews)-1):
        y_compare = calculate_position(transformed_results[i+1])
        x1, x2 = padding(y_actual, y_compare)
        score = 1 - gensim.matutils.jaccard(x1, x2)
        rounded_score = "{:.2f}".format(score)
        jaccard_dist.append(rounded_score)
    jaccard_dist = list(map(float, jaccard_dist))
    stats = {
        'min_val': min(jaccard_dist),
        'max_val': max(jaccard_dist),
        'mean_val': mean(jaccard_dist)}
    return stats


def make_df(reviews_folder_path):
    f = open(reviews_folder_path + 'shuffled_reviews.txt')
    row = []
    for x in f:
        grp = re.match(r'(.*)_(.*)\s=\s(.*)', x)
        review_no = grp.group(1)
        arxivId = str(grp.group(2))
        review = str(grp.group(3))
        row.append([review_no, arxivId, review])
    df = pd.DataFrame()
    df['review_no'] = [i[0] for i in row]
    df['arxivId'] = [i[1] for i in row]
    df['review'] = [i[2] for i in row]
    df.to_csv(reviews_folder_path + 'shuffled_reviews.csv', index=False)


def jaccard_plot(df, paper_ids, plots_path):
    fig, ax = plt.subplots()
    for i in range(len(paper_ids)):
        df_new = df[df['arxivId'] == paper_ids[i]]
        vals = jaccard(df_new['review'])
        ax.scatter(i + 1, vals['min_val'], c='blue', marker='.')
        ax.scatter(i + 1, vals['max_val'], c='red', marker='o')
        ax.scatter(i + 1, vals['mean_val'], c='green', marker='x')
    ax.legend(('min', 'max', 'mean'), loc=1, scatterpoints=1)
    plt.xticks(range(1, 7))
    plt.title("Jaccard Similarity")
    plt.xlabel("Papers")
    plt.ylabel("Similarity")
    plt.savefig(f'{plots_path}jaccard.jpg', dpi=100)
    plt.show()


def cosine_plot(df, paper_ids, plots_path):
    fig, ax = plt.subplots()
    for i in range(len(paper_ids)):
        df_new = df[df['arxivId'] == paper_ids[i]]
        vals = cosine(df_new['review'])
        ax.scatter(i + 1, vals['min_val'], c='blue', marker='.')
        ax.scatter(i + 1, vals['max_val'], c='red', marker='o')
        ax.scatter(i + 1, vals['mean_val'], c='green', marker='x')
    ax.legend(('min', 'max', 'mean'), loc=1, scatterpoints=1)
    plt.xticks(range(1, 7))
    plt.title("Cosine Similarity")
    plt.xlabel("Papers")
    plt.ylabel("Similarity")
    plt.savefig(f'{plots_path}cosine.jpg', dpi=100)
    plt.show()


def Plot_Distances(paper_ids, reviews_folder_path, plots_path):

    make_df(reviews_folder_path)

    df = pd.read_csv(f'{reviews_folder_path}shuffled_reviews.csv')
    df = df.astype("string")

    cosine_plot(df, paper_ids, plots_path)
    jaccard_plot(df, paper_ids, plots_path)

# paper_list_path = "../paper_list.txt"
# reviews_folder_path = "./reviews/"
# plots_path = "./results/"
