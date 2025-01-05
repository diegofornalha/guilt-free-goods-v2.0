from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from pydantic import BaseModel
import json
from pathlib import Path
from prisma import Prisma
from ..db import get_db

router = APIRouter(
    prefix="/api/compliance",
    tags=["compliance"],
    responses={404: {"description": "Not found"}}
)

class ComplianceCheck(BaseModel):
    item_id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None

class ComplianceResult(BaseModel):
    item_id: int
    compliance_passed: bool
    issues: List[str] = []
    restricted_categories: List[str] = []
    brand_verification_passed: Optional[bool] = None

# Load restricted items configuration
def load_restricted_items() -> Dict:
    config_path = Path(__file__).parent.parent / "config" / "restricted_items.json"
    if not config_path.exists():
        return {"categories": [], "keywords": [], "restricted_brands": []}
    
    with open(config_path, "r") as f:
        return json.load(f)

@router.get("/check/{item_id}", response_model=ComplianceResult)
async def check_item_compliance(
    item_id: int,
    db: Prisma = Depends(get_db)
) -> ComplianceResult:
    """
    Check if an item complies with marketplace guidelines by verifying:
    - It's not in restricted categories
    - It doesn't contain restricted keywords
    - Brand authenticity (if applicable)
    """
    # Get item details from database
    item = await db.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Load restricted items configuration
    restricted_config = load_restricted_items()
    
    issues = []
    restricted_categories = []
    
    # Check category restrictions
    if item.category and item.category.lower() in [c.lower() for c in restricted_config["categories"]]:
        restricted_categories.append(item.category)
        issues.append(f"Category '{item.category}' is restricted")
    
    # Check for restricted keywords in name/description
    for keyword in restricted_config["keywords"]:
        if keyword.lower() in item.name.lower():
            issues.append(f"Name contains restricted keyword: {keyword}")
        if item.description and keyword.lower() in item.description.lower():
            issues.append(f"Description contains restricted keyword: {keyword}")
    
    # Basic brand verification
    brand_verification_passed = None
    if item.brand:
        brand_verification_passed = item.brand.lower() not in [b.lower() for b in restricted_config["restricted_brands"]]
        if not brand_verification_passed:
            issues.append(f"Brand '{item.brand}' is restricted or flagged")
    
    return ComplianceResult(
        item_id=item_id,
        compliance_passed=len(issues) == 0,
        issues=issues,
        restricted_categories=restricted_categories,
        brand_verification_passed=brand_verification_passed
    )

@router.post("/validate", response_model=ComplianceResult)
async def validate_item_compliance(
    item: ComplianceCheck,
    db: Prisma = Depends(get_db)
) -> ComplianceResult:
    """
    Validate an item's compliance before it's added to the system
    """
    restricted_config = load_restricted_items()
    
    issues = []
    restricted_categories = []
    
    # Category check
    if item.category and item.category.lower() in [c.lower() for c in restricted_config["categories"]]:
        restricted_categories.append(item.category)
        issues.append(f"Category '{item.category}' is restricted")
    
    # Keyword check
    for keyword in restricted_config["keywords"]:
        if keyword.lower() in item.name.lower():
            issues.append(f"Name contains restricted keyword: {keyword}")
        if item.description and keyword.lower() in item.description.lower():
            issues.append(f"Description contains restricted keyword: {keyword}")
    
    # Brand verification
    brand_verification_passed = None
    if item.brand:
        brand_verification_passed = item.brand.lower() not in [b.lower() for b in restricted_config["restricted_brands"]]
        if not brand_verification_passed:
            issues.append(f"Brand '{item.brand}' is restricted or flagged")
    
    return ComplianceResult(
        item_id=item.item_id,
        compliance_passed=len(issues) == 0,
        issues=issues,
        restricted_categories=restricted_categories,
        brand_verification_passed=brand_verification_passed
    )
