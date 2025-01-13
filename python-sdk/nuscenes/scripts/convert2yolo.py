import cv2
import os
import json

from collections import defaultdict
from pathlib import Path

import pdb

class AnnotationInfo:
    def __init__(self):
        pass
    def set_imgpath(self, img_path):
        self.img_path = img_path

    def set_img_shape(self, shape):
        self.shape = shape
    def set_filename(self, filename):
        self.filename = filename
    def set_bbox(self, bbox):
        self.bbox = bbox
    def set_category_name(self, category_name):
        self.category_name = category_name

# def visualize_bboxes(json_file, root_dir):
#     """
#     Visualize bounding boxes in an image.
#     """
#     with open(json_file, 'r') as file:
#         data = json.load(file)
    
#     file_annotation_dict = defaultdict(list)

#     for record in data:
#         annotation_info = AnnotationInfo()
    
#         img_path = os.path.join(root_dir, record['filename'])
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load image: {img_path}")
#             continue
        
#         x1, y1, x2, y2 = map(int, record['bbox_corners'])
#         annotation_info.set_imgpath(img_path)
#         annotation_info.set_filename(record['filename'])
#         annotation_info.set_bbox([x1, y1, x2, y2])
#         annotation_info.set_category_name(record['category_name'])

        

#         file_annotation_dict[img_path].append(annotation_info)

#     for img_path, annotation_infos in file_annotation_dict.items():
#         img = cv2.imread(img_path)
#         for annotation_info in annotation_infos:
#             # print(annotation_info.img_path)
#             # print(annotation_info.bbox)
#             # print(annotation_info.category_name)

#             x1, y1, x2, y2 = annotation_info.bbox
#             yolo = [0, (x1 + x2) / 2, (y1 + y2) / 2, (x2 - x1), (y2 - y1)]

#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(img, annotation_info.category_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


#         save_name =  rootdir + '/image_with_boxes/' + annotation_info.filename.replace('/', '_')
#         cv2.imwrite(os.path.join(save_name), img)
#         print(f"Saved image with bounding box: {save_name}")


# def img2label_paths(img_paths):
#     """Define label paths as a function of image paths."""
#     sa, sb = f"{os.sep}images{os.sep}", f"{os.sep}labels{os.sep}"  # /images/, /labels/ substrings
#     return [sb.join(x.rsplit(sa, 1)).rsplit(".", 1)[0] + ".txt" for x in img_paths]




# coco
# names:
#   0: person
#   1: bicycle
#   2: car
#   3: motorcycle
#   4: airplane
#   5: bus
#   6: train
#   7: truck
#   8: boat
#   9: traffic light
#   10: fire hydrant
#   11: stop sign
#   12: parking meter
#   13: bench
#   14: bird
#   15: cat
#   16: dog
#   17: horse
#   18: sheep
#   19: cow
#   20: elephant
#   21: bear
#   22: zebra
#   23: giraffe
#   24: backpack
#   25: umbrella
#   26: handbag
#   27: tie
#   28: suitcase
#   29: frisbee
#   30: skis
#   31: snowboard
#   32: sports ball
#   33: kite
#   34: baseball bat
#   35: baseball glove
#   36: skateboard
#   37: surfboard
#   38: tennis racket
#   39: bottle
#   40: wine glass
#   41: cup
#   42: fork
#   43: knife
#   44: spoon
#   45: bowl
#   46: banana
#   47: apple
#   48: sandwich
#   49: orange
#   50: broccoli
#   51: carrot
#   52: hot dog
#   53: pizza
#   54: donut
#   55: cake
#   56: chair
#   57: couch
#   58: potted plant
#   59: bed
#   60: dining table
#   61: toilet
#   62: tv
#   63: laptop
#   64: mouse
#   65: remote
#   66: keyboard
#   67: cell phone
#   68: microwave
#   69: oven
#   70: toaster
#   71: sink
#   72: refrigerator
#   73: book
#   74: clock
#   75: vase
#   76: scissors
#   77: teddy bear
#   78: hair drier
#   79: toothbrush


