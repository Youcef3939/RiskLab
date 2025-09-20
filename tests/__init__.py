
"""
tests package for RiskLab.

this file marks the 'tests' directory as a package
you can also put shared fixtures or setup code here if needed.
"""

import pytest
import sys
sys.path.append("../plugins") 
@pytest.fixture
def sample_text():
    """example fixture for all tests"""
    return "this is a shared test fixture"