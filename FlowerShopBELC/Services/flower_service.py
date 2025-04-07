# service/flower_service.py
from db.database import get_db_connection, close_db_connection

def get_flower_by_name(flower_name: str):
    """
    Truy vấn HoaID từ tên hoa trong cơ sở dữ liệu.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT HoaID FROM Hoa WHERE TenHoa = ?", (flower_name))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        close_db_connection(conn)

def get_products_by_flower_id(hoa_id: int):
    """
    Truy vấn danh sách sản phẩm dựa trên HoaID (giả định bảng Products).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if hoa_id is None:
        return []
    else :
        try:
            cursor.execute("SELECT * FROM SanPham WHERE HoaID = ?", (hoa_id))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            close_db_connection(conn)

def get_flower_details(flower_name: str):
    """
    Lấy thông tin chi tiết của hoa (description, image_path) từ cơ sở dữ liệu.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MoTa AS description, AnhMacDinh AS image_path FROM Hoa WHERE TenHoa = ?", (flower_name,))
        row = cursor.fetchone()
        image_path = row[1] if row else None
        image_url = f"/images/{image_path}" if image_path else None
        return {
            "description": row[0] if row else "Không có mô tả",
            "image_path": image_url
        }
    finally:
        close_db_connection(conn)