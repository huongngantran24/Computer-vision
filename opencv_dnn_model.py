import os
import cv2
from time import time
import mediapipe
import matplotlib.pyplot as plt

opencv_dnn_model = cv2.dnn.readNetFromCaffe(prototxt="models/deploy.prototxt",
                                            caffeModel="models/res10_300x300_ssd_iter_140000_fp16.caffemodel")

def cvDnnDetectFaces(image, opencv_dnn_model, min_confidence=0.5, display = "True"):
   image_heigth, image_width,_ = image.shape# Lấy chiều cao và chiều rộng của hình ảnh đầu vào.

   output_image = image.copy()# Tạo một bản sao của hình ảnh đầu vào để vẽ các hộp giới hạn và ghi điểm tin cậy.

   #xử lý trước hình ảnh / khung hình
   preprocessing_image = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(300, 300),
                                               mean=(104, 0, 117.0, 123.0), swapRB=False, crop=False)

    #scalefactor: quy mô
    # swapRB: hoán đổi kênh: Chuyển đổi từ định dạng BGR sang RGB bằng cách hoán đổi các kênh Xanh lam và Đỏ.
    #mean: Phép trừ trung bình được sử dụng để giúp chống lại những thay đổi về độ sáng trong hình ảnh đầu vào trong tập dữ liệu


   opencv_dnn_model.setInput(preprocessing_image) #đặt hình ảnh được xử lý trước làm đầu vào cho mạng

   start = time()# Lấy thời gian hiện tại trước khi thực hiện nhận diện khuôn mặt.
   results = opencv_dnn_model.forward()# Thực hiện nhận diện khuôn mặt trên hình ảnh.
   print(results)
   end = time()# Lấy thời gian hiện tại sau khi thực hiện nhận diện khuôn mặt.

   print(len(results))
   arr_found = []

   for face in results[0][0]:# Lặp qua từng khuôn mặt được phát hiện trong ảnh.
       face_confidence = face[2]# Lấy điểm tin cậy nhận diện khuôn mặt.

       if face_confidence > min_confidence:# Kiểm tra xem điểm tin cậy nhận diện khuôn mặt có lớn hơn ngưỡng hay không.
           bbox = face[3:]# Lấy hộp giới hạn của khuôn mặt.

           # Lấy tọa độ hộp giới hạn của mặt và chia tỷ lệ chúng theo kích thước ban đầu của ảnh
           x1 = int(bbox[0] * image_width)
           y1 = int(bbox[1] * image_heigth)
           x2 = int(bbox[2] * image_width)
           y2 = int(bbox[3] * image_heigth)

           arr = [x1, y1, x2, y2]
           arr_found.append(arr)

           # Vẽ một hộp giới hạn xung quanh một khuôn mặt trên bản sao của hình ảnh bằng cách sử dụng các tọa độ đã truy xuất.
           cv2.rectangle(output_image, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=image_width//200)

           # Vẽ một hình chữ nhật đầy gần hộp giới hạn của khuôn mặt.
           # Chúng tôi đang làm điều đó để thay đổi nền của điểm tin cậy để làm cho nó dễ dàng hiển thị.
           cv2.rectangle(output_image, pt1=(x1, y1 - image_width // 20), pt2=(x1 + image_width // 16, y1),
                         color=(0, 255, 0), thickness=-1)

           # Viết điểm tin cậy của mặt gần ô giới hạn và trên hình chữ nhật được tô màu.
           cv2.putText(output_image, text=str(round(face_confidence, 1)), org=(x1, y1 - 25),
                       fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=image_width // 700,
                       color=(255, 255, 255), thickness=image_width // 200)

       # Kiểm tra xem hình ảnh đầu vào gốc và hình ảnh đầu ra có được chỉ định để hiển thị hay không.
       if display:
           # Ghi thời gian của quá trình nhận diện khuôn mặt trên hình ảnh đầu ra.
           cv2.putText(output_image, text='Time taken: ' + str(round(end - start, 2)) + ' Seconds.', org=(10, 65),
                       fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=image_width // 700,
                       color=(0, 0, 255), thickness=image_width // 500)

           # Hiển thị hình ảnh đầu vào gốc và hình ảnh đầu ra.
           plt.figure(figsize=[15, 15])
           plt.subplot(121);
           plt.imshow(image[:, :, ::-1]);
           plt.title("Original Image");
           plt.axis('off');
           plt.subplot(122);
           plt.imshow(output_image[:, :, ::-1]);
           plt.title("Output");
           plt.axis('off');
           plt.show()

       # Nếu không thì
       else:

           # Trả lại hình ảnh đầu ra và kết quả nhận diện khuôn mặt.
           return output_image, arr_found, face_confidence



# Read a sample image and perform OpenCV dnn face detection on it.
# image = cv2.imread('media/sample3.jpg')
# cvDnnDetectFaces(image, opencv_dnn_model, display=True)

