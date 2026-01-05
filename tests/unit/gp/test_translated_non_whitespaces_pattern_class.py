"""
Unit tests for the `textfsmgen.gp.TranslatedNonWhitespacesPattern` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/gp/test_translated_non_whitespaces_pattern_class.py
    or
    $ python -m pytest tests/unit/gp/test_translated_non_whitespaces_pattern_class.py
"""

import pytest

from textfsmgen.gp import (
TranslatedPattern,
# TranslatedDigitPattern,
# TranslatedDigitsPattern,
# TranslatedNumberPattern,
# TranslatedMixedNumberPattern,
# TranslatedLetterPattern,
# TranslatedLettersPattern,
# TranslatedAlphabetNumericPattern,
# TranslatedPunctPattern,
# TranslatedPunctsPattern,
# TranslatedPunctsGroupPattern,
# TranslatedGraphPattern,
# TranslatedWordPattern,
# TranslatedWordsPattern,
# TranslatedMixedWordPattern,
# TranslatedMixedWordsPattern,
# TranslatedNonWhitespacePattern,
TranslatedNonWhitespacesPattern,
TranslatedNonWhitespacesGroupPattern
)

to_list = lambda arg: arg if isinstance(arg, (list, tuple)) else [arg]


class TestTranslatedNonWhitespacesPatternClass:
    """Test suite for TranslatedNonWhitespacesPattern class."""

    def setup_method(self):
        """Create a baseline TranslatedNonWhitespacesPattern instance for reuse."""
        self.non_whitespaces_node = TranslatedNonWhitespacesPattern("abc\xc8")

    @pytest.mark.parametrize(
        "other",
        [
            "abc\xc8",          # non-whitespaces are a subset of non-whitespaces
            "abc\xc8 xyz",      # non-whitespaces are a subset of non-whitespace group
        ],
    )
    def test_is_subset_of(self, other):
        """
        Verify that non-whitespaces data is a subset of (non-whitespaces(-group))
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.non_whitespaces_node.is_subset_of(other_instance) is True

    @pytest.mark.parametrize(
        "other",
        [
            "abc 123",          # non-whitespaces are not a subset of words
            "a.1 b.2",          # non-whitespaces are not a subset of mixed-words
            "-- ++ ==",         # non-whitespaces are not a subset of punct-group
        ],
    )
    def test_is_not_subset_of(self, other):
        """
        Verify that non-whitespaces data is not a subset of (puncts-group, words,
        mixed-words, non-whitespaces-group)
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.non_whitespaces_node.is_subset_of(other_instance) is False

    @pytest.mark.parametrize(
        "other",
        [
            "a",                # non-whitespaces are a superset of letter
            "abc",              # non-whitespaces are a superset of letters
            "1",                # non-whitespaces are a superset of digit
            "123",              # non-whitespaces are a superset of digits
            "1.1",              # non-whitespaces are a superset of number
            "-1,1",             # non-whitespaces are a superset of mixed-number
            ["a", "1"],         # non-whitespaces are a superset of alpha-num
            ["a", "1", "#"],    # non-whitespaces are a superset of graph
            "-",                # non-whitespaces are a superset of punct
            "---++==",          # non-whitespaces are a superset of puncts
            "abc123",           # non-whitespaces are a superset of word
            "abc.123",          # non-whitespaces are a superset of mixed-word
            "\xc8",             # non-whitespaces are a superset of non-whitespace
        ],
    )
    def test_is_superset_of(self, other):
        """
        Verify that non-whitespaces data is a superset of (letter(s)).
        """
        args = to_list(other)
        other_instance = TranslatedPattern.do_factory_create(*args)
        assert self.non_whitespaces_node.is_superset_of(other_instance) is True

    @pytest.mark.parametrize(
        "data, expected_class",
        [
            (
                "abc\xc8",                      # non-whitespaces
                TranslatedNonWhitespacesPattern # (non-whitespaces, non-whitespaces) => non-whitespaces
            ),
            (
                "abc\xc8 xyz",                          # non-whitespace-group
                TranslatedNonWhitespacesGroupPattern    # (non-whitespaces, non-whitespace-group) => non-whitespace-group
            ),
        ],
    )
    def test_recommend_method_case_subset(self, data, expected_class):
        """
        Verify that non-whitespaces type correctly recommends a subset type
        when combined with compatible data.
        """
        args = to_list(data)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.non_whitespaces_node.recommend(other)
        assert isinstance(recommend_instance, expected_class) is True

    @pytest.mark.parametrize(
        "data, expected_class",
        [
            (
                "a",                            # letter
                TranslatedNonWhitespacesPattern # (non-whitespaces, letter) => non-whitespaces
            ),
            (
                "abc",                          # letters
                TranslatedNonWhitespacesPattern # (non-whitespaces, letters) => non-whitespaces
            ),
            (
                "1",                            # digit
                TranslatedNonWhitespacesPattern # (non-whitespaces, digit) => non-whitespaces
            ),
            (
                "123",                          # digits
                TranslatedNonWhitespacesPattern # (non-whitespaces, digits) => non-whitespaces
            ),
            (
                "1.1",                          # number
                TranslatedNonWhitespacesPattern # (non-whitespaces, number) => non-whitespaces
            ),
            (
                "-1.1",                         # mixed-number
                TranslatedNonWhitespacesPattern # (non-whitespaces, mixed-number) => non-whitespaces
            ),
            (
                ["a", "1"],                     # alpha-num
                TranslatedNonWhitespacesPattern # (non-whitespaces, alpha-num) => non-whitespaces
            ),
            (
                ["a", "1", "#"],                # graph
                TranslatedNonWhitespacesPattern # (non-whitespaces, graph) => non-whitespaces
            ),
            (
                "-",                            # punct
                TranslatedNonWhitespacesPattern # (non-whitespaces, punct) => non-whitespaces
            ),
            (
                "--++==",                       # puncts
                TranslatedNonWhitespacesPattern # (non-whitespaces, puncts) => non-whitespaces
            ),
            (
                "abc123",                       # word
                TranslatedNonWhitespacesPattern # (non-whitespaces, word) => non-whitespaces
            ),
            (
                "abc.123",                      # mixed-word
                TranslatedNonWhitespacesPattern # (non-whitespaces, mixed-word) => non-whitespaces
            ),
            (
                "\xc8",  # word
                TranslatedNonWhitespacesPattern # (non-whitespaces, non-whitespace) => non-whitespaces
            ),
        ],
    )
    def test_recommend_method_case_superset(self, data, expected_class):
        """
        Verify that non-whitespaces type correctly recommends a superset type
        when combined with compatible data.
        """
        args = to_list(data)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.non_whitespaces_node.recommend(other)
        assert isinstance(recommend_instance, expected_class) is True

    @pytest.mark.parametrize(
        "data, expected_class",
        [
            (
                "a1 b1",                        # words
                TranslatedNonWhitespacesGroupPattern # (non-whitespaces, words) => non-whitespaces-group
            ),
            (
                "a.1 b.1",                      # mixed-words
                TranslatedNonWhitespacesGroupPattern # (non-whitespaces, mixed-words) => non-whitespaces-group
            ),
            (
                "-- ++ ==",                             # punct-group
                TranslatedNonWhitespacesGroupPattern    # (non-whitespaces, punct-group) => non-whitespaces-group
            ),
        ],
    )
    def test_recommend_method_case_aggregating(self, data, expected_class):
        """
        Verify that non-whitespaces type correctly recommends a subset type
        when combined with compatible data.
        """
        args = to_list(data)
        other = TranslatedPattern.do_factory_create(*args)
        recommend_instance = self.non_whitespaces_node.recommend(other)
        assert isinstance(recommend_instance, expected_class)
