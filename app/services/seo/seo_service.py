"""SEO optimization service for marketplace listings."""
from typing import Dict, List, Optional
import re

class SEOService:
    """Service for generating SEO-optimized content."""

    def __init__(self, keyword_weights: Optional[Dict[str, float]] = None):
        """Initialize SEO service with optional keyword weights.
        
        Args:
            keyword_weights: Dictionary mapping keywords to their importance weights
        """
        self.keyword_weights = keyword_weights or {
            "sustainable": 1.2,
            "eco-friendly": 1.1,
            "pre-owned": 1.0,
            "second-hand": 1.0,
            "vintage": 1.1,
            "authentic": 1.0
        }

    def make_title(self, original_title: str, brand: Optional[str] = None, condition: Optional[str] = None) -> str:
        """Generate SEO-optimized title.
        
        Args:
            original_title: Original product title
            brand: Brand name if available
            condition: Item condition if available
        
        Returns:
            SEO-optimized title
        """
        # Clean and normalize the title
        title = original_title.strip()
        
        # Add brand if not in title
        if brand and brand.lower() not in title.lower():
            title = f"{brand} {title}"
        
        # Add condition if provided
        if condition:
            condition_str = condition.lower()
            if condition_str not in title.lower():
                if condition_str == "new":
                    title = f"Brand New {title}"
                else:
                    title = f"Pre-Owned {title}"
        
        # Add eco-friendly emphasis if not present
        if "eco" not in title.lower() and "sustainable" not in title.lower():
            title = f"{title} | Eco-Friendly"
        
        return title

    def generate_tags(self, item_data: Dict[str, str]) -> List[str]:
        """Generate SEO-optimized tags.
        
        Args:
            item_data: Dictionary containing item details
        
        Returns:
            List of relevant tags
        """
        tags = set()
        
        # Add brand-related tags
        if brand := item_data.get("brand"):
            tags.add(brand.lower())
            tags.add(f"{brand.lower()} pre-owned")
        
        # Add condition-related tags
        if condition := item_data.get("condition"):
            tags.add(condition.lower())
            if condition.lower() != "new":
                tags.add("second-hand")
                tags.add("pre-owned")
        
        # Add sustainability tags
        tags.update([
            "sustainable",
            "eco-friendly",
            "guilt-free",
            "sustainable fashion",
            "circular economy"
        ])
        
        # Add category-specific tags if available
        if category := item_data.get("category"):
            tags.add(category.lower())
            tags.add(f"sustainable {category.lower()}")
        
        return sorted(list(tags))

    def calculate_seo_score(self, title: str, description: str, tags: List[str]) -> float:
        """Calculate SEO optimization score.
        
        Args:
            title: Listing title
            description: Listing description
            tags: List of tags
        
        Returns:
            SEO score between 0 and 1
        """
        score = 0.0
        max_score = len(self.keyword_weights)
        
        # Combine all text for keyword analysis
        full_text = f"{title.lower()} {description.lower()} {' '.join(tags).lower()}"
        
        # Check for presence of important keywords
        for keyword, weight in self.keyword_weights.items():
            if keyword in full_text:
                score += weight
        
        # Normalize score to 0-1 range
        return min(score / max_score, 1.0)

    def optimize_description(self, description: str, item_data: Dict[str, str]) -> str:
        """Generate SEO-optimized description.
        
        Args:
            description: Original description
            item_data: Dictionary containing item details
        
        Returns:
            SEO-optimized description
        """
        # Ensure description starts with a hook
        if not description.strip():
            description = "Discover sustainable fashion with this unique piece."
        
        # Add sustainability emphasis
        eco_message = (
            "\n\nBy choosing this pre-owned item, you're making a sustainable choice "
            "that helps reduce waste and supports circular fashion."
        )
        if "sustainable" not in description.lower():
            description = f"{description}{eco_message}"
        
        # Add brand emphasis if available
        if brand := item_data.get("brand"):
            brand_message = f"\n\nAuthentic {brand} quality."
            if brand.lower() not in description.lower():
                description = f"{description}{brand_message}"
        
        # Add condition details if available
        if condition := item_data.get("condition"):
            condition_message = f"\n\nItem Condition: {condition}"
            if "condition" not in description.lower():
                description = f"{description}{condition_message}"
        
        return description
