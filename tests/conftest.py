"""Fixtures independientes y evidencias reales por ejecución y caso."""
import json
import os
import platform
import sys
from datetime import datetime, timedelta, timezone
from importlib.metadata import version
from pathlib import Path
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BASE_URL, TIMEOUT, USERNAME, PASSWORD
from pages.login_page import LoginPage

LOCAL_TZ = timezone(timedelta(hours=-6))


def now():
    return datetime.now(LOCAL_TZ).isoformat(timespec='seconds')


def pytest_configure(config):
    stamp = datetime.now(LOCAL_TZ).strftime('%Y%m%d_%H%M%S_%f')
    config.evidence_dir = Path('reports') / stamp
    config.evidence_dir.mkdir(parents=True, exist_ok=False)
    config.case_results = {}
    config.environment = {
        'started': now(), 'timezone': 'America/Guatemala (UTC-06:00)',
        'os': platform.platform(), 'python': sys.version, 'executable': sys.executable,
        'packages': {p: version(p) for p in ('selenium', 'pytest', 'pytest-html')},
        'base_url': BASE_URL, 'timeout_seconds': TIMEOUT,
        'headless': os.getenv('HEADLESS', '0') == '1',
        'command': [sys.executable, '-m', 'pytest', *sys.argv[1:]],
    }


@pytest.fixture
def observed(request):
    values = {}
    request.node.observations = values
    return values


@pytest.fixture
def driver(request):
    options = Options()
    if os.getenv('HEADLESS', '0') == '1':
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,1000')
    options.add_argument('--disable-features=PasswordLeakDetection')
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_manager_leak_detection': False,
    })
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)
    request.node.browser = browser
    request.config.environment['browser'] = browser.capabilities
    try:
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    case_id = 'CP-' + item.name.split('_')[1][2:]
    result = item.config.case_results.setdefault(case_id, {
        'id': case_id, 'test': item.nodeid, 'timestamp': now(), 'phases': {},
    })
    result['phases'][report.when] = {
        'outcome': report.outcome, 'duration_seconds': report.duration,
    }
    if report.failed:
        result['error'] = str(report.longrepr)
    result['status'] = ('No ejecutado' if report.when == 'setup' and report.failed
                        else result.get('status', 'No ejecutado'))
    if report.when == 'call':
        result['status'] = {'passed': 'Aprobado', 'failed': 'Reprobado',
                            'skipped': 'No ejecutado'}[report.outcome]
        result['observed'] = getattr(item, 'observations', {})
    if report.when == 'teardown' and report.failed:
        result['status'] = 'Error de cierre'
    browser = getattr(item, 'browser', None)
    if browser and (report.when == 'call' or (report.when == 'setup' and report.failed)):
        try:
            result['url'] = browser.current_url
            result['locators'] = getattr(browser, 'locator_checks', [])
            path = item.config.evidence_dir / f'{case_id}.png'
            if not browser.save_screenshot(str(path)):
                raise RuntimeError('WebDriver no guardó la captura')
            result['screenshot'] = path.as_posix()
            report.extras = [*getattr(report, 'extras', []),
                             pytest_html.extras.png(browser.get_screenshot_as_base64())]
        except Exception as exc:
            result['evidence_error'] = str(exc)


def pytest_sessionfinish(session, exitstatus):
    config = session.config
    config.environment.update({'finished': now(), 'pytest_exit_code': int(exitstatus)})
    for name, data in [('environment', config.environment), ('results', config.case_results)]:
        (config.evidence_dir / f'{name}.json').write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


@pytest.fixture
def logged_in(driver):
    page = LoginPage(driver).open()
    page.login(USERNAME, PASSWORD)
    page.wait_path('/inventory.html')
    return driver
