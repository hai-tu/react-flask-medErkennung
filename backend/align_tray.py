import cv2
import numpy as np
import argparse
import imutils
#import timeit

def getRectangles(image, templ):
    '''template matching function to find where the medics tray is!'''

    # convert template to grayscale
    # template = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
    template = templ.copy()

    # only use edges of the template
    # parameters can be changed with another template, these seem to work well
    template = cv2.Canny(template, 100, 200)

    (height, width) = template.shape[:2]
    # convert the image to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    temp_found = None
    # find the template in the image by resizing the image to different sizes
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # resize the image and store the ratio
        resized_img = imutils.resize(
            gray_image, width=int(gray_image.shape[1] * scale))
        ratio = gray_image.shape[1] / float(resized_img.shape[1])
        if resized_img.shape[0] < height or resized_img.shape[1] < width:
            break
        # Convert to edged image for checking
        e = cv2.Canny(resized_img, 150, 200)
        match = cv2.matchTemplate(e, template, cv2.TM_CCOEFF)
        (_, val_max, _, loc_max) = cv2.minMaxLoc(match)

        # use best found match
        if temp_found is None or val_max > temp_found[0]:
            temp_found = (val_max, loc_max, ratio)

        # check to see if the iteration should be visualized
        if 0:
            # draw a bounding box around the detected region
            clone = np.dstack([e, e, e])
            cv2.rectangle(clone, (loc_max[0], loc_max[1]),
                          (loc_max[0] + width, loc_max[1] + height), (0, 0, 255), 2)
            cv2.imshow("Visualize", clone)
            cv2.waitKey(0)

    # Get information from temp_found to compute x,y coordinate
    (_, loc_max, r) = temp_found
    (x_start, y_start) = (int(loc_max[0]*r), int(loc_max[1]*r))
    (x_end, y_end) = (int((loc_max[0] + width)*r), int((loc_max[1] + height)*r))

    return (x_start, y_start, x_end, y_end)

def get_Rotation_angle(img_object, img_scene):
    '''this keypoint matching function determines the rotation angle to shift the image back'''
    if img_object is None or img_scene is None:
        print('Could not open or find the images!')
        exit(0)

    #-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    minHessian = 400
    detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)
    keypoints_obj, descriptors_obj = detector.detectAndCompute(img_object, None)
    keypoints_scene, descriptors_scene = detector.detectAndCompute(img_scene, None)
    #-- Step 2: Matching descriptor vectors with a FLANN based matcher
    # Since SURF is a floating-point descriptor NORM_L2 is used
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors_obj, descriptors_scene, 2)

    #-- Filter matches using the Lowe's ratio test
    ratio_thresh = 0.75
    good_matches = []
    for m,n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)
    #-- Draw matches
    img_matches = np.empty((max(img_object.shape[0], img_scene.shape[0]), img_object.shape[1]+img_scene.shape[1], 3), dtype=np.uint8)
    cv2.drawMatches(img_object, keypoints_obj, img_scene, keypoints_scene, good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    #-- Localize the object
    obj = np.empty((len(good_matches),2), dtype=np.float32)
    scene = np.empty((len(good_matches),2), dtype=np.float32)
    for i in range(len(good_matches)):
        #-- Get the keypoints from the good matches
        obj[i,0] = keypoints_obj[good_matches[i].queryIdx].pt[0]
        obj[i,1] = keypoints_obj[good_matches[i].queryIdx].pt[1]
        scene[i,0] = keypoints_scene[good_matches[i].trainIdx].pt[0]
        scene[i,1] = keypoints_scene[good_matches[i].trainIdx].pt[1]

    H, _ =  cv2.findHomography(obj, scene, cv2.RANSAC)
    #-- Get the corners from the image_1 ( the object to be "detected" )
    obj_corners = np.empty((4,1,2), dtype=np.float32)
    obj_corners[0,0,0] = 0
    obj_corners[0,0,1] = 0
    obj_corners[1,0,0] = img_object.shape[1]
    obj_corners[1,0,1] = 0
    obj_corners[2,0,0] = img_object.shape[1]
    obj_corners[2,0,1] = img_object.shape[0]
    obj_corners[3,0,0] = 0
    obj_corners[3,0,1] = img_object.shape[0]
    scene_corners = cv2.perspectiveTransform(obj_corners, H)

    left_pt = (int(scene_corners[1,0,0] + img_object.shape[1]), int(scene_corners[1,0,1]))
    right_pt = (int(scene_corners[0,0,0] + img_object.shape[1]), int(scene_corners[0,0,1]))

    alpha = np.tan((left_pt[1]-right_pt[1])/(left_pt[0]-right_pt[0])) * 180/ np.pi

    return alpha, left_pt


if __name__ == '__main__':
    #start = timeit.timeit()
    parser = argparse.ArgumentParser(description='Code for Feature Matching with FLANN tutorial.')
    parser.add_argument('--input1', help='Path to input image 1.', default='segment_tray.png')
    parser.add_argument('--input2', help='Path to input image 2.',
                        default='Calibrated_Images/calibrated_Montag/calibrated_WIN_20220117_14_50_51_Pro.jpg')
    args = parser.parse_args()
    #print(args.input1, args.input2)
    img_object = cv2.imread(args.input1, cv2.IMREAD_GRAYSCALE)
    img_scene = cv2.imread(args.input2, cv2.IMREAD_GRAYSCALE)
    img_scene_color = cv2.imread(args.input2)

    # img_scene = cv.rotate(img_scene, cv.ROTATE_180)

    Use_Rotation_Correction = False

    if Use_Rotation_Correction:
        alpha, left_pt = get_Rotation_angle(img_object, img_scene)
        print(alpha)

        height, width = img_scene.shape[:2]
        rotate_matrix = cv2.getRotationMatrix2D(center = left_pt, angle = alpha, scale=1)
        rotated_image = cv2.warpAffine(src=img_scene_color, M=rotate_matrix, dsize=(width, height))

        x1, y1, x2, y2 = getRectangles(rotated_image, img_object)
        rectImage = rotated_image.copy()
    else:
        x1, y1, x2, y2 = getRectangles(img_scene_color, img_object)
        rectImage = img_scene_color.copy()

    '''split the found rectangular of the medics box into 4 equally distributed segments'''
    cv2.rectangle(rectImage, (x1, y1), (x2, y2), (255, 0, 0), 3)
    cv2.rectangle(rectImage, (x1, y1), (int(x1 + 0.25 * (x2 - x1)), y2), (0, 255, 0), 3)
    cv2.rectangle(rectImage, (int(x1 + 0.25 * (x2 - x1)), y1), (int(x1 + 0.5 * (x2 - x1)), y2), (0, 255, 0), 3)
    cv2.rectangle(rectImage, (int(x1 + 0.5 * (x2 - x1)), y1), (int(x1 + 0.75 * (x2 - x1)), y2), (0, 255, 0), 3)
    cv2.rectangle(rectImage, (int(x1 + 0.75 * (x2 - x1)), y1), (x2, y2), (0, 255, 0), 3)
    # cv2.imshow("rectangle", rectImage)
    # cv2.waitKey(0)

    if Use_Rotation_Correction:
        cv2.imwrite("segmentation_rotated.jpg", rectImage)
    else:
        cv2.imwrite("segmentation_original.jpg", rectImage)
    #print(timeit.timeit() - start)