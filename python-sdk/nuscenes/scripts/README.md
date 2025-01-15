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
this will create a yolo format label txt under the same directory where picture is saved. for example there would be a /home/adas/dataset/Odaiba_JT_v1.0/ec95e7e6-a2bd-4335-9923-bd90fe0c0b13/data/CAM_FRONT/58.txt which is yolo format label txt of 58.png

