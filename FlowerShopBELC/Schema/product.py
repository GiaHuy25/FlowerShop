from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    image: Optional[str] = None  # Đường dẫn ảnh có thể là null

    class Config:
        from_attributes = True  # Cho phép ánh xạ từ object SQLAlchemy hoặc pyodbc
    