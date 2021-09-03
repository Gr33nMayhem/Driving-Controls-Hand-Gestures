from utils import detector_utils as detector_utils
import cv2
import tensorflow as tf

cap = cv2.VideoCapture(0)
detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':
    im_width, im_height = (cap.get(3), cap.get(4))
    num_hands_detect=2
    cv2.namedWindow('Hand Gesture Detection', cv2.WINDOW_NORMAL)

    while True:
        ret, image_np = cap.read()
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        boxes, scores = detector_utils.detect_objects(
            image_np, detection_graph, sess)

        lst=detector_utils.draw_box_on_image(
            num_hands_detect, 0.2, scores, boxes, im_width, im_height, image_np)
        print(lst)
		
        cv2.imshow('Single-Threaded Detection', cv2.cvtColor(
    	    image_np, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
