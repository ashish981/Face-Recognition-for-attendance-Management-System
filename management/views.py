from django.shortcuts import render, redirect
from .forms import EmployeeForm, AttendanceForm
from .models import Employee, Attendance
from django.contrib.auth.decorators import login_required
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import cv2
import os
import numpy as np
from PIL import Image
import pickle



# Create your views here.

@login_required(login_url='login')
def employee_list(request):
    context = {'employee_list': Employee.objects.all()}
    return render(request, 'employee_list.html', context)

@login_required(login_url='login')
def employee_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EmployeeForm()
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(instance=employee)
        return render(request, 'employee_form.html', {'form':form})
    else:
        if id == 0:
            form = EmployeeForm(request.POST)
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
        return redirect('/management/list')

@login_required(login_url='login')
def employee_delete(request,id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('/management/list')

def face_extractor(img):
    # function detects face and return the cropped face
    # if no face detected, it returns the input image
    face_cascade = cv2.CascadeClassifier('C:\\FYP\\auto_attendance_system\\haarcascades\\haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if faces is ():
        return None

    # crop all faces found
    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]

    return cropped_face

@login_required(login_url='login')
def collect_data(request, id):
    employee = Employee.objects.get(pk=id)
    id_num = employee.employee_id
    num = 1
    parent_dir = 'C:\\FYP\\auto_attendance_system\\management\\training_dataset'
    path = os.path.join(parent_dir, id_num)
    try:
        os.mkdir(path)

        # Initialize webcam
        cap = cv2.VideoCapture(0)
        count = 0
        #print("Start capturing the input Data Set")

        while True:
            ret, frame = cap.read()

            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (500, 500))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # save file in specified directory with unique name
                cv2.imwrite(os.path.join(path, str(count) + '.jpg'), face)

                # put count on image and display live count
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow('Face Cropper', face)

            else:
                #print("Face not found")
                pass

            if (count % 400) == 0 and count != num * 400 and count != 0:
                cv2.waitKey()

            if cv2.waitKey(1) == 13 or count == num * 400:  # 13 is the Enter key
                break

        cap.release()
        cv2.destroyAllWindows()
        employee.photo_status = 1
        employee.save()
    except:
        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()

        messagebox.showerror('Capturing  Faces', 'The image sample of this Employee already exists in the system.')
        window.deiconify()
        window.destroy()
        window.quit()
    return redirect('/management/list')
    #print("Collecting Samples Complete")

@login_required(login_url='login')
def train_system(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "training_dataset")
    face_cascade = cv2.CascadeClassifier('C:\\FYP\\auto_attendance_system\\haarcascades\\haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(root)
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]
                pil_image = Image.open(path).convert("L")  # grayscale
                final_image = pil_image.resize((500, 500), Image.ANTIALIAS)
                image_array = np.array(final_image, "uint8")
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.3, minNeighbors=5)
                for (x, y, w, h) in faces:
                    roi = image_array[y:y + h, x:x + w]
                    x_train.append(roi)
                    y_labels.append(id_)


    with open("C:\\FYP\\auto_attendance_system\\pickle\\labels.pickle", 'wb') as f:
        pickle.dump(label_ids, f)
    try:
        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("C:\\FYP\\auto_attendance_system\\recognizer\\face-trainer.yml")

        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()

        messagebox.showinfo('Training', 'Your System is Trained Successfully')
        window.deiconify()
        window.destroy()
        window.quit()
    except:
        if os.path.isfile("C:\\FYP\\auto_attendance_system\\pickle\\labels.pickle"):
            os.remove("C:\\FYP\\auto_attendance_system\\pickle\\labels.pickle")
        if os.path.isfile("C:\\FYP\\auto_attendance_system\\recognizer\\face-trainer.yml"):
            os.remove("C:\\FYP\\auto_attendance_system\\recognizer\\face-trainer.yml")
        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()

        messagebox.showerror('Training', 'No images found to train.')
        window.deiconify()
        window.destroy()
        window.quit()
    return redirect('/')

@login_required(login_url='login')
def recognize_face(request):
    face_cascade = cv2.CascadeClassifier('C:\\FYP\\auto_attendance_system\\haarcascades\\haarcascade_frontalface_default.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read("C:\\FYP\\auto_attendance_system\\recognizer\\face-trainer.yml")

        labels = {"person_name": 1}
        with open("C:\\FYP\\auto_attendance_system\\pickle\\labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v: k for k, v in og_labels.items()}



        cap = cv2.VideoCapture(0)

        while (True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]

                id_, conf = recognizer.predict(roi_gray)

                if conf < 500:
                    success = int(100 * (1 - (conf) / 400))


                if success > 80:
                    id = labels[id_]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    color = (255, 255, 255) # BGR 0-255
                    stroke = 2
                    display_string = 'If your ID is ' + id + ' Hit Enter'
                    cv2.putText(frame, str(success) + ' %  ' + id, (x, y-9), font, 1, color, stroke, cv2.LINE_AA)
                    cv2.putText(frame, display_string, (0, 450), font, 1, color, stroke)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


            # Display the resulting frame
            cv2.putText(frame, 'Press e to exit', (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)

            pressedKey = cv2.waitKey(1)
            if pressedKey == 13:
                try:
                    employee = Employee.objects.get(employee_id=id)
                    recognizedName = employee.name
                    recognizedID = id
                    recognizedGroup = employee.group
                    attendanceDate = datetime.now().date()
                    attendanceStatus = 'Present'

                    attendance_instance = Attendance.objects.create(name=recognizedName, employee_id=recognizedID, group=recognizedGroup, date=attendanceDate, attendance_status=attendanceStatus)
                    attendance_instance.save()
                    status = 1
                except:
                    window = Tk()
                    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                    window.withdraw()

                    messagebox.showerror('Recognition', 'There is no record of the person in the system.')
                    window.deiconify()
                    window.destroy()
                    window.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    return redirect('/')
                break
            elif pressedKey == ord('e'):
                status = 0
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        if status==1:
            return redirect('/management/view_attendance')
        else:
            return redirect('/')

    except:
        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()

        messagebox.showwarning('Recognition', 'Please train the system first.')
        window.deiconify()
        window.destroy()
        window.quit()
        return redirect('/')


@login_required(login_url='login')
def attendance_list(request):
    context = {'attendance_list': Attendance.objects.all()}
    return render(request, 'attendance_list.html', context)

@login_required(login_url='login')
def attendance_delete(request,id):
    attendance = Attendance.objects.get(pk=id)
    attendance.delete()
    return redirect('/management/view_attendance')

@login_required(login_url='login')
def attendance_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            att_form = AttendanceForm()
        else:
            attendance = Attendance.objects.get(pk=id)
            att_form = AttendanceForm(instance=attendance)
        return render(request, 'attendance_form.html', {'form':att_form})
    else:
        if id == 0:
            att_form = AttendanceForm(request.POST)
        else:
            attendance = Attendance.objects.get(pk=id)
            att_form = AttendanceForm(request.POST, instance=attendance)
        if att_form.is_valid():
            att_form.save()
        return redirect('/management/view_attendance')
