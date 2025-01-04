"""
ListingGenerator service for creating optimized listing content.

This module provides the core functionality for generating SEO-optimized titles,
descriptions, and tags for marketplace listings.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from .mobile_formatter import MobileContentFormatter

@dataclass
class ListingDetails:
    """Data class for storing generated listing details."""
    title: str
    description: str
    tags: List[str]
    seo_score: Optional[float] = None
    keyword_density: Optional[Dict[str, float]] = None
    mobile_title: Optional[str] = None
    mobile_description: Optional[str] = None
    mobile_tags: Optional[List[str]] = None

class ListingGenerator:
    """Service for generating optimized listing content."""

    def __init__(self, nlp_model, seo_service):
        """Initialize the ListingGenerator with required services.

        Args:
            nlp_model: Natural Language Processing model for text generation
            seo_service: Service for SEO optimization and analysis
        """
        self.nlp_model = nlp_model
        self.seo_service = seo_service

    def generate_listing_details(
        self,
        item_data: Dict,
        is_mobile: bool = False
    ) -> ListingDetails:
        """Generate optimized listing details from item data.

        Args:
            item_data: Dictionary containing item information including:
                - title: Original item title
                - brand: Brand name
                - condition: Item condition
                - category: Item category
                - description: Original description (optional)
            is_mobile: Whether to optimize content for mobile display

        Returns:
            ListingDetails object containing optimized content

        Raises:
            ValueError: If required item_data fields are missing
        """
        self._validate_item_data(item_data)
        
        # Generate optimized title
        generated_title = self.seo_service.make_title(
            title=item_data["title"],
            brand=item_data.get("brand"),
            category=item_data.get("category")
        )

        # Generate optimized description
        generated_description = self.nlp_model.generate_description(
            title=item_data["title"],
            brand=item_data.get("brand"),
            condition=item_data["condition"],
            category=item_data.get("category"),
            original_description=item_data.get("description", "")
        )

        # Generate relevant tags
        tags = self.seo_service.generate_tags(item_data)

        # Calculate SEO metrics
        seo_score = self.seo_service.calculate_seo_score(
            title=generated_title,
            description=generated_description,
            tags=tags
        )
        
        keyword_density = self.seo_service.analyze_keyword_density(
            title=generated_title,
            description=generated_description
        )

        # Create mobile-optimized content if requested
        mobile_formatter = MobileContentFormatter()
        mobile_content = mobile_formatter.format_listing_content({
            "title": generated_title,
            "description": generated_description,
            "tags": tags
        }) if is_mobile else {}

        return ListingDetails(
            title=generated_title,
            description=generated_description,
            tags=tags,
            seo_score=seo_score,
            keyword_density=keyword_density,
            mobile_title=mobile_content.get("title"),
            mobile_description=mobile_content.get("description"),
            mobile_tags=mobile_content.get("tags")
        )

    def _validate_item_data(self, item_data: Dict) -> None:
        """Validate required fields in item_data.

        Args:
            item_data: Dictionary containing item information

        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["title", "condition"]
        missing_fields = [field for field in required_fields if field not in item_data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
