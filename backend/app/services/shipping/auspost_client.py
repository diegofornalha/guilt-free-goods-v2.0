from typing import Dict, Optional, List
import requests
from datetime import datetime

class AusPostClient:
    """Australia Post API client for domestic shipping integration."""
    
    BASE_URL = "https://digitalapi.auspost.com.au/shipping/v1"
    
    def __init__(self, api_key: str, account_number: str):
        """Initialize the Australia Post client.
        
        Args:
            api_key: Australia Post API key
            account_number: Australia Post account number
        """
        self.api_key = api_key
        self.account_number = account_number
        self.headers = {
            "Auth-Key": api_key,
            "Account-Number": account_number,
            "Content-Type": "application/json"
        }
    
    def get_account_details(self) -> Dict:
        """Retrieve information about the account and available postage products."""
        url = f"{self.BASE_URL}/accounts/{self.account_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_shipping_price(self, weight: float, length: int, width: int, height: int,
                          from_postcode: str, to_postcode: str) -> Dict:
        """Get shipping prices for a domestic parcel.
        
        Args:
            weight: Weight in kilograms (max 22kg)
            length: Length in centimeters (max 105cm)
            width: Width in centimeters
            height: Height in centimeters
            from_postcode: Sender postcode
            to_postcode: Recipient postcode
            
        Returns:
            Dict containing available shipping options and prices
        """
        url = f"{self.BASE_URL}/prices/items"
        payload = {
            "from_postcode": from_postcode,
            "to_postcode": to_postcode,
            "length": length,
            "width": width,
            "height": height,
            "weight": weight
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def create_shipment(self, shipment_details: Dict) -> Dict:
        """Create a new shipment with Australia Post.
        
        Args:
            shipment_details: Dictionary containing:
                - sender_details: Dict with name, address, etc.
                - recipient_details: Dict with name, address, etc.
                - items: List of items with dimensions and weight
                
        Returns:
            Dict containing shipment information including shipment ID
        """
        url = f"{self.BASE_URL}/shipments"
        
        # Validate package dimensions against Australia Post limits
        for item in shipment_details.get("items", []):
            weight = item.get("weight", 0)
            length = item.get("length", 0)
            volume = (item.get("length", 0) * item.get("width", 0) * 
                     item.get("height", 0)) / 1000000  # Convert to cubic meters
            
            if weight > 22:
                raise ValueError(f"Weight {weight}kg exceeds maximum 22kg limit")
            if length > 105:
                raise ValueError(f"Length {length}cm exceeds maximum 105cm limit")
            if volume > 0.25:
                raise ValueError(f"Volume {volume}m³ exceeds maximum 0.25m³ limit")
        
        response = requests.post(url, headers=self.headers, json=shipment_details)
        response.raise_for_status()
        return response.json()
    
    def create_label(self, shipment_id: str) -> bytes:
        """Generate a shipping label for a shipment.
        
        Args:
            shipment_id: ID of the shipment to generate label for
            
        Returns:
            PDF bytes containing the shipping label
        """
        url = f"{self.BASE_URL}/labels"
        payload = {
            "shipments": [{
                "shipment_id": shipment_id,
                "layout_type": "A4",
                "label_format": "PDF"
            }]
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.content
    
    def track_item(self, tracking_number: str) -> Dict:
        """Track a shipment using its tracking number.
        
        Args:
            tracking_number: Australia Post tracking number
            
        Returns:
            Dict containing tracking events and current status
        """
        url = f"{self.BASE_URL}/track"
        params = {"tracking_numbers": tracking_number}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
