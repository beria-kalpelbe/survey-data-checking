import exifread

# Open the image file
with open('image.jpg', 'rb') as f:
    # Read the image data
    tags = exifread.process_file(f)

# Print the extracted metadata
for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'EXIF MakerNote'):
        print(f"{tag}: {tags.get(tag)}")