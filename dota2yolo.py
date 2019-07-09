import os
import sys
import argparse
from os import listdir
from os.path import isfile, join


class Point:
  def __init__(self):
    self.x = 0
    self.y = 0

  def __init__(self, x, y):
    self.x = x
    self.y = y


class DotaBox:
  # x1, y1, x2, y2, x3, y3, x4, y4, category, difficult
  def __init__(self):
    self.points = []
    self.category = ""
    self.difficult = False

  def __init__(self, p1, p2, p3, p4, category, difficult):
    self.points = [p1, p2, p3, p4]  # P1 is Head point. The points behind a head point are clockwise other.
    self.category = category
    self.difficult = difficult

  def __init__(self, dota_raw_list: list):
    self.points = [Point(float(dota_raw_list[0]), float(dota_raw_list[1])),
                   Point(float(dota_raw_list[2]), float(dota_raw_list[3])),
                   Point(float(dota_raw_list[4]), float(dota_raw_list[5])),
                   Point(float(dota_raw_list[6]), float(dota_raw_list[7]))]
    self.category = dota_raw_list[8]
    self.difficult = int(dota_raw_list[9])


class YoloBox:
  def __init__(self):
    self.x_min = .0
    self.y_min = .0
    self.x_max = .0
    self.y_max = .0
    self.class_id = ""

  def __init__(self, dota_box: DotaBox):
    x_list = []
    y_list = []

    for idx in range(0, 4):
      x_list.append(dota_box.points[idx].x)
      y_list.append(dota_box.points[idx].y)

    self.x_min = min(x_list)
    self.y_min = min(y_list)
    self.x_max = max(x_list)
    self.y_max = max(y_list)
    self.class_id = dota_box.category

  def to_string(self):
    return "{} {} {} {} {}".format(self.x_min, self.y_min, self.x_max, self.y_max, self.class_id)


def convert_dota2yolov3(dota_path, out_path):
  dataset_paths = [f for f in listdir(dota_path) if isfile(join(dota_path, f))]
  for dataset_path in dataset_paths:
    dota_boxes = []
    # read
    try:
      with open(os.path.join(dota_path, dataset_path), "r") as f:
        f.readline()
        f.readline()
        for line in f.readlines():
          dota_boxes.append(DotaBox(line.split(" ")))
    except Exception as e:
      print(
        "DOTA dataset(file_name={}) is not suitable. Error is [{}]".format(os.path.join(dota_path, dataset_path), e))
      continue

    # write
    os.makedirs(out_path, exist_ok=True)
    try:
      with open(os.path.join(out_path, dataset_path), "w") as f:
        for dota_box in dota_boxes:
          f.write(YoloBox(dota_box).to_string() + '\n')
    except Exception as e:
      print("Fail to save file as .txt. Error is [{}]".format(e))
      continue


def main():
  print("arg : {}, {}, {}".format(FLAGS.dota_path, FLAGS.out_path, FLAGS.difficult))
  convert_dota2yolov3(FLAGS.dota_path, FLAGS.out_path)


if __name__ == '__main__':
  # class YOLO defines the default value, so suppress any default here
  parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
  '''
  Command line positional arguments -- for video detection mode
  '''

  parser.add_argument(
    "--no_difficult", dest='difficult', action='store_false',
    help="[Optional] Exclude difficulty objects"
  )

  parser.add_argument(
    "--difficult", dest='difficult', action='store_true',
    help="[Default] Include difficulty objects"
  )

  parser.add_argument(
    "--dota_path", nargs='?', type=str, required=False, default='dota',
    help="DOTA labels' dir path. Default is './dota'"
  )

  parser.add_argument(
    "--out_path", nargs='?', type=str, required=False, default='yolo',
    help="Directory where the coverted data will be stored. Default is './yolo'"
  )

  parser.set_defaults(difficult=True)
  FLAGS = parser.parse_args()

  main()
# read_dota(FLAGS.dota_path, FLAGS.no_difficult)
