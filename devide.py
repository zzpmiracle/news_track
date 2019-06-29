import csv
import numpy
data_dir = 'D:news_track'
with open('data.txt') as f,open(data_dir+'//train.csv','w',newline ='') as train_file,open(data_dir+'//dev.csv','w',newline='') as dev_file:
    reader = csv.reader(f,delimiter=',')
    lines = []
    for line in reader:
        lines.append(line)
    length = len(lines)
    numpy.random.shuffle(lines)

    train_len = int(0.8 * length)
    training, dev = lines[:train_len], lines[train_len:]

    train_writer = csv.writer(train_file)
    train_writer.writerows(training)
    dev_writer = csv.writer(dev_file)
    dev_writer.writerows(dev)
