from extract_sanskrit_words_with_kmean_clustering import (syl_tokenizer,
                                                          syls_to_skrt_vectors)


def test_syl_tokenizer():
    text = "།།རྒྱ་གར་གྱི་མཁན་པོ་བིདྱཱ་ཀ་ར་པྲ་བྷཱ་དང་།"

    syls = syl_tokenizer(text)

    assert syls == [
        "།།",
        "རྒྱ་",
        "གར་",
        "གྱི་",
        "མཁན་",
        "པོ་",
        "བིདྱཱ་",
        "ཀ་",
        "ར་",
        "པྲ་",
        "བྷཱ་",
        "དང་",
        "།",
    ]


def test_syl_to_skrt_vectors():
    text = "།།རྒྱ་གར་གྱི་མཁན་པོ་བིདྱཱ་ཀ་ར་པྲ་བྷཱ་དང་།"
    syls = syl_tokenizer(text)

    skrt_vectors, mapping = syls_to_skrt_vectors(syls)

    expected_vector_result = [[6, 0], [10, 0]]
    expected_mapping_result = {0: 6, 1: 10}

    assert [list(i) for i in list(skrt_vectors)] == expected_vector_result
    assert mapping == expected_mapping_result
