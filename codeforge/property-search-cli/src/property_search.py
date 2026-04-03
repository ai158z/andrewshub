import logging
from typing import Dict, List, Any, Union

# Set up logging
logger = logging.getLogger(__name__)

# Mock property database - in a real application, this would come from a database or API
_PROPERTIES = [
    {
        "id": 1,
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "90210",
        "price": 750000.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "square_feet": 1800,
        "year_built": 1995,
        "property_type": "Single Family Home",
        "listing_type": "Sale",
        "interest_rate": 4.5
    },
    {
        "id": 2,
        "address": "456 Oak Ave",
        "city": "Sometown",
        "state": "CA",
        "zip_code": "90211",
        "price": 1200000.0,
        "bedrooms": 4,
        "bathrooms": 3,
        "square_feet": 2500,
        "year_built": 2005,
        "property_type": "Townhouse",
        "listing_type": "Sale",
        "interest_rate": 4.2
    },
    {
        "id": 3,
        "address": "789 Pine Rd",
        "city": "Othertown",
        "state": "CA",
        "zip_code": "90212",
        "price": 950000.0,
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1500,
        "year_built": 1985,
        "property_type": "Condo",
        "listing_type": "Sale",
        "interest_rate": 4.8
    },
    {
        "id": 4,
        "address": "321 Elm St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "90210",
        "price": 850000.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "square_feet": 2000,
        "year_built": 2000,
        "property_type": "Single Family Home",
        "listing_type": "Sale",
        "interest_rate": 4.3
    }
]

def _get_all_properties() -> List[Dict[str, Any]]:
    """Return all properties from the mock database."""
    return _PROPERTIES

def _filter_by_price_range(properties: List[Dict[str, Any]], min_price: float, max_price: float) -> List[Dict[str, Any]]:
    """Filter properties by price range."""
    if min_price <= 0 and max_price <= 0:
        return properties
    
    filtered = []
    for property in properties:
        price = property.get('price', 0)
        if min_price > 0 and price < min_price:
            continue
        if max_price > 0 and price > max_price:
            continue
        filtered.append(property)
    return filtered

def _filter_by_bedrooms(properties: List[Dict[str, Any]], min_bedrooms: int) -> List[Dict[str, Any]]:
    """Filter properties by minimum number of bedrooms."""
    if min_bedrooms <= 0:
        return properties
    
    return [p for p in properties if p.get('bedrooms', 0) >= min_bedrooms]

def _filter_by_bathrooms(properties: List[Dict[str, Any]], min_bathrooms: int) -> List[Dict[str, Any]]:
    """Filter properties by minimum number of bathrooms."""
    if min_bathrooms <= 0:
        return properties
    
    return [p for p in properties if p.get('bathrooms', 0) >= min_bathrooms]

def _filter_by_property_type(properties: List[Dict[str, Any]], property_type: str) -> List[Dict[str, Any]]:
    """Filter properties by property type."""
    if not property_type:
        return properties
    
    return [p for p in properties if p.get('property_type', '').lower() == property_type.lower()]

def _filter_by_city(properties: List[Dict[str, Any]], city: str) -> List[Dict[str, Any]]:
    """Filter properties by city."""
    if not city:
        return properties
    
    return [p for p in properties if p.get('city', '').lower() == city.lower()]

def _filter_by_zip_code(properties: List[Dict[str, Any]], zip_code: str) -> List[Dict[str, Any]]:
    """Filter properties by zip code."""
    if not zip_code:
        return properties
    
    return [p for p in properties if p.get('zip_code', '').lower() == zip_code.lower()]

def search_properties(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Search properties based on provided filters.
    
    Args:
        filters: Dictionary containing search criteria
        
    Returns:
        List of properties matching the filters
    """
    # Start with all properties
    results = _get_all_properties()
    
    # Apply price range filter
    min_price = filters.get('min_price', 0)
    max_price = filters.get('max_price', 0)
    results = _filter_by_price_range(results, min_price, max_price)
    
    # Apply bedroom filter
    min_bedrooms = filters.get('min_bedrooms', 0)
    results = _filter_by_bedrooms(results, min_bedrooms)
    
    # Apply bathroom filter
    min_bathrooms = filters.get('min_bathrooms', 0)
    results = _filter_by_bathrooms(results, min_bathrooms)
    
    # Apply property type filter
    property_type = filters.get('property_type')
    if property_type is not None:
        results = _filter_by_property_type(results, property_type)
    
    # Apply city filter
    city = filters.get('city')
    if city is not None:
        results = _filter_by_city(results, city)
    
    # Apply zip code filter
    zip_code = filters.get('zip_code')
    if zip_code is not None:
        results = _filter_by_zip_code(results, zip_code)
    
    return results

# For testing purposes
if __name__ == "__main__":
    # Example usage
    filters = {
        'min_price': 800000,
        'max_price': 1000000,
        'min_bedrooms': 2,
        'min_bathrooms': 2,
        'property_type': 'Single Family Home',
        'city': 'Anytown',
        'zip_code': '90210'
    }
    
    filtered_properties = search_properties(filters)
    print(f"Found {len(filtered_properties)} properties matching criteria")
    for prop in filtered_properties:
        print(f"Property: {prop['address']}, Price: ${prop['price']:,.2f}")