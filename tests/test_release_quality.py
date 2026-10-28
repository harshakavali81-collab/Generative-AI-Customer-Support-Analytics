from scripts.check_assets import validate
from scripts.evaluate import evaluate

def test_project_visuals_and_static_demo_sources():
    r = validate()
    assert r["status"] == "ok"
    assert r["original_svg_count"] == 10
    assert r["browser_demo_policies"] == 6
    assert r["verified_internal_references"] >= 2

def test_authored_fixture_source_provenance_regression():
    r = evaluate()
    assert r["n"] == 16
    assert r["retrieval_hit_at_3"] == r["answerable"]
    assert r["unsupported_abstentions"] == r["unsupported"]
    # Citation validity is reported separately from retrieval recall and
    # never misrepresented as human-judged answer correctness.
    assert 0 <= r["supported_queries_with_valid_citation_ids"] <= r["answerable"]
