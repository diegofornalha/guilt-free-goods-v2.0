"""Mobile-optimized content formatter for listings."""
from typing import Dict, Any, List

class MobileContentFormatter:
    """Format listing content for mobile devices."""
    
    def __init__(
        self,
        max_title_length: int = 50,
        max_description_length: int = 200,
        max_tag_count: int = 5
    ):
        """Initialize the formatter with size constraints."""
        self.max_title_length = max_title_length
        self.max_description_length = max_description_length
        self.max_tag_count = max_tag_count
    
    def format_listing_content(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format listing content for mobile display."""
        return {
            "title": self._truncate_title(listing_data["title"]),
            "description": self._truncate_description(listing_data["description"]),
            "tags": self._limit_tags(listing_data["tags"])
        }
    
    def _truncate_title(self, title: str) -> str:
        """Truncate title to fit mobile display."""
        if len(title) <= self.max_title_length:
            return title
        return title[:self.max_title_length-3] + "..."
    
    def _truncate_description(self, description: str) -> str:
        """Truncate description to fit mobile display."""
        if len(description) <= self.max_description_length:
            return description
        return description[:self.max_description_length-3] + "..."
    
    def _limit_tags(self, tags: List[str]) -> List[str]:
        """Limit number of tags for mobile display."""
        return tags[:self.max_tag_count]
