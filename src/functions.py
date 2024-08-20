import exifread
import pandas as pd
import cv2
import os
import glob

def get_image_paths(folder_path):
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif')
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
    return image_paths

def extract_metadata_one_image(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
    names = [key for key in tags.keys()]
    values = [tags[key] for key in tags.keys()]
    column_name = f"{image_path.split('/')[-1]}"
    data = pd.DataFrame({'Variable': names, f'{column_name}': values})
    return data

def extract_metadata_set_of_images(images_paths):
    metadatas = extract_metadata_one_image(images_paths[0])
    for image_path in images_paths:
        image_metadata = extract_metadata_one_image(image_path)
        metadatas = pd.merge(metadatas, image_metadata, on='Variable', how='outer')
    return metadatas        

def similarity_index(image_path1, image_path2):
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = [m for m in matches if m.distance < 30]
    return 100*len(good_matches)/len(matches)

def find_similar_images(images_paths):
    images_paths_copy = images_paths.copy()
    anchor_image_path = images_paths_copy[0]
    images_paths_copy.remove(anchor_image_path)
    similar = [anchor_image_path]
    for image_path in images_paths_copy:
        index = similarity_index(image_path, anchor_image_path)
        if index > 0.0:
            similar.append(image_path)
    return similar

def find_all_similar_images(images_paths):
    images_paths_copy = images_paths.copy()
    i = 0
    groups = {}
    while i<= len(images_paths_copy):
        groups[i] = find_similar_images(images_paths_copy)
        for element in groups[i]:
            images_paths_copy.remove(element)
        i += 1
    return groups




# paths = ['images/image1.jpg', 'images/image2.jpg', 'images/image3.jpg', 'images/image4.jpeg']

# groups = find_all_similar_images(paths)
# print(groups)

# image1 = Image.open('images/image1.jpg')
# image2 = Image.open('images/image2.jpg')
# tags = extract_metadata('images/image1.jpg')
# print(tags.head())
# plt.imshow(image)
# plt.show()


