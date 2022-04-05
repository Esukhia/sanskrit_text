import re
from pathlib import Path
from typing import Dict, List

import numpy as np
from botok.third_party.has_skrt_syl import is_skrt
from sklearn.cluster import AgglomerativeClustering, KMeans


def syl_tokenizer(string: str) -> List[str]:
    chunks = re.split("(་|།།|།)", string)
    syls = []
    cur_syl = ""
    for chunk in chunks:
        if re.search("་|།།|།", chunk):
            cur_syl += chunk
            syls.append(cur_syl)
            cur_syl = ""
        else:
            cur_syl += chunk
    if cur_syl:
        syls.append(cur_syl)
    return syls


def syls_to_skrt_vectors(syls: List[str]):
    skrt_vector_idx_to_syls_idx = {}

    skrt_syl_counter = 0
    for idx, syl in enumerate(syls):
        if is_skrt(syl):
            skrt_vector_idx_to_syls_idx[skrt_syl_counter] = idx
            skrt_syl_counter += 1

    skrt_vectors = np.array([[i, 0] for i in skrt_vector_idx_to_syls_idx.values()])
    return skrt_vectors, skrt_vector_idx_to_syls_idx


def find_skrt_clusters_with_kmean(X):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    return list(kmeans.labels_)


def find_skrt_clusters_with_agglo(X):
    clustering = AgglomerativeClustering()
    clustering.fit(X)
    return list(clustering.labels_)


def convert_clusters_to_skrt_words(
    syls: List[str], clusters: List[int], mapping: Dict[int, int]
) -> List[str]:
    reversed_clusters = clusters[::-1]
    skrt_words_span = []
    cluster_idx = 0
    while cluster_idx <= len(clusters) - 1:
        cluster = clusters[cluster_idx]
        cluster_end_idx = (len(clusters) - 1) - reversed_clusters.index(cluster)
        skrt_words_span.append(
            (mapping[cluster_idx], mapping[cluster_end_idx])
        )
        cluster_idx = cluster_end_idx + 1

    return ["".join(syls[start : end + 1]) for start, end in skrt_words_span]


def extrack_skrt_words(text: str) -> List[str]:
    syls = syl_tokenizer(text)
    skrt_syls_vectors, vec_idx2syl_idx = syls_to_skrt_vectors(syls)
    if len(skrt_syls_vectors) < 2:
        return []
    clusters = find_skrt_clusters_with_kmean(skrt_syls_vectors)
    skrt_words = convert_clusters_to_skrt_words(syls, clusters, vec_idx2syl_idx)
    return skrt_words


def main():
    line_delimiter = "----"
    print("[INFO]: Extracking Sankrit words...")
    text_path = Path("./sanskrit_text")
    skrt_words_fn = text_path / "skrt_words.txt"
    all_skrt_words = []
    for fn in text_path.iterdir():
        print(f"\t- processing {fn.name}...")
        for n_line, line in enumerate(fn.read_text().splitlines()):
            skrt_words = extrack_skrt_words(line)
            if not skrt_words:
                continue
            all_skrt_words += skrt_words + [str(n_line + 1), line_delimiter]
        skrt_words_fn = text_path / f"{fn.stem}_words.txt"
        skrt_words_fn.write_text("\n".join(all_skrt_words))
        break


if __name__ == "__main__":
    main()
