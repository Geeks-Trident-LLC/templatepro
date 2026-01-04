"""
Unit tests for the `textfsmgen.gp.TranslatedNumberPattern` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/gp/test_translated_number_pattern_class.py
    or
    $ python -m pytest tests/unit/gp/test_translated_number_pattern_class.py
"""

import pytest

from textfsmgen.gp import (
TranslatedPattern,
# TranslatedDigitPattern,
# TranslatedDigitsPattern,
TranslatedNumberPattern,
TranslatedMixedNumberPattern,
# TranslatedLetterPattern,
# TranslatedLettersPattern,
# TranslatedAlphabetNumericPattern,
# TranslatedPunctPattern,
# TranslatedPunctsPattern,
# TranslatedPunctsGroupPattern,
# TranslatedGraphPattern,
# TranslatedWordPattern,
# TranslatedWordsPattern,
TranslatedMixedWordPattern,
TranslatedMixedWordsPattern,
# TranslatedNonWhitespacePattern,
TranslatedNonWhitespacesPattern,
TranslatedNonWhitespacesGroupPattern
)

to_list = lambda arg: arg if isinstance(arg, (list, tuple)) else [arg]


class TestTranslatedNumberPatternClass:
    """Test suite for TranslatedNumberPattern class."""

    def setup_method(self):
        """Create a baseline TranslatedNumberPattern instance for reuse."""
        self.number_node = TranslatedNumberPattern("1.1")

    @pytest.mark.parametrize(
        "other",
        [
            "1.1",              # number is a subset of number
            "-1.1",             # number is a subset of mixed number
            "abc\xc8",          # number is a subset of non-whitespaces
            "abc\xc8 xyz",      # number is a subset of non-whitespace group
        ],
    )
    def test_is_subset_of(self, other):
        """
        Verify that number is a subset of (number, mixed number,
        non-whitespaces, non-whitespace-group)
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.number_node.is_subset_of(other_instance) is True

    @pytest.mark.parametrize(
        "other",
        [
            "1",                # number is not a subset of digit
            "123",              # number is not a subset of digits
            "a",                # number is not a subset of letter
            "abc",              # number is not a subset of letter(s)
            "+",                # number is not a subset of punctuation
            "++--",             # number is not a subset of punctuation(s)
            "++ -- ==",         # number is not a subset of punctuation group
            "\xc8",             # number is not a subset of non-whitespace
        ],
    )
    def test_is_not_subset_of(self, other):
        """
        Verify that number is not a subset of (digit, digits, letter(s),
        punctuation(s), punctuation group, non-whitespace)
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.number_node.is_subset_of(other_instance) is False

    @pytest.mark.parametrize(
        "other",
        [
            "1",                # number is a superset of digit
            "123",              # number is a superset of digits
        ],
    )
    def test_is_superset_of(self, other):
        """
        Verify that number is a superset of (digit, digits).
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.number_node.is_superset_of(other_instance) is True

    @pytest.mark.parametrize(
        "number, expected_class",
        [
            (
                "1.1",  # number
                # When number is combined with a number,
                # the recommendation should produce a number pattern.
                TranslatedNumberPattern
            ),
            (
                "-1.1", # mixed number
                # When number is combined with a mixed number,
                # the recommendation should produce a mixed number pattern.
                TranslatedMixedNumberPattern
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
    def test_recommend_method_case_subset(self, number, expected_class):
        """
        Verify that a number type correctly recommends a subset type
        when combined with compatible number.
        """
        args = to_list(number)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.number_node.recommend(other)
        assert isinstance(recommend_instance, expected_class)

    @pytest.mark.parametrize(
        "number, expected_class",
        [
            (
                "1",    # digit
                # When number are combined with a digit,
                # the recommendation should produce number pattern.
                TranslatedNumberPattern
            ),
            (
                "12",  # digits
                # When number are combined with digits,
                # the recommendation should produce number pattern.
                TranslatedNumberPattern
            ),
        ],
    )
    def test_recommend_method_case_superset(self, number, expected_class):
        """
        Verify that a digit type correctly recommends a subset type
        when combined with compatible number.
        """
        args = to_list(number)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.number_node.recommend(other)
        assert isinstance(recommend_instance, expected_class)

    @pytest.mark.parametrize(
        "number, expected_class",
        [
            # When a number is combined with letters, alphanumeric characters,
            # graphs, or words,
            # the recommendation should produce a TranslatedMixedWordPattern.
            (
                "a",  # letter
                TranslatedMixedWordPattern
            ),
            (
                "ab",  # letters
                TranslatedMixedWordPattern
            ),
            (
                ["a", "1"], # an alphabet or numeric
                TranslatedMixedWordPattern
            ),
            (
                ["a", "1", "#"], # a graph character
                TranslatedMixedWordPattern
            ),
            (
                "abc123",   # a word
                TranslatedMixedWordPattern
            ),

            # ====================
            # When a number is combined with words
            # the recommendation should produce a TranslatedMixedWordsPattern.
            (
                    "a1 b1",  # words
                    TranslatedMixedWordsPattern
            ),

            # ====================
            # When a number is combined with punctuation(s) or non-whitespace(s)
            # the recommendation should produce a TranslatedNonWhitespacesPattern.
            (
                "+",  # a punctuation
                TranslatedNonWhitespacesPattern
            ),
            (
                "++--==",   # punctuations
                TranslatedNonWhitespacesPattern
            ),
            (
                "\xc8",  # a non-whitespace
                TranslatedNonWhitespacesPattern
            ),
            (
                "abc\xc8",  # multi-non-whitespace
                TranslatedNonWhitespacesPattern
            ),

            # ====================
            # When a number is combined with punctuation-group
            # the recommendation should produce a TranslatedNonWhitespacesGroupPattern.
            (
                    "++ -- ** ==",  # punctuation-group
                    TranslatedNonWhitespacesGroupPattern
            ),

        ],
    )
    def test_recommend_method_case_aggregating(self, number, expected_class):
        """
        Verify that a digit type correctly recommends a subset type
        when combined with compatible number.
        """
        args = to_list(number)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.number_node.recommend(other)
        assert isinstance(recommend_instance, expected_class)
