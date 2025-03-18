from pydantic import BaseModel
from typing import Optional  # Thêm import này

class FlowerSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None

    class Config:
        from_attributes = True