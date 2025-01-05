import { ShipmentDetails, ShipmentResponse, TrackingResponse } from './types';

/**
 * Create a new shipment using the appropriate carrier based on package dimensions.
 * 
 * @param shipmentDetails Shipment creation details including items and addresses
 * @returns Promise resolving to shipment creation response
 * @throws Error if shipment creation fails
 */
export async function createShipment(shipmentDetails: ShipmentDetails): Promise<ShipmentResponse> {
  try {
    const response = await fetch('/api/shipping/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(shipmentDetails),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create shipment');
    }

    return response.json();
  } catch (error) {
    console.error('Error creating shipment:', error);
    throw error;
  }
}

/**
 * Track a shipment using its tracking number.
 * 
 * @param trackingNumber Shipment tracking number
 * @returns Promise resolving to tracking information
 * @throws Error if tracking lookup fails
 */
export async function trackShipment(trackingNumber: string): Promise<TrackingResponse> {
  try {
    const response = await fetch(`/api/shipping/track/${trackingNumber}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to track shipment');
    }

    return response.json();
  } catch (error) {
    console.error('Error tracking shipment:', error);
    throw error;
  }
}
