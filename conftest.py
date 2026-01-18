import os
import shutil
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
from allure_commons.types import AttachmentType

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
SCREENSHOT_DIR = os.path.join(ARTIFACTS_DIR, "screenshots")
VIDEO_DIR = os.path.join(ARTIFACTS_DIR, "videos")
LOG_DIR = os.path.join(BASE_DIR, "logs")
ALLURE_RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")

# ---------- CLEANUP BEFORE TESTS START ----------


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Runs once before the test session starts.
    Ensures a clean workspace for artifacts and reports.
    Safe for local, CI, and parallel execution.
    """
    for path in [
        SCREENSHOT_DIR,
        VIDEO_DIR,
        LOG_DIR,
        ALLURE_RESULTS_DIR,
    ]:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)


# ---------- PAGE FIXTURE (UI TESTS ONLY) ----------


@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 720},
        )

        page = context.new_page()
        yield page

        # ---------- ATTACH ARTIFACTS ON FAILURE ONLY ----------

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name

            # Screenshot
            screenshot_path = os.path.join(
                SCREENSHOT_DIR, f"{test_name}_{timestamp}.png"
            )

            page.screenshot(path=screenshot_path, full_page=True)

            if os.path.exists(screenshot_path):
                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=AttachmentType.PNG,
                )

            # Video (DEFENSIVE — REQUIRED)
            if page.video:
                video_path = page.video.path()
                if video_path and os.path.exists(video_path):
                    allure.attach.file(
                        video_path,
                        name="Failure Video",
                        attachment_type=AttachmentType.WEBM,
                    )

        context.close()
        browser.close()


# ---------- PYTEST REPORT HOOK ----------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures test result status for use in fixtures.
    Required for failure-based attachments.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# def pytest_collection_modifyitems(config, items):
#     for item in items:
#         if "auth" in item.keywords:
#             item.add_marker(
#                 pytest.mark.skip(
#                     reason="Authentication handled by gateway; use mock auth service"
#                 )
#             )
