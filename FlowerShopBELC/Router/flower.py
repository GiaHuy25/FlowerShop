from fastapi import APIRouter, UploadFile, File
from Schema.flower import FlowerSchema
from Schema.product import ProductSchema
import tensorflow as tf  # Thay đổi import thành cách chuẩn
import cv2
import numpy as np
import os
from dotenv import load_dotenv
from db import get_db_connection, close_db_connection

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH")

router = APIRouter()

# Load mô hình khi khởi động
model = tf.keras.models.load_model(MODEL_PATH) 
CLASS_NAMES = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

def get_flower_by_name(flower_name):
    """Lấy HoaID dựa trên tên hoa"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT HoaID FROM Hoa WHERE TenHoa = ?", (flower_name,))
    row = cursor.fetchone()
    close_db_connection(conn)
    return row.HoaID if row else None

def get_products_by_flower_id(hoa_id):
    """Lấy danh sách sản phẩm dựa trên HoaID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SanPhamID AS id, TenSanPham AS name, Gia AS price, AnhURL AS image FROM SanPham WHERE HoaID = ?", (hoa_id,))
    rows = cursor.fetchall()
    products = [{"id": row.id, "name": row.name, "price": float(row.price), "image": row.image} for row in rows]
    close_db_connection(conn)
    return products

@router.get("/", response_model=list[FlowerSchema])
async def get_flowers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT HoaID AS id, TenHoa AS name, MoTa AS description FROM Hoa")
    rows = cursor.fetchall()
    flowers = [{"id": row.id, "name": row.name, "description": row.description} for row in rows]
    close_db_connection(conn)
    return flowers

@router.post("/predict", response_model=dict)
async def predict_flower(file: UploadFile = File(...)):
    contents = await file.read()
    nparray = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Không thể giải mã ảnh từ dữ liệu tải lên")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])
    flower_name = CLASS_NAMES[predicted_class]

    hoa_id = get_flower_by_name(flower_name)
    products = get_products_by_flower_id(hoa_id) if hoa_id else []

    return {"flower_name": flower_name, "products": products}