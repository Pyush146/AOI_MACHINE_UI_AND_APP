import shutil
import cv2
import numpy as np
import pandas as pd
from ast import literal_eval
import imutils

# Pixel to CNC Transformation Parameters

xp=0.02955275
yp=0.02924065
xc=0.6179165
yc=0.4992825

dx = -0.04782644580618903
dy = 0.05856534126471486

# Feature Matching Parameter to Get Correct Aligment, Maximum features that will match will be 5000 and 15% Match percentage will be Considered as Good Match.

MAX_FEATURES = 5000
GOOD_MATCH_PERCENT = 0.15

# Function to Get the Median of All X and Y cordinates which is Part of Pixel to CNC Transformation.

def median(coord):
    x=0
    y=0
    for i in range(4):
        x+=coord[i][0]
        y+=coord[i][1]
    x=x/4
    y=y/4
    median_coord = np.array([x,y])
    return(median_coord)

# This Function is Used to Align The image according to the Given Reference Image.
# im1 is the Non Aligned image and The im2 image is Standard image which is used as reference for the im1 image to Align it as reference.

def alignImages(im1, im2):

  # Convert images to grayscale
  im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

  # Detect ORB features and compute descriptors.
  orb = cv2.ORB_create(MAX_FEATURES)
  keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
  keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

  # Match features.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = matcher.match(descriptors1, descriptors2, None)

  # Sort matches by score

  matches = sorted(matches, key=lambda x:x.distance)

  # Remove not so good matches

  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]

  # Draw top matches

  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
  cv2.imwrite("matches.jpg", imMatches)

  # Extract location of good matches

  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)

  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt

  # Find homography

  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

  # Use homography

  height, width, channels = im2.shape
  im1Reg = cv2.warpPerspective(im1, h, (width, height))
  return im1Reg, h

# Part of Image Component Vertices Superimposition.

def new_coord(tr_coord,h):
  h_inv = np.linalg.inv(h)
    
  fin_coord=[]
  for i in range(4):
      coord = np.append(tr_coord[i],1).reshape(3,-1)
      mod_coord = np.divide(np.dot(h_inv,coord),np.dot(h_inv,coord)[2])
      mod_coord = mod_coord.astype(int)
      mod_coord = np.delete(mod_coord,2)
      mod_coord.reshape(-1,2)
      fin_coord.append(mod_coord)
  fin_coord = np.array(fin_coord)
  return(fin_coord)


def complete_alignment():
  # Read reference image

  refFilename = "Standard_Image_folder/Standard_Image.jpg"

  imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

  # Read image to be aligned

  imFilename = "Captured_Image_folder/Captured_Image.jpg"

  im = cv2.imread(imFilename, cv2.IMREAD_COLOR)


  # Registered image will be restored in imReg.
  # The estimated homography will be stored in h.

  imReg, h = alignImages(im, imReference)

  # Write aligned image to disk.
  outFilename = "aligned.jpg"

  cv2.imwrite(outFilename, imReg)

  aligned = imutils.resize(imReg, width=700)
  template = imutils.resize(imReference, width=700)

  # our first output visualization of the image alignment will be a
  # side-by-side comparison of the output aligned image and the
  # template

  stacked = np.hstack([aligned, template])

  # our second image alignment visualization will be *overlaying* the
  # aligned image on the template, that way we can obtain an idea of
  # how good our image alignment is

  overlay = template.copy()
  output = aligned.copy()
  cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)

  # show the two output image alignment visualizations

#  cv2.imshow("Image Alignment Stacked", stacked)
 # cv2.imshow("Image Alignment Overlay", output)
  #cv2.waitKey(0)

  # Read the Standard Annotations Created by S3A PCB annotator and Make sure the CSV file Path is correct otherwise program will throw the Error.
  shutil.copy("C:/Users/Relax/.s3a/s3aprj/annotations/Standard_Image.jpg.csv", "annotations/Standard_Image.jpg.csv")
  tr_csv = pd.read_csv("C:/Users/Relax/.s3a/s3aprj/annotations/Standard_Image.jpg.csv")
  data = tr_csv['Vertices'].to_numpy()

  # Used create a CSV file Showing the Relation between Standard Image and Captured Image.

  for i in range(data.size):
      res = np.array(literal_eval(data[i]))
      or_coord = new_coord(res[0],h)
      or_coord = or_coord.reshape(1,4,2)
      or_coord = str(or_coord).replace('\n  ','s')
      or_coord = str(or_coord).replace(' ',', ')
      or_coord = str(or_coord).replace(', , ',', ')
      or_coord = str(or_coord).replace('s',', ')
      data[i] = or_coord.replace('','')

  tr_csv.iloc[:,2] = data
  tr_csv.to_csv(r'annotations/Captured_Image.jpg.csv',index=False)

  CNC_ratio=np.array([dx,dy])

  # Read the Captured Image CSV file to Calculate the Center Differences of Different Components on annotated Standard PCB and Non Standard Image.

  mod_csv = pd.read_csv("annotations/Captured_Image.jpg.csv")
  data = mod_csv['Vertices'].to_numpy()

  mod_img = cv2.imread("Captured_Image_folder/Captured_Image.jpg")

  centre_x = mod_img.shape[0]/2
  centre_y = mod_img.shape[1]/2
  center = np.array([centre_y,centre_x])

  # Calculate the CNC Movements using Center Differences to Iterate on Centers of Different Components on Non-Standard Image.

  medians=[]
  center_diffs=[]
  CNC_movements=[]

  # Iterate through the Component Vertices to get The Component vertices and Transform it in CNC Movements.

  for i in range(data.size):
      res = np.array(literal_eval(data[i]))
      # print(res[0])
      median_coord = median(res[0])
      medians.append(median_coord)

      pixel_diff = np.subtract(median_coord,center)
      center_diffs.append(pixel_diff)

      CNC_movements.append(np.multiply(pixel_diff,CNC_ratio))

  # Median, Center Difference and CNC Movements these three values are stored in cnc_movements.csv File

  mod_csv['Medians'] = medians
  mod_csv['Center_diffs'] = center_diffs
  mod_csv['CNC_movements'] = CNC_movements

  # Write the Calculated CNC Movements in the CSV file to use it for iterating between the Different Components.

  mod_csv.to_csv(r'cnc_movements.csv',index=False)
