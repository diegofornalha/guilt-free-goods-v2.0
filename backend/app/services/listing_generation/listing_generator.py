"""Listing generation service."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from .mobile_formatter import MobileContentFormatter

@dataclass
class ListingDetails:
    """Details for generating a listing."""
    title: str
    description: str
    tags: List[str]
    seo_score: float
    keyword_density: Dict[str, float]
    mobile_title: Optional[str] = None
    mobile_description: Optional[str] = None
    mobile_tags: Optional[List[str]] = None

class ListingGenerator:
    """Service for generating listings."""
    def __init__(self, nlp_model, seo_service):
        """Initialize the listing generator."""
        self.nlp_model = nlp_model
        self.seo_service = seo_service
        self.mobile_formatter = MobileContentFormatter()

    def generate_listing_details(self, item_data: Dict[str, Any], is_mobile: bool = False) -> ListingDetails:
        """Generate listing details from item data."""
        if "title" not in item_data or "condition" not in item_data:
            raise ValueError("Missing required fields: title and condition are required")

        title = self.seo_service.make_title(
            item_data["title"],
            brand=item_data.get("brand"),
            category=item_data.get("category")
        )

        description = self.nlp_model.generate_description(
            item_data["title"],
            brand=item_data.get("brand"),
            condition=item_data.get("condition"),
            category=item_data.get("category")
        )

        tags = self.seo_service.generate_tags(item_data)
        seo_score = self.seo_service.calculate_seo_score(title, description, tags)
        keyword_density = self.seo_service.analyze_keyword_density(title, description)

        mobile_content = None
        if is_mobile:
            mobile_content = self.mobile_formatter.format_listing_content({
                "title": title,
                "description": description,
                "tags": tags
            })

        return ListingDetails(
            title=title,
            description=description,
            tags=tags,
            seo_score=seo_score,
            keyword_density=keyword_density,
            mobile_title=mobile_content["title"] if mobile_content else None,
            mobile_description=mobile_content["description"] if mobile_content else None,
            mobile_tags=mobile_content["tags"] if mobile_content else None
        )
