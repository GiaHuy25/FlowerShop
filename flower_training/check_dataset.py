import os

data_dir = 'E:\\Kysu\\VanDeHienDaiCNTT\\Datasets\\flowers'
classes = os.listdir(data_dir)
for class_name in classes:
    num_images = len(os.listdir(os.path.join(data_dir, class_name)))
    print(f"{class_name}: {num_images} ảnh")