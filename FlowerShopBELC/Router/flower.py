# Router/flower.py
from fastapi import APIRouter, UploadFile, File,HTTPException
from typing import List, Dict
import tensorflow as tf
import cv2
import numpy as np
from Schema.flower import FlowerSchema
from dotenv import load_dotenv
import os
from db.database import get_db_connection, close_db_connection
from Services.flower_service import get_flower_by_name, get_products_by_flower_id, get_flower_details 

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH")

router = APIRouter()

# Load mô hình nhận diện hoa
model = tf.keras.models.load_model(MODEL_PATH) 
CLASS_NAMES = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
CONFIDENCE_THRESHOLD = 0.7
ENTROPY_THRESHOLD = 0.5

def preprocess_image(img: np.ndarray, target_size=(224, 224), normalize=True) -> np.ndarray:
    if img is None:
        raise ValueError("Ảnh đầu vào không hợp lệ")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    if normalize:
        img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)

# Endpoint: Dự đoán loài hoa từ ảnh
@router.post("/predict", response_model=Dict)
async def predict_flower(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparray = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Không thể giải mã ảnh từ dữ liệu tải lên")

        # Tiền xử lý ảnh
        img_processed = preprocess_image(img)

        # Dự đoán
        predictions = model.predict(img_processed, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])

        # Tính entropy để kiểm tra độ chắc chắn
        entropy = -np.sum(predictions[0] * np.log(predictions[0] + 1e-10))
        
        # Kiểm tra độ tin cậy và entropy
        if confidence < CONFIDENCE_THRESHOLD or entropy > ENTROPY_THRESHOLD:
            raise HTTPException(status_code=400, detail="Không thể nhận diện loài hoa / Vật thể từ ảnh này")

        flower_name = CLASS_NAMES[predicted_class]

        # Lấy thông tin chi tiết và sản phẩm
        flower_details = get_flower_details(flower_name)
        hoa_id = get_flower_by_name(flower_name)
        products = get_products_by_flower_id(hoa_id) if hoa_id else []

        response = {
            "flower_name": flower_name,
            "confidence": confidence,  # Thêm độ tin cậy vào response
            "description": flower_details["description"],
            "image_path": flower_details["image_path"],
            "products": products
        }
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")

@router.get("/", response_model=List[FlowerSchema])
async def get_flowers():
    """
    Lấy danh sách tất cả các loài hoa từ cơ sở dữ liệu, bao gồm URL hình ảnh mặc định.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT HoaID AS id, TenHoa AS name, MoTa AS description, AnhMacDinh AS image_path FROM Hoa")
        rows = cursor.fetchall()
        flowers = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "image_path": f"/images/{row[3]}" if row[3] else None
            }
            for row in rows
        ]
        return flowers
    finally:
        close_db_connection(conn)

@router.get("/health")
async def health_check():
    """
    Kiểm tra trạng thái của microservice.
    """
    return {"status": "healthy"}