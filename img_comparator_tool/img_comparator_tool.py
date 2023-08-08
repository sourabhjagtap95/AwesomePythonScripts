# This tool helps to compare two images and specifically colors the difference in red in the second image argument
import cv2
def img_comparator(imPath1,imPath2):
    img1 = cv2.imread(imPath1)
    img2 = cv2.imread(imPath2)

    if img1 is None or img2 is None:
        return "Images weren't loaded successfully!!"

    # resize the images to same dimension
    img1 = cv2.resize(img1,(300,300))
    img2 = cv2.resize(img2,(300,300))

    # calculating difference between two images
    diff = cv2.subtract(img1,img2)
    b,g,r = cv2.split(diff)
    if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
        return "The images are identical"
    else:
        # color the mask red
        conv_hsv_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(
            conv_hsv_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )
        diff[mask != 255] = [0, 0, 255]

        # add the red mask to the images to spot the differences
        img1[mask != 255] = [0, 0, 255]
        img2[mask != 255] = [0, 0, 255]

        cv2.imwrite("difference.png", diff)
        return "The images are different!!"     


img1 = "python_img.jpg"
img2 = "image2.jpg"
print(img_comparator(img1,img2))