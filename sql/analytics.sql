-- SQLite reporting queries; app persists only aggregate-friendly metadata.
SELECT DATE(created_at) AS day, COUNT(*) AS questions,
 ROUND(100.0 * AVG(answered), 1) AS answer_rate_pct,
 ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM events GROUP BY DATE(created_at) ORDER BY day DESC;

SELECT topic, COUNT(*) AS questions,
 SUM(CASE WHEN answered = 0 THEN 1 ELSE 0 END) AS unanswered
FROM events GROUP BY topic ORDER BY unanswered DESC;

SELECT CASE WHEN latency_ms < 100 THEN '<100 ms'
 WHEN latency_ms < 500 THEN '100-499 ms'
 ELSE '500+ ms' END AS bucket, COUNT(*) AS queries
FROM events GROUP BY bucket;
