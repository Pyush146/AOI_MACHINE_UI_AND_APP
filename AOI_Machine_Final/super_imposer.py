import cv2
import pandas as pd
import numpy as np

# This Function is Defined to Superimpose the Annotations of The Standard Image and Draw the said annotations on the Aligned image produced by aligned.py file to verify if the Annotaions are Superimposed Correctly.

def draw_annotations():

    # Read the Aligned image and Store it in matrix form file path should br correct.

    img = cv2.imread('aligned.jpg', 1)

    # Read the Standard image annotations CSV File to get the Correct Vertices, File Path should by correct.

    annotations = pd.read_csv('annotations/Standard_Image.jpg.csv')
    data = annotations['Vertices'].to_numpy()

    # Point tranformation to get the four Vertices of all Annotated Component to Draw on aligned image.

    for point in data:
        point = point[:-3]
        point = point[3:]
        point = point.replace(']', '')
        point = point.replace('[', '') 
        point = point.split(',')
        point = np.array(point)
        point = np.reshape(point, (4, 2))

        # Draw the rectangle on the Identified Components to exactly Superimpose the Standard Image component on The Non Standard ALigned Image. (Image should be aligned before using the Function)

        cv2.rectangle(img, (int(point[0][0]), int(point[0][1])), (int(point[2][0]), int(point[2][1])), (0,0,255), 3)
    
    # Resize the Image to Get better View

    img = cv2.resize(img, (1000, 700))

    # Show the Produced Standard Image annotations Superimposed on ALigned Image.

    #cv2.imshow("image", img)
    
    # Store the Superimposed Image in specified Path.

    cv2.imwrite('super_imposed_image.jpg', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
