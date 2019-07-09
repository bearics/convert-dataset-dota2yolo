# convert-dataset-dota2yolo

convert dataset format DOTA's labelTxt-v1.5 to qqwweee/keras-yolo3's row format.

### DOTA's labelTxt-v1.5

```
'imagesource':imagesource 
'gsd':gsd 
x1, y1, x2, y2, x3, y3, x4, y4, category, difficult 
x1, y1, x2, y2, x3, y3, x4, y4, category, difficult
... 
```

### qqwweee/keras-yolo3's row format

Row format: image_file_path box1 box2 ... boxN;
Box format: x_min,y_min,x_max,y_max,class_id (no space).

```
path/to/img1.jpg 50,100,150,200,0 30,50,200,120,3
path/to/img2.jpg 120,300,250,600,2
...
```
