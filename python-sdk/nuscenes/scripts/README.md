# Convert Tier4 dataset to yolo format
1. create 2d label for tier4 dataset
```
python gen_2d_labels.py
```
this will create a json file named 'image_annotations.json' under directory 'Odaiba_JT_v1.0/xxx/annotations'

2. convert to yolo format
```
python convert2yolo.py
```
this will create a yolo format label txt under the same directory where picture is saved 

