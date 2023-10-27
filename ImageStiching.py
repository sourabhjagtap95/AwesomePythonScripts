import cv2
import numpy as np 

img1 = input("Enter the path of the first image: ")
img2 = input("Enter the path of the second image: ")

train = cv2.imread(r"{}".format(img1))
query = cv2.imread(r"{}".format(img2))
train_RGB = cv2.cvtColor(train,cv2.COLOR_BGR2RGB)
query_RGB = cv2.cvtColor(query,cv2.COLOR_BGR2RGB)
train_gray = cv2.cvtColor(train_RGB,cv2.COLOR_RGB2GRAY)
query_gray = cv2.cvtColor(query_RGB,cv2.COLOR_RGB2GRAY)

query_gray = cv2.resize(query,(500,300))
train_gray = cv2.resize(train,(500,300))
query = cv2.resize(query,(500,300))
train = cv2.resize(train,(500,300))
feature_extraction_algo = 'sift'
feature_to_match = 'bf'

def select_descriptor(image,method=None):
    assert method is not None,"Please define a descriptor method. Accepted values are 'Sift','Surf','orb','brisk' "

    if method == 'sift':
        descriptor  = cv2.SIFT_create()
    if method == 'surf':
        descriptor  = cv2.SURF_create()
    if method == 'orb':
        descriptor  = cv2.ORB_create()
    if method == 'brisk':
        descriptor  = cv2.BRISK_create()
    (keypoints,features) = descriptor.detectAndCompute(image,None)
    return (keypoints,features)

keypoints_train,feature_train = select_descriptor(train_gray,feature_extraction_algo)
keypoints_query,feature_query = select_descriptor(query_gray,feature_extraction_algo)

# print(keypoints_query)
# for keypoint in keypoints_query:
#     x,y = keypoint.pt
#     size = keypoint.size
#     orientation = keypoint.angle
#     response = keypoint.response
#     octave = keypoint.octave
#     class_id = keypoint.class_id
#     print(x,y)
# cv2.imshow("Image1  ",cv2.drawKeypoints(train_gray,keypoints_train,None,color=(0,255,0)))
# cv2.imshow("Image2",cv2.drawKeypoints(query_gray,keypoints_query,None,color=(0,255,0))) # to draw key points 
cv2.imshow("Image 1",train)
cv2.imshow("Image 2",query)

def create_matching_object(method,crossCheck):
    if method == 'sift' or method == 'surf':
        bf = cv2.BFMatcher(cv2.NORM_L2,crossCheck=crossCheck)
    if method == 'brisk' or method == 'orb':
        bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck==crossCheck)
    
    return bf

def keypoints_matching(feature_train,feature_query,method):
    bf = create_matching_object(method,True)
    best_matches = bf.match(feature_train,feature_query)
    raw_matches = sorted(best_matches,key = lambda x:x.distance)
    print("Raw Matches with Brute Force",len(raw_matches))
    return raw_matches

def keypoints_matching_knn(feature_train,feature_query,ratio,method):
    bf = create_matching_object(method,False)
    raw_matches = bf.knnMatch(feature_train,feature_query,k=2)
    print("Raw Matches with Knn",len(raw_matches))

    knn_matches=[]
    for m,n in raw_matches:
        if m.distance<n.distance*ratio:
            knn_matches.append(m)
    return knn_matches

print("Drawing Matched features for ",feature_to_match)
if feature_to_match == 'bf':
    matches = keypoints_matching(feature_train,feature_query,feature_extraction_algo)
    mapped_feature = cv2.drawMatches(train,keypoints_train,query,keypoints_query,matches[:100],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

elif feature_to_match == 'knn':
    matches = keypoints_matching_knn(feature_train,feature_query,0.75,feature_extraction_algo)
    # print(matches)
    mapped_feature = cv2.drawMatches(train,keypoints_train,query,keypoints_query,np.random.choice(matches,100),None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imshow("Mapped",mapped_feature)
def homography_Stiching(keypoints_train,keypoints_query,reprojthreshhold):
    # convert to numpy array 
    keypoints_train_image = np.float32([keypoint.pt for keypoint in keypoints_train])
    keypoints_query_image = np.float32([keypoint.pt for keypoint in keypoints_query])

    if len(matches)>4:
        points_train = np.float32([keypoints_train_image[m.queryIdx] for m in matches])
        points_query= np.float32([keypoints_query_image[m.trainIdx] for m in matches])

        (H,status)=cv2.findHomography(points_train,points_query,cv2.RANSAC,reprojthreshhold)
        return (matches,H,status)
    
    else:
        return None
    
M = homography_Stiching(keypoints_train,keypoints_query,4)
if M is None:
    print('Error')
(matches,Homography_Matrix,status) = M
print(Homography_Matrix)
width = query.shape[1]+train.shape[1]
print(width)
height = max(query.shape[0],train.shape[0])
print(height)

result = cv2.warpPerspective(train,Homography_Matrix,(width,height))
print(result)

result[0:query.shape[0],0:query.shape[1]] = query

cv2.imshow("Stich",result)
cv2.waitKey(0)
cv2.destroyAllWindows()