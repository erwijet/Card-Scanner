import cv2
import numpy as np
import os
import keyboard

from parse import format_card_string_for_database
from mongo_import import insert_card_into_owned_collection

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

CARDS_TO_ADD = []
CARD_TYPE = 'U' # UNDEF

print('MTG M19 CARD SCANNER...')
print('1. INSTANT')
print('2. CREATUE')
print('3. SORCERY')
print('4. ENCHANTMENT')
print('5. PLANESWALKER')

while True:
    #print(CARD_TYPE)
    if (CARD_TYPE != 'U'):
        break
    if (keyboard.is_pressed('1')):
        CARD_TYPE = 'instant'
    elif (keyboard.is_pressed('2')):
        CARD_TYPE = 'creature'
    elif (keyboard.is_pressed('3')):
        CARD_TYPE = 'sorcery'
    elif (keyboard.is_pressed('4')):
        CARD_TYPE = 'enchantment'
    elif (keyboard.is_pressed('5')):
        CARD_TYPE = 'planeswalker'
    else:
        continue

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted([ (cv2.contourArea(i), i) for i in contours ], key=lambda a:a[0], reverse=True)


    for _, contour in sorted_contours:
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 1)

    _, card_contour = sorted_contours[0]
    cv2.drawContours(frame, [card_contour], -1, (100, 100, 0), 2)
    _, card_contour = sorted_contours[1]
    cv2.drawContours(frame, [card_contour], -1, (255, 0, 0), 2)

    rect = cv2.minAreaRect(card_contour)
    points = cv2.boxPoints(rect)
    points = np.int0(points)

    for point in points:
        cv2.circle(frame, tuple(point), 3, (255,0,0), -1)


    if (keyboard.is_pressed('s')):
        # create a min area rectangle from contour
        _rect = cv2.minAreaRect(card_contour)
        box = cv2.boxPoints(_rect)
        box = np.int0(box)

        # create empty initialized rectangle
        rect = np.zeros((4, 2), dtype = "float32")

        # get top left and bottom right points
        s = box.sum(axis = 1)
        rect[0] = box[np.argmin(s)]
        rect[2] = box[np.argmax(s)]

        # get top right and bottom left points
        diff = np.diff(box, axis = 1)
        rect[1] = box[np.argmin(diff)]
        rect[3] = box[np.argmax(diff)]

        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))

        from PIL import Image, ImageFilter
        from glob import glob
        import imagehash

        # hash warped image
        hash = imagehash.average_hash(Image.fromarray(warped))

        lowest_score = 0
        scanned_card = ""
        cls() 
        # loop over all official images
        for orig in glob('img/{}/*.jpg'.format(CARD_TYPE)):

            # grayscale, resize, and blur original image
            orig_image = Image.open(orig).convert('LA')
            orig_image.resize((maxWidth, maxHeight))
            orig_image.filter(ImageFilter.BLUR)

            # hash original and get hash
            orig_hash = imagehash.average_hash(orig_image)
            score = hash - orig_hash
            if (lowest_score == 0):
                lowest_score = score
                scanned_card = orig
            elif (score < lowest_score):
                lowest_score = score
                scanned_card = orig
            #print('Testing card {} -> score {}'.format(orig, score))
        #print('='*60)
        #print('Best match: {}, (score: {})'.format(scanned_card, lowest_score))
         
        # Show the card the scanned image best matched to
        cv2.imshow('capture', warped)
        cv2.imshow('card', cv2.imread(scanned_card))
    # Show preview of cam
    cv2.imshow('frame', frame)

    if (cv2.waitKey(1) == ord('a') and scanned_card != ""):
        print("addded card!")
        insert_card_into_owned_collection(format_card_string_for_database(scanned_card))
cap.release()
cv2.destroyAllWindows()