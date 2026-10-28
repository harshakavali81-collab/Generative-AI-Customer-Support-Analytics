from src.analytics.metrics import connection, record, summary, unanswered_report
def test_metrics_and_unanswered(tmp_path):
    db=tmp_path/"events.db"
    record(db,"shipping",True,42,2,30)
    record(db,"refund",False,89,0,24)
    s=summary(db)
    assert s["total_questions"]==2 and s["answer_rate_pct"]==50.0
    assert s["unanswered"]==1
    assert unanswered_report(db)==[{"topic":"refund","count":1}]
    with connection(db) as c:
        columns=[r[1] for r in c.execute("PRAGMA table_info(events)")]
    assert "question" not in columns and "message" not in columns