def clsName2id(cls_name):
    """
    Convert class name to id.
    """
    cls_id = -1

    if cls_name == 'vehicle.car':
        cls_id = 0
    if cls_name == 'vehicle.truck':
        cls_id = 1
    if cls_name == 'vehicle.construction': 
        cls_id = 2
    if cls_name == 'vehicle.bus (bendy & rigid)':
        cls_id = 3
    if cls_name == 'vehicle.trailer':
        cls_id = 4
    if cls_name == 'vehicle.motorcycle':
        cls_id = 5
    if cls_name == 'vehicle.bicycle':
        cls_id = 6
    if cls_name == 'vehicle.emergency (ambulance & police)':
        cls_id = 7
    if cls_name == 'pedestrian.adult'\
        or cls_name == 'pedestrian.child'\
        or cls_name == 'pedestrian.construction_worker'\
        or cls_name == 'pedestrian.police_officer'\
        or cls_name == 'pedestrian.wheelchair'\
        or cls_name == 'pedestrian.stroller'\
        or cls_name == 'pedestrian.personal_mobility':\
        cls_id = 8
    if cls_name == 'movable_object.trafficcone':
        cls_id = 9
    if cls_name == 'movable_object.barrier':
        cls_id = 10
    if cls_name == 'movable_object.debris':
        cls_id = 11
    if cls_name == 'movable_object.pushable_pullable':
        cls_id = 12
    if cls_name == 'static_object.bicycle_rack':
        cls_id = 13
    if cls_name == 'animal':
        cls_id = 14

    if cls_id == -1:
        raise ValueError(f"unknown cls_name: {cls_name} in the tier4 dataset")
        # print(f"unknown cls_name: {cls_name} in the tier4 dataset")
    return cls_id
    

def convert2yolo(rootdir):
    """
    Convert the dataset to YOLO format.
    在每一个图片的路径下,创建同名的.txt文件,记录yolo格式标注信息

    rootdir: 数据的目录路径. 比如1cf17b50-551f-4597-b589-01edf4b1302a
    """
    print("Converting to YOLO format...{}".format(rootdir))
    json_file = os.path.join(rootdir, 'annotation/image_annotations.json')

    with open(json_file, 'r') as file:
        data = json.load(file)
    
    file_annotation_dict = defaultdict(list)

    for record in data:
        annotation_info = AnnotationInfo()
    
        img_path = os.path.join(rootdir, record['filename'])
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        
        x1, y1, x2, y2 = map(int, record['bbox_corners'])
        annotation_info.set_imgpath(img_path)
        annotation_info.set_filename(record['filename'])
        annotation_info.set_bbox([x1, y1, x2, y2])
        annotation_info.set_category_name(record['category_name'])
        annotation_info.set_img_shape(img.shape)
        file_annotation_dict[img_path].append(annotation_info)

    # save to .txt label file
    for img_path, annotation_infos in file_annotation_dict.items():
        img = cv2.imread(img_path)
        #把Imgpath的后缀换成txt
        label_path = Path(img_path).with_suffix('.txt')
        f = open(label_path, 'w')
           
        for annotation_info in annotation_infos:
            # print(annotation_info.img_path)
            # print(annotation_info.bbox)
            # print(annotation_info.category_name)

            x1, y1, x2, y2 = annotation_info.bbox
            center_x = (x1 + x2) / 2 / annotation_info.shape[1]
            center_y = (y1 + y2) / 2 / annotation_info.shape[0]
            width = (x2 - x1) / annotation_info.shape[1]
            height = (y2 - y1) / annotation_info.shape[0]

            yolo_label = [clsName2id(annotation_info.category_name),center_x, center_y, width, height]

            f.write(' '.join(map(str, yolo_label)) + '\n')
        
        f.close()
        print('save label file:{}'.format(label_path))


def get_subdirectory_names(root_dir):
    """
    获取指定目录下的所有子目录名称。

    :param root_dir: 根目录路径
    :return: 子目录名称列表
    """
    subdirectory_names = []
    try:
        with os.scandir(root_dir) as it:
            for entry in it:
                if entry.is_dir():
                    subdirectory_names.append(entry.name)
    except FileNotFoundError:
        print(f"目录 {root_dir} 不存在")
    except PermissionError:
        print(f"没有权限访问目录 {root_dir}")
    except Exception as e:
        print(f"发生错误: {e}")
    
    return subdirectory_names
    
if __name__ == "__main__":
    # rootdir = "/home/sc/work/autoware_lab/Odaiba_JT_v1.0/1cf17b50-551f-4597-b589-01edf4b1302a"
    # convert2yolo(rootdir)
    rootdir = "/home/adas/dataset/Odaiba_JT_v1.0"
    subdirectory_names = get_subdirectory_names(rootdir)
    print('共计{}个子目录:'.format(len(subdirectory_names)))

    for i,subdir_name in enumerate(subdirectory_names):
        print('processing {} dir:{}'.format(i,subdir_name))
        subdir_fullpath = os.path.join(rootdir, subdir_name)
        convert2yolo(subdir_fullpath)

    # pdb.set_trace()