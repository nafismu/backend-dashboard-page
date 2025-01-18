import face_recognition

# Load gambar sampel
image = face_recognition.load_image_file("Elon_Musk.jpg")

# Deteksi wajah dalam gambar
face_locations = face_recognition.face_locations(image)

print(f"Jumlah wajah terdeteksi: {len(face_locations)}")
