# Chromium browser QA

The static browser-only `site/` demonstration has an automated end-to-end check running in GitHub Actions on every push.

```bash
python -m pip install playwright==1.58.0
python -m playwright install chromium
python -m scripts.browser_e2e
```

The test starts an HTTP server bound to 127.0.0.1:8090 and launches Chromium at both 1440×900 and 390×844. It verifies six fictional policy records, a sample cited refund answer, unsupported-question abstention, dynamic analytics counts, view navigation, and lack of third-party requests. It saves **real browser screenshots** to `browser-test-output/` and uploads them as short-lived GitHub Actions artifacts.

This tests the **standalone static browser showcase** and **does not** prove the publicly hosted URL works, nor does it exercise the separate Python/React full stack. The 16-case fixture remains authored synthetic evaluation, not real-world quality benchmarking.
