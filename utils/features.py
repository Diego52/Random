import glob
import cv2
import imutils
import dlib
import os
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb

def create_database(group_folder):
    in_folder = group_folder + 'images/original/'
    out_folder = group_folder + 'images/faces/'
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('detectors/shape_predictor_68_face_landmarks.dat')
    fa = FaceAligner(predictor, desiredFaceWidth=256)
    for _dir in glob.glob(in_folder + '*'):
        _id = os.path.basename(_dir)
        if not os.path.exists(out_folder + _id + '/'):
            os.mkdir(out_folder + _id + '/')
        for _file in glob.glob(_dir + '/*'):
            filename = os.path.basename(_file)
            print(_file)
            image = cv2.imread(_file)
            image = imutils.resize(image, width=800)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # show the original input image and detect faces in the grayscale
            # image
            rects = detector(gray, 2)
            i = 0
            # loop over the face detections
            for rect in rects:
                # extract the ROI of the *original* face, then align the face
                # using facial landmarks
                (x, y, w, h) = rect_to_bb(rect)
                faceAligned = fa.align(image, gray, rect)
                outputname = out_folder + _id + '/' + filename 
                print(outputname)
                cv2.imwrite(outputname, faceAligned)
                i += 1

if __name__ == '__main__':
    create_database()