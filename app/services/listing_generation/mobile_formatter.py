"""Mobile content formatting service for optimizing listing content for mobile devices."""
from typing import Dict, Any, Optional, List

class MobileContentFormatter:
    """Service for optimizing content for mobile devices."""

    def __init__(
        self,
        max_title_length: int = 80,
        max_description_length: int = 300,
        max_tag_count: int = 10
    ):
        """Initialize mobile content formatter.
        
        Args:
            max_title_length: Maximum length for mobile titles
            max_description_length: Maximum length for mobile descriptions
            max_tag_count: Maximum number of tags for mobile display
        """
        self.max_title_length = max_title_length
        self.max_description_length = max_description_length
        self.max_tag_count = max_tag_count

    def format_listing_content(
        self,
        listing_data: Dict[str, Any],
        is_mobile: Optional[bool] = True
    ) -> Dict[str, Any]:
        """Format listing content for mobile display.
        
        Args:
            listing_data: Original listing data
            is_mobile: Whether to apply mobile formatting
        
        Returns:
            Dictionary with mobile-optimized content
        """
        if not is_mobile:
            return listing_data

        formatted_data = listing_data.copy()

        # Format title
        if title := formatted_data.get("title"):
            formatted_data["title"] = self._truncate_text(
                title,
                self.max_title_length
            )

        # Format description
        if description := formatted_data.get("description"):
            formatted_data["description"] = self._format_description(description)

        # Format tags
        if tags := formatted_data.get("tags"):
            formatted_data["tags"] = self._format_tags(tags)

        return formatted_data

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length with ellipsis."""
        if len(text) <= max_length:
            return text
        return f"{text[:max_length-3]}..."

    def _format_description(self, description: str) -> str:
        """Format description for mobile display.
        
        Formats the description by:
        1. Breaking into paragraphs
        2. Keeping only essential paragraphs
        3. Truncating if still too long
        4. Adding proper spacing for mobile
        """
        # Split into paragraphs
        paragraphs = [p.strip() for p in description.split("\n\n") if p.strip()]
        
        # Keep only essential paragraphs (first few)
        if len(paragraphs) > 3:
            paragraphs = paragraphs[:3]
        
        # Join with mobile-friendly spacing
        formatted_description = "\n\n".join(paragraphs)
        
        # Truncate if still too long
        return self._truncate_text(
            formatted_description,
            self.max_description_length
        )

    def _format_tags(self, tags: List[str]) -> List[str]:
        """Format tags for mobile display.
        
        Args:
            tags: List of original tags
        
        Returns:
            List of formatted tags optimized for mobile
        """
        # Sort tags by importance (shorter tags first for mobile)
        sorted_tags = sorted(tags, key=len)
        
        # Keep only the most important tags
        return sorted_tags[:self.max_tag_count]

    def get_mobile_config(self) -> Dict[str, Any]:
        """Get current mobile formatting configuration.
        
        Returns:
            Dictionary containing current mobile formatting settings
        """
        return {
            "max_title_length": self.max_title_length,
            "max_description_length": self.max_description_length,
            "max_tag_count": self.max_tag_count
        }
