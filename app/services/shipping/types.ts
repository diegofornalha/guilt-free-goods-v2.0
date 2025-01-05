/**
 * Address information for shipping
 */
export interface Address {
  name: string;
  street: string;
  suburb: string;
  state: string;
  postcode: string;
  country: string;
  phone?: string;
  email?: string;
}

/**
 * Item dimensions and weight
 */
export interface ItemDimensions {
  weight: number;  // in kg
  length: number;  // in cm
  width: number;   // in cm
  height: number;  // in cm
}

/**
 * Complete shipment creation request
 */
export interface ShipmentDetails {
  senderDetails: Address;
  recipientDetails: Address;
  items: Array<ItemDimensions & {
    description?: string;
    value?: number;
  }>;
}

/**
 * Shipment creation response
 */
export interface ShipmentResponse {
  id: string;
  carrier: string;
  trackingNumber?: string;
  status: string;
  labelUrl?: string;
  createdAt: string;
}

/**
 * Tracking event information
 */
export interface TrackingEvent {
  timestamp: string;
  status: string;
  location?: string;
  description: string;
}

/**
 * Complete tracking response
 */
export interface TrackingResponse {
  trackingNumber: string;
  carrier: string;
  status: string;
  estimatedDelivery?: string;
  events: TrackingEvent[];
}
