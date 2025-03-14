from fastapi import APIRouter
from Schema.cart import CartSchema
from db.database import get_db_connection, close_db_connection

router = APIRouter()

@router.get("/", response_model=list[CartSchema])
async def get_cart():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT GioHangID AS id, NguoiDungID AS user_id, SanPhamID AS product_id, SoLuong AS quantity FROM GioHang")
    rows = cursor.fetchall()
    carts = [{"id": row.id, "user_id": row.user_id, "product_id": row.product_id, "quantity": row.quantity} for row in rows]
    close_db_connection(conn)
    return carts