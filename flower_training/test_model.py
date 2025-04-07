import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Cấu hình toàn cục
MODEL_PATH = "E:\\Kysu\\VanDeHienDaiCNTT\\FlowerShop\\flower_training\\flower_model_improved.h5"
CLASS_NAMES = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
TARGET_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.7
ENTROPY_THRESHOLD = 0.5

def preprocess_image(image_path, target_size=TARGET_SIZE, normalize=True):
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"File không tồn tại: {image_path}")

    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh từ: {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    if normalize:
        img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)

def predict_flower(model, image_path):
    try:
        img = preprocess_image(image_path)
        predictions = model.predict(img, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Tính entropy
        entropy = -np.sum(predictions[0] * np.log(predictions[0] + 1e-10))
        flower_name = CLASS_NAMES[predicted_class]
        
        if confidence < CONFIDENCE_THRESHOLD or entropy > ENTROPY_THRESHOLD:
            return "unknown", 0.0
        return flower_name, confidence
    except Exception as e:
        raise RuntimeError(f"Lỗi khi dự đoán: {e}")

def show_result(image_path, flower_name, confidence):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Không thể đọc ảnh để hiển thị: {image_path}")
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(6, 6))
        plt.imshow(img)
        plt.title(f"Loài hoa: {flower_name} (Độ tin cậy: {confidence:.2%})", fontsize=12)
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Lỗi hiển thị ảnh: {e}")

def main():
    test_image_path = 'E:\\Kysu\\VanDeHienDaiCNTT\\Datasets\\Test\\CatTuong.jpg'
    try:
        model = load_model(MODEL_PATH)
        print("Mô hình đã được tải thành công.")
        flower_name, confidence = predict_flower(model, test_image_path)
        print(f"Dự đoán: {flower_name} với độ tin cậy {confidence:.2%}")
        show_result(test_image_path, flower_name, confidence)
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()