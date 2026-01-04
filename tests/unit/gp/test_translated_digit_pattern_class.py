"""
Unit tests for the `textfsmgen.gp.TranslatedDigitPattern` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/gp/test_translated_digit_pattern_class.py
    or
    $ python -m pytest tests/unit/gp/test_translated_digit_pattern_class.py
"""

import pytest

from textfsmgen.gp import (
TranslatedPattern,
TranslatedDigitPattern,
TranslatedDigitsPattern,
TranslatedNumberPattern,
TranslatedMixedNumberPattern,
# TranslatedLetterPattern,
# TranslatedLettersPattern,
TranslatedAlphabetNumericPattern,
# TranslatedPunctPattern,
# TranslatedPunctsPattern,
# TranslatedPunctsGroupPattern,
# TranslatedGraphPattern,
TranslatedWordPattern,
TranslatedWordsPattern,
TranslatedMixedWordPattern,
TranslatedMixedWordsPattern,
TranslatedNonWhitespacePattern,
TranslatedNonWhitespacesPattern,
TranslatedNonWhitespacesGroupPattern
)

from tests.unit.gp import TranslatedDummyPattern

to_list = lambda arg: arg if isinstance(arg, (list, tuple)) else [arg]


class TestTranslatedDigitPatternClass:
    """Test suite for TranslatedDigitPattern class."""

    def setup_method(self):
        """Create a baseline TranslatedDigitPattern instance for reuse."""
        self.digit_node = TranslatedDigitPattern("1", "2", "3")

    @pytest.mark.parametrize(
        "other",
        [
            "1",                # digit is a subset of digit
            "123",              # digit is a subset of digits
            "1.1",              # digit is a subset of number
            "-1.1",             # digit is a subset of mixed number
            ["a", "1"],         # digit is a subset of alphabet numeric
            ["a", "1", "#"],    # digit is a subset of graph
            "abc123",           # digit is a subset of word
            "a1 b12",           # digit is a subset of words
            "abc.123",          # digit is a subset of mixed word
            "a.1 b.2",          # digit is a subset of mixed words
            "\xc8",             # digit is a subset of non-whitespace
            "abc\xc8",          # digit is a subset of non-whitespaces
            "abc\xc8 xyz",      # digit is a subset of non-whitespace group
        ],
    )
    def test_is_subset_of(self, other):
        """
        Verify that a digit data is correctly identified as a subset of
        broader translated categories, including digits, numbers, graphs,
        words, and non‑whitespace.
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.digit_node.is_subset_of(other_instance) is True

    @pytest.mark.parametrize(
        "other",
        [
            "abc",              # digit is not a subset of letter(s)
            "++--",             # digit is not a subset of punctuation(s)
            "++ -- ==",         # digit is not a subset of punctuation group
        ],
    )
    def test_is_not_subset_of(self, other):
        """
        Verify that a digit data is not a subset of letters or punctuations
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.digit_node.is_subset_of(other_instance) is False

    @pytest.mark.parametrize(
        "other",
        [
            "1",                # digit is not a superset of digit
            "123",              # digit is not a superset of digits
            "1.1",              # digit is not a superset of number
            "abc\xc8 xyz",      # digit is not a superset of non-whitespace group
        ],
    )
    def test_is_superset_of(self, other):
        """
        Verify that a digit data is correctly identified as not belonging
        to any broader translated category.
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.digit_node.is_superset_of(other_instance) is False

    @pytest.mark.parametrize(
        "data, expected_class",
        [
            (
                "1",    # digit
                # When a digit is combined with a digit,
                # the recommendation should produce a digit pattern.
                TranslatedDigitPattern
            ),
            (
                "123",  # digits
                # When a digit is combined with digits,
                # the recommendation should produce a digits pattern.
                TranslatedDigitsPattern
            ),
            (
                "1.1",  # number
                # When a digit is combined with a number,
                # the recommendation should produce a number pattern.
                TranslatedNumberPattern
            ),
            (
                "-1.1", # mixed number
                # When a digit is combined with a mixed number,
                # the recommendation should produce a mixed number pattern.
                TranslatedMixedNumberPattern
            ),
            (
                "abc123",   # a word
                # When a digit is combined with a word,
                # the recommendation should produce a word pattern.
                TranslatedWordPattern
            ),
            (
                "a1 a12",   # words
                # When a digit is combined with words,
                # the recommendation should produce words pattern.
                TranslatedWordsPattern
            ),
            (
                "abc.123",  # a mixed word
                # When a digit is combined with a mixed word,
                # the recommendation should produce a mixed word pattern.
                TranslatedMixedWordPattern
            ),
            (
                "a.1 b.1",  # mixed words
                # When a digit is combined with mixed words,
                # the recommendation should produce mixed words pattern.
                TranslatedMixedWordsPattern
            ),
            (
                "\xc8",  # a non-whitespace
                # When a digit is combined with a non-whitespace,
                # the recommendation should produce non-whitespace pattern.
                TranslatedNonWhitespacePattern
            ),
            (
                "abc\xc8",  # non-whitespaces
                # When a digit is combined with non-whitespaces,
                # the recommendation should produce non-whitespaces pattern.
                TranslatedNonWhitespacesPattern
            ),
            (
                "abc\xc8 xyz",  # non-whitespace group
                # When a digit is combined with non-whitespaces,
                # the recommendation should produce non-whitespace group pattern.
                TranslatedNonWhitespacesGroupPattern
            ),
        ],
    )
    def test_recommend_method_case_subset(self, data, expected_class):
        """
        Verify that a digit type correctly recommends a subset type
        when combined with compatible data.
        """
        args = to_list(data)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.digit_node.recommend(other)
        assert isinstance(recommend_instance, expected_class)

    @pytest.mark.parametrize(
        "data, expected_class",
        [
            (
                "a",    # a letter
                # When a digit is combined with a letter,
                # the recommendation should produce an alphabet numeric pattern.
                TranslatedAlphabetNumericPattern
            ),
            (
                "ab",  # letters
                # When a digit is combined with letters,
                # the recommendation should produce a word pattern.
                TranslatedWordPattern
            ),
            (
                "+",  # a punctuation
                # When a digit is combined with a punctuation,
                # the recommendation should produce a punctuation pattern.
                TranslatedNonWhitespacePattern
            ),
            (
                "++",  # punctuations
                # When a digit is combined with punctuations,
                # the recommendation should produce punctuations pattern.
                TranslatedNonWhitespacesPattern
            ),
            (
                "++ -- ==",  # punctuation group
                # When a digit is combined with punctuation group,
                # the recommendation should produce punctuation group pattern.
                TranslatedNonWhitespacesGroupPattern
            ),
        ],
    )
    def test_recommend_method_case_aggregating(self, data, expected_class):
        """
        Verify that a digit type correctly recommends a subset type
        when combined with compatible data.

            ["a", "1"],         # digit is a subset of alphabet numeric
            ["a", "1", "#"],    # digit is a subset of graph
            "abc123",           # digit is a subset of word
            "a1 b12",           # digit is a subset of words
            "abc.123",          # digit is a subset of mixed word
            "a.1 b.2",          # digit is a subset of mixed words
            "\xc8",             # digit is a subset of non-whitespace
            "abc\xc8",          # digit is a subset of non-whitespaces
            "abc\xc8 xyz",      # digit is a subset of non-whitespaces
        """
        args = to_list(data)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.digit_node.recommend(other)
        assert isinstance(recommend_instance, expected_class)