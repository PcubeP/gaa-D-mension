"""Car models (dict-based for simplicity with SQLite)."""
from datetime import datetime
from typing import Optional


class Car:
    """Represents a car with its dimensions."""
    def __init__(self, 
                 id: int, make: str, model: str, year: int,
                 length: float, width: float, height: float, wheelbase: float,
                 side_view_url: Optional[str] = None, front_view_url: Optional[str] = None, 
                 rear_view_url: Optional[str] = None, description: Optional[str] = None):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.length = length
        self.width = width
        self.height = height
        self.wheelbase = wheelbase
        self.side_view_url = side_view_url or ""
        self.front_view_url = front_view_url or ""
        self.rear_view_url = rear_view_url or ""
        self.description = description
    
    def to_dict(self) -> dict:
        """Convert to dict for JSON response."""
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "wheelbase": self.wheelbase,
            "side_view_url": self.side_view_url,
            "front_view_url": self.front_view_url,
            "rear_view_url": self.rear_view_url,
            "description": self.description
        }


class CarComparison:
    """Represents a comparison between two cars."""
    def __init__(self, 
                 id: int, car_a_id: int, car_b_id: int,
                 thumbnail_url: Optional[str] = None, comparison_data_json: Optional[str] = None):
        self.id = id
        self.car_a_id = car_a_id
        self.car_b_id = car_b_id
        self.thumbnail_url = thumbnail_url or ""
        self.comparison_data_json = comparison_data_json
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "car_a_id": self.car_a_id,
            "car_b_id": self.car_b_id,
            "thumbnail_url": self.thumbnail_url,
            "comparison_data_json": self.comparison_data_json
        }


class CarModel:
    """Car model class for type hints and consistency (alias for Car)."""
    def __init__(self, 
                 id: int, make: str, model: str, year: int,
                 length: float, width: float, height: float, wheelbase: float,
                 side_view_url: Optional[str] = None, front_view_url: Optional[str] = None, 
                 rear_view_url: Optional[str] = None, description: Optional[str] = None):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.length = length
        self.width = width
        self.height = height
        self.wheelbase = wheelbase
        self.side_view_url = side_view_url or ""
        self.front_view_url = front_view_url or ""
        self.rear_view_url = rear_view_url or ""
        self.description = description
    
    def to_dict(self) -> dict:
        return self.to_dict()  # Reuse parent class method


class CarComparisonModel:
    """Car comparison model class (alias for CarComparison)."""
    def __init__(self, 
                 id: int, car_a_id: int, car_b_id: int,
                 thumbnail_url: Optional[str] = None, comparison_data_json: Optional[str] = None):
        self.id = id
        self.car_a_id = car_a_id
        self.car_b_id = car_b_id
        self.thumbnail_url = thumbnail_url or ""
        self.comparison_data_json = comparison_data_json
    
    def to_dict(self) -> dict:
        return self.to_dict()  # Reuse parent class method
