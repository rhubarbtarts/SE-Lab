
from hypothesis import given, strategies as st
from museum_admission_parser import format_visitor_name, parse_group_ages, parse_visit_date


@given(st.text() | st.none())
def test_format_visitor_name_no_crash(s):
    try:
        format_visitor_name(s)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass


@given(st.text() | st.none())
def test_parse_group_ages_no_crash(s):
    try:
        parse_group_ages(s)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass


@given(st.text() | st.none())
def test_parse_visit_date_no_crash(s):
    try:
        parse_visit_date(s)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass
