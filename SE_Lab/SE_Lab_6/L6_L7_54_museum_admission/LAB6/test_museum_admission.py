
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# Original example tests
def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_small_group():
    assert group_discount(4, False) == 0


# ticket_price tests
def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("invalid", 30, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_child_under_five():
    assert ticket_price("child", 4, "tuesday", False) == 0


def test_age_five():
    assert ticket_price("child", 5, "tuesday", False) == 100


def test_student_price():
    assert ticket_price("student", 20, "tuesday", False) == 150


def test_senior_price():
    assert ticket_price("senior", 70, "tuesday", False) == 200


def test_monday_half_price():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_saturday_surcharge():
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_sunday_surcharge():
    assert ticket_price("adult", 30, "sunday", False) == 350


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_non_student_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


def test_weekend_guided_tour():
    assert ticket_price("adult", 30, "sunday", True) == 450


# group_discount tests
def test_invalid_group_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_school_group_of_twenty():
    assert group_discount(20, True) == 40


def test_school_group_below_twenty():
    assert group_discount(19, True) == 25


def test_non_school_group_of_fifteen():
    assert group_discount(15, False) == 20


def test_non_school_group_of_eight():
    assert group_discount(8, False) == 10


def test_non_school_group_below_eight():
    assert group_discount(7, False) == 0


# gallery_entry tests
def test_gallery_at_capacity():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_over_capacity():
    assert gallery_entry(101, 100, True) == "wait"


def test_gallery_at_ninety_percent_without_slot():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_at_ninety_percent_with_slot():
    assert gallery_entry(90, 100, True) == "enter"


def test_gallery_below_ninety_percent():
    assert gallery_entry(89, 100, False) == "enter"


def test_empty_gallery():
    assert gallery_entry(0, 100, False) == "enter"
