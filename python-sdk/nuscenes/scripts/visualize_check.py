import cv2
import os
import json

from collections import defaultdict

"""
/mnt/data1/public_datasets/Odaiba_JT_v1.0/b449e9eb-daeb-4934-89c7-c97ddbc3a615
"""

class AnnotationInfo:
    def __init__(self):
        pass
    def set_imgpath(self, img_path):
        self.img_path = img_path
    def set_filename(self, filename):
        self.filename = filename
    def set_bbox(self, bbox):
        self.bbox = bbox
    def set_category_name(self, category_name):
        self.category_name = category_name

def visualize_bboxes(json_file, root_dir):
    """
    Visualize bounding boxes in an image.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    file_annotation_dict = defaultdict(list)

    for record in data:
        annotation_info = AnnotationInfo()
    
        img_path = os.path.join(root_dir, record['filename'])
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        
        x1, y1, x2, y2 = map(int, record['bbox_corners'])
        annotation_info.set_imgpath(img_path)
        annotation_info.set_filename(record['filename'])
        annotation_info.set_bbox([x1, y1, x2, y2])
        annotation_info.set_category_name(record['category_name'])
        file_annotation_dict[img_path].append(annotation_info)

    for img_path, annotation_infos in file_annotation_dict.items():
        img = cv2.imread(img_path)
        for annotation_info in annotation_infos:
            # print(annotation_info.img_path)
            # print(annotation_info.bbox)
            # print(annotation_info.category_name)

            x1, y1, x2, y2 = annotation_info.bbox
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, annotation_info.category_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        save_name =  rootdir + '/image_with_boxes/' + annotation_info.filename.replace('/', '_')
        cv2.imwrite(os.path.join(save_name), img)
        print(f"Saved image with bounding box: {save_name}")


rootdir = "/mnt/data1/public_datasets/Odaiba_JT_v1.0/b449e9eb-daeb-4934-89c7-c97ddbc3a615"
json_file = os.path.join(rootdir, 'annotation/image_annotations.json')
visualize_bboxes(json_file, rootdir)