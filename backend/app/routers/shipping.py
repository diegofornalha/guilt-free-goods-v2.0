from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
from ..services.shipping.auspost_client import AusPostClient
from ..services.shipping.toll_client import TollClient
from pydantic import BaseModel, Field

router = APIRouter(prefix="/shipping", tags=["shipping"])

class ShipmentDetails(BaseModel):
    """Pydantic model for shipment creation request."""
    sender_details: Dict = Field(..., description="Sender's address and contact information")
    recipient_details: Dict = Field(..., description="Recipient's address and contact information")
    items: list[Dict] = Field(..., description="List of items with dimensions and weight")

def get_auspost_client() -> AusPostClient:
    """Dependency injection for AusPost client."""
    # TODO: Get credentials from environment variables
    return AusPostClient(api_key="", account_number="")

def get_toll_client() -> TollClient:
    """Dependency injection for Toll client."""
    return TollClient()

def select_carrier(items: list[Dict]) -> tuple[str, bool]:
    """Select appropriate carrier based on package dimensions.
    
    Returns:
        Tuple of (carrier_name, requires_fallback)
    """
    for item in items:
        weight = item.get("weight", 0)
        length = item.get("length", 0)
        volume = (item.get("length", 0) * item.get("width", 0) * 
                 item.get("height", 0)) / 1000000  # Convert to cubic meters
        
        # Check if any dimension exceeds Australia Post limits
        if weight > 22 or length > 105 or volume > 0.25:
            return "TOLL", True
    
    return "AUS_POST", False

@router.post("/create")
async def create_shipment(
    shipment_details: ShipmentDetails,
    auspost: AusPostClient = Depends(get_auspost_client),
    toll: TollClient = Depends(get_toll_client)
) -> Dict:
    """Create a new shipment using the most cost-effective carrier."""
    try:
        # Get dimensions of first item (assuming single-item shipments for now)
        item = shipment_details.items[0]
        weight = item.get("weight", 0)
        length = item.get("length", 0)
        width = item.get("width", 0)
        height = item.get("height", 0)
        
        # Get shipping quotes from both carriers if package is within AusPost limits
        quotes = {}
        if weight <= 22 and length <= 105 and (length * width * height / 1000000) <= 0.25:
            try:
                auspost_quote = auspost.get_shipping_price(
                    weight=weight,
                    length=length,
                    width=width,
                    height=height,
                    from_postcode=shipment_details.sender_details["postcode"],
                    to_postcode=shipment_details.recipient_details["postcode"]
                )
                quotes["AUS_POST"] = auspost_quote["total_cost"]
            except Exception as e:
                print(f"Failed to get AusPost quote: {e}")
        
        # Get Toll quote if package exceeds AusPost limits or AusPost quote failed
        if not quotes or weight > 22 or length > 105 or (length * width * height / 1000000) > 0.25:
            try:
                toll_quote = toll.get_quote(
                    weight=weight,
                    length=length,
                    width=width,
                    height=height,
                    from_postcode=shipment_details.sender_details["postcode"],
                    to_postcode=shipment_details.recipient_details["postcode"]
                )
                quotes["TOLL"] = toll_quote["total_cost"]
            except Exception as e:
                print(f"Failed to get Toll quote: {e}")
        
        if not quotes:
            raise ValueError("Failed to get quotes from any carrier")
        
        # Select the cheapest carrier
        selected_carrier = min(quotes.items(), key=lambda x: x[1])[0]
        
        # Create shipment with selected carrier
        if selected_carrier == "AUS_POST":
            response = auspost.create_shipment(shipment_details.dict())
        else:
            response = toll.create_shipment(shipment_details.dict())
        
        # Add cost information to response
        response["shipping_cost"] = quotes[selected_carrier]
        response["carrier"] = selected_carrier
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create shipment: {str(e)}")

@router.get("/track/{tracking_number}")
async def track_shipment(
    tracking_number: str,
    auspost: AusPostClient = Depends(get_auspost_client),
    toll: TollClient = Depends(get_toll_client)
) -> Dict:
    """Track a shipment. Tries both carriers if necessary."""
    # Try Australia Post first
    try:
        return auspost.track_item(tracking_number)
    except Exception:
        # If AusPost fails, try Toll
        try:
            return toll.track_shipment(tracking_number)
        except Exception:
            raise HTTPException(
                status_code=404,
                detail=f"Tracking number {tracking_number} not found with any carrier"
            )
