"""
Tests for language detection functionality in Township Connect.

These tests verify that the language detection functionality works correctly,
including detecting languages from common greetings.
"""

import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.language_utils import detect_language

@pytest.mark.parametrize("text,expected_language", [
    ("Hello", "en"),
    ("Hi there", "en"),
    ("Good morning", "en"),
    ("Molo", "xh"),
    ("Molweni", "xh"),
    ("Hallo", "af"),
    ("Goeie dag", "af"),
    ("Random text", "en"),  # Default to English
    ("", "en"),  # Empty text should default to English
    (None, "en"),  # None should default to English
])
@pytest.mark.unit
def test_detect_language(text, expected_language):
    """Test that the detect_language function correctly detects languages."""
    detected = detect_language(text)
    assert detected == expected_language, f"Expected '{expected_language}' for '{text}', got '{detected}'"

@pytest.mark.unit
def test_detect_language_case_insensitive():
    """Test that language detection is case-insensitive."""
    assert detect_language("HELLO") == "en"
    assert detect_language("mOlO") == "xh"
    assert detect_language("HALLO") == "af"