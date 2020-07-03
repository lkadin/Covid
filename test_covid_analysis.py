import covid_analysis
import pytest
import datatest as dt

@pytest.fixture(scope='module')
def df():
    return covid_analysis.prep_place('Florida')

@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {'date', 'place', 'fips', 'cases','deaths','state','change_in_cases','change_in_deaths'},
    )
