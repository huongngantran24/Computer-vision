import cv2
from PIL import Image
from PIL import ImageTk
import tkinter
from tkinter.filedialog import askopenfilename

from opencv_dnn_model import cvDnnDetectFaces

opencv_dnn_model = cv2.dnn.readNetFromCaffe(prototxt="models/deploy.prototxt",
                                            caffeModel="models/res10_300x300_ssd_iter_140000_fp16.caffemodel")

class videoStream:
    panel = None
    ventana = None
    camera = None
    buttonFrame = None
    onButton = None
    label = None
    onButton3 = None
    offButton = None
    inputtxt = None
    selectButton = None
    Mode = False
    Image = False
    collectionFrame = None
    InfoFrame = None
    CollectionItem = []
    CollectionIndex = []

#__init__ là hàm dựng
#Khi một thực thể (instance) của một class được tạo ra thì hàm này sẽ được thực thi đầu tiên và một cách tự động self
    def __init__(self):
        self.ventana = tkinter.Tk()
        self.ventana.title('Face Detect')
        self.ventana.geometry("1000x600")
        # init panel
        self.panel = tkinter.Label(self.ventana)
        self.panel.place(x=53, y=111)
        # init camera
        self.camera = cv2.VideoCapture(0)
        self.AddLayout()
        self.ventana.mainloop()

    def onMode(self):
        self.Mode = True
        self.Camera()

    def offMode(self):
        self.Mode = False
        self.Camera()

    def AddLayout(self):
        self.buttonFrame = tkinter.Frame(self.ventana)
        self.collectionFrame = tkinter.Frame(self.ventana)
        self.InfoFrame = tkinter.Frame(self.ventana)
        self.collectionFrame.place(x=635,y=111)
        self.InfoFrame.place(x=635,y=323)
        self.onButton3 = tkinter.Button(self.collectionFrame, text="Onsas", background="#FF9494", fg="#FFFFFF", padx=10,
                                        pady=5,
                                        borderwidth=0, command=self.onMode)

        self.onButton = tkinter.Button(self.buttonFrame, text="On", background="#FF9494", fg="#FFFFFF", padx=10, pady=5, borderwidth=0, command=self.onMode)
        self.offButton = tkinter.Button(self.buttonFrame, text="Off", background="#969696", fg="#FFFFFF", padx=10, pady=5, borderwidth=0, command=self.offMode)
        self.selectButton = tkinter.Button(self.buttonFrame, text="Image From System", background="#FFFFFF", fg="#FF9494", padx=15, pady=5, borderwidth=0, command=self.SelectImage)
        self.onButton.grid(row=0,column=0)
        # self.label.grid(row=0, column=0)
        self.onButton3.grid(row=0, column=0)
        self.offButton.grid(row=0,column=1)
        self.selectButton.grid(row=0,column=2)
        self.buttonFrame.place(x=345, y= 23)

    def AddCollection(self, collections):
        i = 0
        array = []
        arrayItem = []
        for collection in collections:
            collection = cv2.cvtColor(collection, cv2.COLOR_BGR2RGB)
            collection = cv2.resize(collection, (88, 102))
            collection = Image.fromarray(collection)
            collection = ImageTk.PhotoImage(collection)
            hold = tkinter.Label(self.collectionFrame)
            hold.grid(row=0, column=i)
            hold.configure(image=collection)
            hold.image = collection
            arrayItem.append(hold)
            array.append(i)
            i += 1
        if len(self.CollectionIndex) != 0:
            if len(array) != 0:
                if len(self.CollectionIndex) >= len(array):
                    diff = list(set(self.CollectionIndex) - set(array))
                    if len(diff) != 0:
                        for index in diff:
                            self.CollectionIndex.pop(index)
                            self.CollectionItem[index].destroy()
                            self.CollectionItem.pop(index)
                            self.CollectionItem = arrayItem
                if len(array) > len(self.CollectionIndex):
                    self.CollectionIndex = array
                    self.CollectionItem = arrayItem
            else:
                for index in self.CollectionIndex:
                    self.CollectionItem[index].destroy()
                self.CollectionItem = []
                self.CollectionIndex = []
        else:
            self.CollectionIndex = array
            self.CollectionItem = arrayItem

    def SelectImage(self):
        FilePath = askopenfilename()
        self.offMode()
        img = cv2.imread(FilePath)
        frame, result, accuracy = cvDnnDetectFaces(img, opencv_dnn_model, min_confidence=0.5, display=False)
        face_confidence = self.getAccuracy(accuracy)
        print(accuracy)
        collections = self.getImage(img, result)
        self.AddCollection(collections)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (538, 424))
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.panel.configure(image=frame)
        self.panel.image = frame
        self.Image = True

        return accuracy

    def getImage(self, image, results):
        collections = []
        for i in results:
            x1 = i[0]
            y1 = i[1]
            x2 = i[2]
            y2 = i[3]
            img = image[y1:y2, x1:x2]
            collections.append(img)
        return collections

    def getAccuracy(self, accuracys):
        return accuracys

    def addAccuracy(self, face_confidence):
        for face in face_confidence:
            acc = tkinter.Label(self.InfoFrame)
            acc.grid(row=0, column=0)
            acc = face



    def Camera(self):
        if self.Mode:
            _, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            original = frame
            frame, result, accuracy = cvDnnDetectFaces(frame, opencv_dnn_model, min_confidence=0.5, display=False)

            face_confidence = self.getAccuracy(accuracy)
            print(face_confidence)
            collections = self.getImage(original, result)
            self.AddCollection(collections)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (538, 424))
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.panel.configure(image=frame)
            self.panel.image = frame
            self.Image = False
            self.panel.after(1, self.Camera)
            return accuracy
        else:
            if self.Image != True:
                self.panel.configure(bg='#000000')
                self.panel.image = None

if __name__ == '__main__':
    objVideo = videoStream()