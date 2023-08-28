import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5)
tip_ids = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

def draw_hand_landmarks(image, hand_landmarks):
    if  hand_landmarks:
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
    
def count_fingers(image, hand_landmarks, hand_number = 0):
    if hand_landmarks:
        landmarks = hand_landmarks[hand_number].landmark
        #print(landmarks)
        
        fingers = []
        for lm_index in tip_ids:
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y
            if lm_index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    print("Finger with id", lm_index, "is Closed")
                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    print('Finger with id', lm_index, "is Closed")
        total_fingers = fingers.count(1)
        text = f'fingers:{total_fingers}'
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    
while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    result = hands.process(image)
    hand_landmarks = result.multi_hand_landmarks
    draw_hand_landmarks(image, hand_landmarks)
    count_fingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

