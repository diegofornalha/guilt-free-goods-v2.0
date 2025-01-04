"""Unit tests for the listing generation service."""
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any, Optional

from app.services.listing_generation.listing_generator import ListingGenerator, ListingDetails
from app.services.listing_generation.mobile_formatter import MobileContentFormatter

class MockNLPModel:
    """Mock NLP model for testing."""
    def generate_description(
        self,
        title: str,
        brand: Optional[str] = None,
        condition: Optional[str] = None,
        category: Optional[str] = None,
        original_description: str = ""
    ) -> str:
        return f"Test description for {title} ({condition})"

class MockSEOService:
    """Mock SEO service for testing."""
    def make_title(self, title: str, brand: Optional[str] = None, category: Optional[str] = None) -> str:
        if brand:
            return f"{brand} - {title}"
        return title

    def generate_tags(self, item_data: Dict[str, Any]) -> list:
        tags = ["test-tag"]
        if brand := item_data.get("brand"):
            tags.append(brand.lower())
        return tags

    def calculate_seo_score(self, title: str, description: str, tags: list) -> float:
        return 0.85

    def analyze_keyword_density(self, title: str, description: str) -> Dict[str, float]:
        return {"test": 0.5, "keyword": 0.3}

@pytest.fixture
def listing_generator():
    """Create a ListingGenerator instance with mock dependencies."""
    return ListingGenerator(
        nlp_model=MockNLPModel(),
        seo_service=MockSEOService()
    )

def test_generate_listing_details_basic(listing_generator):
    """Test basic listing generation without mobile optimization."""
    item_data = {
        "title": "Vintage Denim Jacket",
        "brand": "Levi's",
        "condition": "Used - Good",
        "category": "Clothing"
    }

    result = listing_generator.generate_listing_details(item_data, is_mobile=False)

    assert isinstance(result, ListingDetails)
    assert "Levi's - Vintage Denim Jacket" == result.title
    assert "Test description for Vintage Denim Jacket (Used - Good)" == result.description
    assert "test-tag" in result.tags
    assert "levi's" in result.tags
    assert result.seo_score == 0.85
    assert result.keyword_density == {"test": 0.5, "keyword": 0.3}
    assert result.mobile_title is None
    assert result.mobile_description is None
    assert result.mobile_tags is None

def test_generate_listing_details_mobile(listing_generator):
    """Test listing generation with mobile optimization."""
    item_data = {
        "title": "Vintage Levi's 501 Original Fit Men's Jeans - Classic American Denim",
        "brand": "Levi's",
        "condition": "Used - Excellent",
        "category": "Clothing",
        "description": "A detailed description that would be too long for mobile..."
    }

    result = listing_generator.generate_listing_details(item_data, is_mobile=True)

    assert isinstance(result, ListingDetails)
    assert result.mobile_title is not None
    assert result.mobile_description is not None
    assert result.mobile_tags is not None
    assert len(result.mobile_title) <= 80
    assert len(result.mobile_description) <= 300
    assert len(result.mobile_tags) <= 10

def test_missing_required_fields(listing_generator):
    """Test handling of missing required fields."""
    item_data = {
        "brand": "Levi's",
        "category": "Clothing"
    }

    with pytest.raises(ValueError) as exc_info:
        listing_generator.generate_listing_details(item_data)
    
    assert "Missing required fields" in str(exc_info.value)
    assert "title" in str(exc_info.value)
    assert "condition" in str(exc_info.value)

def test_empty_optional_fields(listing_generator):
    """Test handling of empty optional fields."""
    item_data = {
        "title": "Test Item",
        "condition": "New",
    }

    result = listing_generator.generate_listing_details(item_data)

    assert isinstance(result, ListingDetails)
    assert result.title == "Test Item"
    assert "Test description for Test Item (New)" == result.description
    assert isinstance(result.tags, list)
    assert result.seo_score is not None
    assert result.keyword_density is not None

def test_mobile_content_formatter():
    """Test the mobile content formatter directly."""
    formatter = MobileContentFormatter(
        max_title_length=50,
        max_description_length=200,
        max_tag_count=5
    )

    listing_data = {
        "title": "A very long title that should be truncated for mobile devices",
        "description": "A very long description " * 20,
        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    }

    result = formatter.format_listing_content(listing_data)

    assert len(result["title"]) <= 50
    assert len(result["description"]) <= 200
    assert len(result["tags"]) <= 5
    assert "..." in result["title"]
    assert isinstance(result["tags"], list)
