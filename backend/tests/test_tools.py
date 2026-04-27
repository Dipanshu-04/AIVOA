import pytest
from app.agents.tools import search_hcp, suggest_follow_up, add_materials_or_samples

def test_search_hcp_returns_string():
    """Test that search_hcp tool executes without crashing and returns a formatted string."""
    # This is a lightweight test. In a real environment, you'd mock the database session.
    # The tool returns JSON stringified results or a message if none found.
    try:
        result = search_hcp("NonExistentDoctor")
        assert isinstance(result, str)
        assert "No HCPs found" in result or "Search results:" in result
    except Exception as e:
        pytest.fail(f"Tool failed with exception: {e}")

def test_suggest_follow_up_format():
    """Test follow up tool string output format."""
    result = suggest_follow_up("mock-id-123", "Send email next week", "2026-05-01")
    assert isinstance(result, str)
    assert "Successfully scheduled" in result
    assert "Send email next week" in result

def test_add_materials_or_samples():
    """Test sample addition logic output format."""
    result = add_materials_or_samples(
        interaction_id="mock-id-123", 
        materials=["Product Brochure"], 
        samples=[{"name": "DrugA", "quantity": 2}]
    )
    assert isinstance(result, str)
    assert "Added materials: Product Brochure" in result
    assert "Added samples: DrugA (2)" in result
