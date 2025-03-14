from fastapi import APIRouter
from Schema.product import ProductSchema
from db.database import get_db_connection, close_db_connection

router = APIRouter()

@router.get("/", response_model=list[ProductSchema])
async def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SanPhamID AS id, TenSanPham AS name, Gia AS price, AnhURL AS image FROM SanPham")
    rows = cursor.fetchall()
    products = [{"id": row.id, "name": row.name, "price": float(row.price), "image": row.image} for row in rows]
    close_db_connection(conn)
    return products