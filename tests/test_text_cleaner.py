"""
Unit tests for text_cleaner module.
"""

import pytest
from core.utils.text_cleaner import clean_text


def test_excessive_spaces_removed():
    """Test that excessive spaces are cleaned to single spaces."""
    text = "Hello    world    this   is   a   test"
    result = clean_text(text)
    assert "    " not in result
    assert result == "Hello world this is a test"


def test_repeated_blank_lines_reduced():
    """Test that repeated blank lines are reduced to two newlines."""
    text = "Line 1\n\n\n\nLine 2\n\n\n\nLine 3"
    result = clean_text(text)
    # Should reduce multiple newlines to double newlines
    assert "\n\n\n" not in result
    assert "Line 1" in result and "Line 2" in result and "Line 3" in result


def test_leading_trailing_whitespace_removed():
    """Test that leading and trailing whitespace is stripped."""
    text = "   Hello World   "
    result = clean_text(text)
    assert result == "Hello World"
    assert not result.startswith(" ")
    assert not result.endswith(" ")


def test_empty_string_handled():
    """Test that empty string is handled gracefully."""
    result = clean_text("")
    assert result == ""


def test_none_value_handled():
    """Test that None value is handled gracefully."""
    result = clean_text(None)
    assert result == ""


def test_line_breaks_normalized():
    """Test that different line break formats are normalized."""
    text = "Line 1\r\nLine 2\rLine 3\nLine 4"
    result = clean_text(text)
    # All should be converted to \n
    assert "\r\n" not in result
    assert "\r" not in result