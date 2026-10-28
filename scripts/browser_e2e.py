"""Real Chromium smoke test for static browser demo; no external hosted service."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "browser-test-output"

class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def check(page):
    errors = []
    remote_requests = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: remote_requests.append(request.url)
            if urlparse(request.url).hostname not in {"127.0.0.1", "localhost"} else None)
    page.goto("http://127.0.0.1:8090/", wait_until="networkidle")
    page.locator(".source-card").first.wait_for(state="attached")
    assert page.locator(".source-card").count() == 6, "Expected six fictional policies"

    page.get_by_role("button", name="How many days do refunds take?").click()
    assert page.locator(".msg.assistant").count() == 2
    reply = page.locator(".msg.assistant").last
    assert "[source:" in reply.inner_text(), "Refund FAQ lacks a source"
    assert reply.locator("details.evidence").count() == 1, "Evidence disclosure missing"

    page.locator("#question").fill("What is the CEO's phone number?")
    page.locator("#chat-form button").click()
    assert page.locator(".msg.assistant").count() == 3
    assert "couldn't verify" in page.locator(".msg.assistant").last.inner_text().lower()

    page.locator("[data-view='analytics']").click()
    assert page.locator("#analytics").is_visible()
    assert page.locator("#stat-queries").inner_text() == "2"
    assert page.locator("#stat-unanswered").inner_text() == "1"
    assert page.locator("#stat-coverage").inner_text() == "50%"

    page.locator("[data-view='sources']").click()
    assert page.locator("#sources").is_visible()
    assert page.locator(".source-card").count() == 6
    assert not errors, "Browser JavaScript errors: " + repr(errors)
    assert not remote_requests, "Unexpected external network calls: " + repr(remote_requests)

def main():
    OUTPUT.mkdir(exist_ok=True)
    handler = partial(SilentHandler, directory=str(ROOT / "site"))
    server = ThreadingHTTPServer(("127.0.0.1", 8090), handler)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
            try:
                desktop = browser.new_page(viewport={"width": 1440, "height": 900},
                                           device_scale_factor=1)
                check(desktop)
                desktop.locator("[data-view='chat']").click()
                desktop.screenshot(path=str(OUTPUT / "desktop-chat.png"), full_page=True)
                desktop.locator("[data-view='analytics']").click()
                desktop.screenshot(path=str(OUTPUT / "desktop-analytics.png"), full_page=True)
                desktop.close()
                mobile = browser.new_page(viewport={"width": 390, "height": 844},
                                          device_scale_factor=1)
                check(mobile)
                mobile.locator("[data-view='chat']").click()
                mobile.screenshot(path=str(OUTPUT / "mobile-chat.png"), full_page=True)
                mobile.close()
                print("Browser E2E PASS: desktop + mobile, citations, abstention, "
                      "six sources, analytics, no external network calls; "
                      "screenshots written to browser-test-output")
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
