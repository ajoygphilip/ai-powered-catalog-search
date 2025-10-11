from elasticsearch.dsl import analyzer, char_filter, token_filter

description_analyzer = analyzer(
    "description_analyzer",
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"],
)

special_characters_filter = char_filter(
    "special_characters_filter",
    type="pattern_replace",
    pattern="[^A-Za-z0-9 ]",
    replacement="",
)

edge_ngram_completion_filter = token_filter(
    "edge_ngram_completion_filter", type="edge_ngram", min_gram=2, max_gram=8
)

sku_edge_ngram_completion_analyzer = analyzer(
    "sku_edge_ngram_completion",
    tokenizer="whitespace",
    filter=["lowercase", "stop", edge_ngram_completion_filter],
    char_filter=special_characters_filter,
)

english_analyzer = analyzer("english")
