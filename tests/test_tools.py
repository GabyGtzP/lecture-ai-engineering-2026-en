"""Tool tests (no LLM or API key used)."""

import json

from app import tools


def test_glossary_ids_are_unique_and_related_links_exist():
    terms = tools.load_glossary()
    ids = [t["id"] for t in terms]
    assert len(ids) == len(set(ids))
    for t in terms:
        for r in t["related"]:
            assert r in ids, f"{t['id']} has a nonexistent id in related: {r}"


def test_search_finds_term_by_name_and_alias():
    for query in ["LoRA", "lora", "Low-Rank Adaptation"]:
        hits = json.loads(tools.search_glossary(query))
        assert hits[0]["term"] == "LoRA", query


def test_search_finds_course_specific_term():
    hits = json.loads(tools.search_glossary("lecNN-start"))
    assert hits[0]["term"] == "lecNN-start tag"


def test_search_limits_number_of_results():
    hits = json.loads(tools.search_glossary("agent"))
    assert 1 <= len(hits) <= tools.MAX_RESULTS


def test_search_reports_not_found():
    assert "was not found" in tools.search_glossary("nonexistent-term-xyz")


def test_lecture_summary():
    assert "agent" in tools.get_lecture_summary(3)
    assert "not available yet" in tools.get_lecture_summary(99)


def test_hybrid_retrieval_merges_adjacent_pages(monkeypatch):
    from app import retrieval

    pages = [
        {"page_id": "lec03-main-p039", "document_id": "lec03-main", "lecture": 3,
         "page": 39, "title": "Claude", "content": "Compaction and memory"},
        {"page_id": "lec03-main-p040", "document_id": "lec03-main", "lecture": 3,
         "page": 40, "title": "OpenClaw", "content": "Daily notes"},
    ]
    monkeypatch.setattr(retrieval, "search",
                        lambda query: [{"page_id": "lec03-main-p039",
                                        "document_id": "lec03-main",
                                        "distance": 0.1}])
    graph_calls = []
    monkeypatch.setattr(retrieval, "search_graph",
                        lambda query, seeds=None: graph_calls.append(seeds) or
                        {"seeds": [], "expanded": [], "max_hops": 2})
    monkeypatch.setattr(retrieval, "load_pages", lambda source=None: pages)

    result = retrieval.search_hybrid("compaction memory")
    ids = {page["page_id"] for page in result["seeds"] + result["expanded"]}
    assert "lec03-main-p039" in ids
    assert "lec03-main-p040" in ids
    assert graph_calls == [[{"page_id": "lec03-main-p039",
                             "document_id": "lec03-main",
                             "distance": 0.1}]]


def test_default_question_of_lecture1_is_answerable_from_glossary():
    """The Lecture 03 agent can correctly answer the Lecture 01 default question (app.ask) using the glossary."""
    from app.ask import DEFAULT_QUESTION

    assert "3 homework levels" in DEFAULT_QUESTION
    hits = json.loads(tools.search_glossary("3 homework levels"))
    assert hits[0]["term"] == "3 homework levels"
