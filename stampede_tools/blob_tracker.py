from __future__ import print_function
import sys
import json
import cv2
import scipy
import os


def track_blobs(params):

    cv_major_ver, cv_minor_ver, _ = cv2.__version__.split('.')
    cv_major_ver = int(cv_major_ver)
    cv_minor_ver = int(cv_minor_ver)

    input_video = params['input_video'] 
    background_file = params['background_file']
    median_centroid_file = params["median_centroid_file"]
    tracking_output_video = params["tracking_output_video"]

    background_threshold = params['background_threshold']
    kernel_size = params['open_kernel_size']
    blob_area_min = params['blob_area_min']
    blob_area_max = params['blob_area_max']

    vidin = cv2.VideoCapture(input_video)
    vidout = cv2.VideoWriter()
    
    frame_background = cv2.imread(background_file,0)
    median_centroid_fid = open(median_centroid_file,'w')
    
    cnt = 0
    blob_count_list = []
    median_centroid_list = []
    
    while vidin.isOpened():
    
        # Read frame from video file and convert to mono image
        ret, frame_bgr = vidin.read()
        if not ret:
            break
        frame_gry = cv2.cvtColor(frame_bgr,cv2.COLOR_BGR2GRAY)
    
        # Select Region of interest
        c0,c1 = params['roi_cols']
        r0,r1 = params['roi_rows']
        frame_gry = frame_gry[r0:r1,c0:c1]
    
        # Remove background and threshold image
        frame_dif = cv2.absdiff(frame_gry,frame_background)
        ret, frame_thr = cv2.threshold(frame_dif,background_threshold,255,cv2.THRESH_BINARY)
    
        # Perform morphological open - to try and remove small blobs
        kernel = scipy.ones(kernel_size,scipy.uint8)
        frame_opn = cv2.morphologyEx(frame_thr, cv2.MORPH_OPEN, kernel)
    
        # Find blobs - get list of blob contours
        frame_tmp = scipy.array(frame_opn)
        if cv_major_ver < 3:
            contour_list, dummy = cv2.findContours(frame_tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contour_list, heirarchy = cv2.findContours(frame_tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # Filter blobs and find blob centroids
        blob_list = []
        centroid_list = []
        for contour in contour_list:
            area = cv2.contourArea(contour)
            if area >= blob_area_min and area <= blob_area_max:
                moments = cv2.moments(contour)
                centroid_x = moments['m10']
                if moments['m00'] > 0:  
                    centroid_x = moments['m10']/moments['m00'] 
                    centroid_y = moments['m01']/moments['m00']
                    blob_list.append(contour)
                    centroid_list.append((centroid_x,centroid_y))
    
        centroid_array = scipy.array(centroid_list)
        median_centroid = scipy.median(centroid_array,axis=0)
        median_centroid_list.append(median_centroid)
        blob_count_list.append(len(blob_list))
    
        # Plot contours
        frame_drw = scipy.array(frame_gry)
        frame_drw = cv2.cvtColor(frame_drw,cv2.COLOR_GRAY2BGR)
        cv2.drawContours(frame_drw,blob_list, -1,(0,0,255),2)
    
        # Create temporary BGR versions of intermediate analysis images - required for composite image
        temp_gry = cv2.cvtColor(frame_gry,cv2.COLOR_GRAY2BGR)
        temp_dif = cv2.cvtColor(frame_dif,cv2.COLOR_GRAY2BGR)
        temp_opn = cv2.cvtColor(frame_opn,cv2.COLOR_GRAY2BGR)
        frame_cmp = scipy.concatenate((temp_gry,temp_dif,temp_opn,frame_drw),axis=0)
        cv2.imshow('composite',frame_cmp)
    
        print('frame: {0}, numblob: {1}, cx: {2}'.format(cnt,len(blob_list), median_centroid[0]))
        median_centroid_fid.write('{0} {1}{2}'.format(cnt,median_centroid[0],os.linesep))
    
        if cnt == 0:
            if cv_major_ver < 3:
                fourcc = cv2.cv.CV_FOURCC(*'xvid')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'xvid')
            n = frame_cmp.shape[1]
            m = frame_cmp.shape[0]
            vidout.open(tracking_output_video,fourcc,30,(n,m),True)
    
        if vidout.isOpened():
            vidout.write(frame_cmp)
        else:
            print('Error: output video not opened')
            break
    
        if cv2.waitKey(1) & 0xff == ord('q'): #or cnt > 200: 
            break
        cnt+=1
    
        
    vidin.release()
    vidout.release()
    cv2.destroyAllWindows()
    median_centriod_fid.close()

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    params_file = sys.argv[1]
    with open(params_file,'r') as f:
        params = json.load(f)
    track_blobs(params)
