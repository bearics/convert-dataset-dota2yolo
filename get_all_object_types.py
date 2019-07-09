import os
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
  dataset_dir_path = 'dataset'
  out_path = 'all_types.txt'
  dataset_paths = [f for f in listdir(dataset_dir_path) if isfile(join(dataset_dir_path, f))]
  object_types = set()

  for dataset_path in dataset_paths:
    with open(os.path.join(dataset_dir_path, dataset_path), "r") as f:
      f.readline()
      f.readline()
      for line in f.readlines():
        object_types.add(line.split(' ')[8])


  with open(out_path, "w") as f:
    for type in object_types:
      f.write(type + "\n")