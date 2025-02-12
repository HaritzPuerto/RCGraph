#!/usr/bin/env python
# encoding: utf-8

import json
import rdflib
import sys
import unicodedata


def scrub_unicode (text):
    """
    try to handle the unicode edge cases encountered in source text,
    as best as possible
    """
    x = " ".join(map(lambda s: s.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace("`` ", '"').replace("''", '"')
    x = x.replace('…', '...').replace("\\u2026", "...")
    x = x.replace("\\u00ae", "").replace("\\u2122", "")
    x = x.replace("\\u00a0", " ").replace("\\u2022", "*").replace("\\u00b7", "*")
    x = x.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u201a", "'")
    x = x.replace("\\u201c", '"').replace("\\u201d", '"')

    x = x.replace("\\u20ac", "€")
    x = x.replace("\\u2212", " - ") # minus sign

    x = x.replace("\\u00e9", "é")
    x = x.replace("\\u017c", "ż").replace("\\u015b", "ś").replace("\\u0142", "ł")    
    x = x.replace("\\u0105", "ą").replace("\\u0119", "ę").replace("\\u017a", "ź").replace("\\u00f3", "ó")

    x = x.replace("\\u2014", " - ").replace('–', '-').replace('—', ' - ')
    x = x.replace("\\u2013", " - ").replace("\\u00ad", " - ")

    x = str(unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))

    # some content returns text in bytes rather than as a str ?
    try:
        assert type(x).__name__ == "str"
    except AssertionError:
        print("not a string?", type(x), x)

    return x


def write_jsonld (filename, graph, vocab="vocab.json"):
    """
    serialize the given graph a JSON-LD output
    """
    with open(vocab, "r") as f:
        context = json.load(f)

    with open(filename, "wb") as f:
        f.write(graph.serialize(format="json-ld", context=context, indent=2))


if __name__ == "__main__":
    # load the graph
    filename = sys.argv[1]
    graph = rdflib.Graph().parse(filename, format="n3")

    # enumerate all of the relations
    for subj, pred, obj in graph:
        print(subj, pred, obj)

    # serialize the graph as JSON-LD
    filename = "tmp.jsonld"
    write_jsonld(filename, graph)
