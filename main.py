import kivy.app
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import face_recognition
import glob
import cv2
import os

Builder.load_file('manage.kv')

img_direction = str()
folder_addresses = str()


class main_face(Screen):
    def find_matches(self, selectedFile, process_id):
        print("img_direction", img_direction)
        print("folder_addresses", folder_addresses)
        # image_path = './majid.jpg'
        try:
            azam_image = face_recognition.load_image_file(img_direction)
            # path = './azamdata'
            save_path = folder_addresses + '/find_simulatation'
            azam_face_encoding = face_recognition.face_encodings(azam_image)[0]
            known_face_encodings = [azam_face_encoding]

            if not os.path.exists(save_path):
                os.mkdir(save_path)

            data_path = os.path.join(folder_addresses, '*g')
            files = glob.glob(data_path)
            counter = 1

            for pic in files:
                img = cv2.imread(pic)
                rgb_img = img[:, :, ::-1]
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_img)
                face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
                face_names = []
                flag = 0
                for face_encoding in face_encodings:
                    if flag == 1:
                        break
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
                    name = None
                    if matches[0]:
                        name = "wanted"
                    face_names.append(name)

                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        if not name:
                            continue
                        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                        # Draw a label with a name below the face
                        cv2.rectangle(img, (left, bottom), (right, bottom), (0, 0, 255), cv2.FILLED)
                        new_path = ''.join((save_path + '/newpic', str(counter), '.jpg'))
                        counter = counter + 1
                        cv2.imwrite(new_path, img)
                        print(new_path)
                        flag = 1

            selectedFile.text = "Done!"
        except:
            selectedFile.text = "Bad Choice, Change sample image!!"
            process_id.background_color = [1, 0, 0, 1]


class image_screen(Screen):
    # def __init__(self, **kwargs):
    #     self.img = list()
    def callback_image_and_other_stuff(self, new_image_address, img, selectedFile, img_choose_id):
        try:
            # new_image_address = new_image_address[0].replace("\\", "/")
            img_dir = new_image_address[0]
            file_path, file_ext = os.path.splitext(img_dir)
            # file_name = file_path.split('/')[-1]
            if file_ext in ['.png', '.jpg']:
                print("file_dir", img_dir)
                global img_direction
                img_direction = img_dir
                img_choose_id.background_color = [0, 1, 1, 1]
                #img_choose_id.color = [0, 1, 1, 1]
                img.source = img_dir
                selectedFile.text = ' '
            else:
                selectedFile.text = "The file you chose is not an image. Please choose  an  image(png/ jpg). "
                #img_choose_id.color = [1, 0, 1, 1]
                img_choose_id.background_color = [1, 0, 0, 1]
        except:
            selectedFile.text = "The file you chose is not an image. Please choose  an  image(png/ jpg). "
            img_choose_id.background_color = [1, 0, 0, 1]


class help_screen(Screen):
    pass


class path_screen(Screen):
    def callback_path_and_other_stuff(self, folder_address, path_choose_id):
        try:
            # selectedFile.text = str(folder_address)
            print("folder_address", folder_address)
            global folder_addresses
            folder_addresses = folder_address
            #path_choose_id.color = [0, 1, 1, 1]
            path_choose_id.background_color = [0, 1, 1, 1]
        except:
            path_choose_id.background_color = [1, 0, 0, 1]

sm = ScreenManager()

sm.add_widget(main_face(name='main_face'))
sm.add_widget(image_screen(name='image_screen'))
sm.add_widget(path_screen(name='path_screen'))
sm.add_widget(help_screen(name='help_screen'))


class TestApp(kivy.app.App):
    def build(self):
        return sm

    # print(path_screen.path)


app = TestApp()
app.run()
