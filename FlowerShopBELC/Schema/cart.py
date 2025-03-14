from pydantic import BaseModel

class CartSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True  # Cho phép ánh xạ từ object SQLAlchemy hoặc pyodbc