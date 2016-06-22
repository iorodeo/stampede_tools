from __future__ import print_function
import sys
import json
import cv2
import scipy
import matplotlib.pyplot as plt

def median_background(params):

    input_video = params['input_video']
    cap = cv2.VideoCapture(input_video)
    
    cnt = 0
    frame_list = []
    
    while cap.isOpened():
    
        ret, frame_bgr = cap.read()
        if not ret:
            break
    
        frame_gry = cv2.cvtColor(frame_bgr,cv2.COLOR_BGR2GRAY)
    
        # Select Region of interest
        c0,c1 = params['roi_cols']
        r0,r1 = params['roi_rows']
        frame_gry = frame_gry[r0:r1,c0:c1]
    
    
        if cnt%params['background_frame_skip'] == 0:
            frame_list.append(frame_gry)
    
        cv2.imshow('frame', frame_gry)
        if cnt == 0 and params['background_check_roi']:
            print()
            print("Does ROI look ok? press q to quit and adjust or press any key to continue")
            wait_val = 0
        else:
            wait_val = 1

        if cv2.waitKey(wait_val) & 0xff == ord('q'): 
                cap.release()
                cv2.destroyAllWindows()
                sys.exit(0)

        print('frame: {0}'.format(cnt))
        cnt+=1
    
    cap.release()
    
    frame_array = scipy.array(frame_list)
    frame_med = scipy.median(frame_array,0)
    frame_med = frame_med.astype(scipy.uint8) 
    
    cv2.imshow('median',frame_med)
    cv2.waitKey(0)
    
    output_file = params['background_file']
    cv2.imwrite(output_file,frame_med)
    
    cv2.destroyAllWindows()

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # Testing
    params_file = sys.argv[1]
    with open(params_file,'r') as f:
        params = json.load(f)
    median_background(params)




