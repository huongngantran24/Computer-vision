from tkinter import *
root=Tk()
def retrieve_input():
    inputValue=textBox.get("1.0","end-1c")
    print(inputValue)
    #mảng chứa các hộp giới hạn tọa độ được chuẩn hóa  ([0.0, 1.0]) và độ tin cậy phát hiện của mỗi khuôn mặt trong hình ảnh.

textBox=Text(root, height=2, width=10)
textBox.pack()
buttonCommit=Button(root, height=1, width=10, text="Commit",
                    command=lambda: retrieve_input())
#command=lambda: retrieve_input() >>> just means do this when i press the button
buttonCommit.pack()

mainloop()