import pytest
from recherche import recherche

def test_recherche_valid_conditions():
    result = recherche(["BoolItem"], ["TypeMono"], Grid=True)
    assert result == 0, "Expected result to be 0 for valid conditions"

def test_recherche_invalid_conditions():
    result = recherche(["TypeDual"], ["TypeMono"], Grid=False)
    assert result == 1, "Expected result to be 1 for invalid conditions"
