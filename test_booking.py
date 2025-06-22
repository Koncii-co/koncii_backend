#!/usr/bin/env python3
"""
Test script for the chat endpoint (booking via root agent)
"""

import json
import requests
from typing import Dict, Any

API_BASE_URL = "http://localhost:10000"

def test_booking_via_chat(booking_type: str, details: Dict[str, Any], user_preferences: Dict[str, Any] = None):
    """Test the chat endpoint for booking requests"""
    # Format the message as a user would
    message = f"I want to book a {booking_type} with the following details:\n" \
              f"{json.dumps(details, indent=2)}\n" \
              f"User preferences: {json.dumps(user_preferences or {}, indent=2)}\n" \
              f"Please help me complete this booking with payment processing."
    payload = {"message": message}
    print(f"\n{'='*60}")
    print(f"Testing {booking_type.upper()} booking via chat endpoint")
    print(f"{'='*60}")
    print(f"Request message:\n{message}")
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Success! Status: {response.status_code}")
            print(f"Response:\n{result['response']}")
        else:
            print(f"❌ Error! Status: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Make sure the server is running on {API_BASE_URL}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    print("🚀 Travel Concierge Booking via Chat API Test")
    print("=" * 60)
    # Test 1: Flight Booking
    flight_details = {
        "airline": "Delta Airlines",
        "flight_number": "DL1234",
        "departure": "New York (JFK)",
        "arrival": "London (LHR)",
        "departure_time": "2024-02-15T08:00:00Z",
        "arrival_time": "2024-02-15T20:00:00Z",
        "seat_class": "Business",
        "price": "$1200"
    }
    flight_preferences = {
        "seat_preference": "window",
        "meal_preference": "vegetarian",
        "special_assistance": False
    }
    test_booking_via_chat("flight", flight_details, flight_preferences)
    # Test 2: Hotel Booking
    hotel_details = {
        "hotel_name": "The Ritz-Carlton",
        "location": "Downtown Manhattan",
        "check_in": "2024-02-15T15:00:00Z",
        "check_out": "2024-02-18T11:00:00Z",
        "room_type": "Deluxe Suite",
        "nights": 3,
        "price_per_night": "$350",
        "total_price": "$1050"
    }
    hotel_preferences = {
        "room_preference": "high_floor",
        "bed_type": "king",
        "smoking": False,
        "special_requests": "Late check-in"
    }
    test_booking_via_chat("hotel", hotel_details, hotel_preferences)
    # Test 3: Taxi Booking
    taxi_details = {
        "service": "Premium Taxi Service",
        "pickup_location": "JFK Airport Terminal 1",
        "dropoff_location": "The Ritz-Carlton, Manhattan",
        "pickup_time": "2024-02-15T09:00:00Z",
        "vehicle_type": "Luxury Sedan",
        "price": "$85"
    }
    taxi_preferences = {
        "vehicle_preference": "luxury",
        "driver_rating": "4.5+",
        "payment_method": "credit_card"
    }
    test_booking_via_chat("taxi", taxi_details, taxi_preferences)
    # Test 4: Activity Booking
    activity_details = {
        "activity_name": "New York City Walking Tour",
        "location": "Manhattan, NYC",
        "date": "2024-02-16T10:00:00Z",
        "duration": "4 hours",
        "price": "$95"
    }
    activity_preferences = {
        "group_size": "small",
        "language": "English",
        "accessibility": False,
        "includes": ["Guide", "Snacks", "Photos"]
    }
    test_booking_via_chat("activity", activity_details, activity_preferences)
    # Test 5: Restaurant Booking
    restaurant_details = {
        "restaurant_name": "Le Bernardin",
        "location": "Midtown Manhattan",
        "date": "2024-02-16T19:00:00Z",
        "party_size": 2,
        "price": "$200"
    }
    restaurant_preferences = {
        "cuisine": "French",
        "dietary_restrictions": ["vegetarian"],
        "seating": "window",
        "special_occasion": "anniversary"
    }
    test_booking_via_chat("restaurant", restaurant_details, restaurant_preferences)
    print(f"\n{'='*60}")
    print("🎉 All booking chat tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 