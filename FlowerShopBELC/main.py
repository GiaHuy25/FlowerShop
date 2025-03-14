from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Router import flower, product, cart
from db.database import get_db_connection, close_db_connection
import os
from dotenv import load_dotenv

load_dotenv()  # Load biến môi trường từ .env

app = FastAPI()

# Cấu hình CORS để frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký routes

app.include_router(flower.router, prefix="/flowers", tags=["flowers"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])

@app.get("/test-db")
async def test_database_connection():
    try:
        # Kiểm tra kết nối tới database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Thực hiện truy vấn đơn giản từ bảng Hoa
        cursor.execute("SELECT HoaID, TenHoa FROM Hoa")
        rows = cursor.fetchall()

        # Chuyển đổi kết quả thành danh sách
        flowers = [{"id": row.HoaID, "name": row.TenHoa} for row in rows]

        # Đóng kết nối
        close_db_connection(conn)

        if flowers:
            return {"status": "success", "message": "Kết nối database thành công!", "data": flowers}
        else:
            return {"status": "success", "message": "Kết nối database thành công, nhưng không có dữ liệu trong bảng Hoa.", "data": []}

    except Exception as e:
        return {"status": "error", "message": f"Lỗi kết nối database: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "Welcome to Flower Shop API"}