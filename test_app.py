import pytest
from dash.testing.application_runners import import_app


# shared fixture so i dont have to start the server in each test
@pytest.fixture
def app_runner(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    return dash_duo


# checks the h1 heading is on the page with the right text
def test_header_present(app_runner):
    app_runner.wait_for_element("h1", timeout=10)
    header = app_runner.find_element("h1")
    assert "Pink Morsel Sales Visualiser" in header.text


# makes sure the chart actualy renders
def test_chart_present(app_runner):
    app_runner.wait_for_element("#sales-chart", timeout=10)
    chart = app_runner.find_element("#sales-chart")
    assert chart is not None


# checks the region radio buttons are there
def test_region_picker_present(app_runner):
    app_runner.wait_for_element("#region-filter", timeout=10)
    picker = app_runner.find_element("#region-filter")
    assert picker is not None
