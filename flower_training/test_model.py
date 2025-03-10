import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đường dẫn tới file mô hình
MODEL_PATH = "E:\\Kysu\\VanDeHienDaiCNTT\\FlowerShop\\flower_training\\flower_model.h5"  

# Danh sách các loài hoa
CLASS_NAMES = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

# Hàm tiền xử lý ảnh
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Không thể đọc ảnh từ đường dẫn: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Hàm dự đoán loài hoa
def predict_flower(model, image_path):
    img = preprocess_image(image_path)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])
    flower_name = CLASS_NAMES[predicted_class]
    confidence = predictions[0][predicted_class]
    return flower_name, confidence

# Hàm hiển thị ảnh và kết quả
def show_result(image_path, flower_name, confidence):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.title(f"Loài hoa: {flower_name} (Độ tin cậy: {confidence:.2%})")
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    # Đường dẫn tới ảnh test
    TEST_IMAGE_PATH = 'E:\\Kysu\\VanDeHienDaiCNTT\\Datasets\\Test\\Huongduong.jpg'
    
    # Load mô hình
    model = load_model(MODEL_PATH)
    print("Mô hình đã được tải thành công.")

    # Dự đoán
    flower_name, confidence = predict_flower(model, TEST_IMAGE_PATH)
    
    # Hiển thị kết quả
    print(f"Dự đoán: {flower_name} với độ tin cậy {confidence:.2%}")
    show_result(TEST_IMAGE_PATH, flower_name, confidence)