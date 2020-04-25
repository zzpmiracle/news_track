import csv
import numpy
data_dir = 'G:news_track//'
def train_and_eval():
    with open(data_dir+'data.txt') as f,open(data_dir+'train.csv','w',newline ='') as train_file,open(data_dir+'dev.csv','w',newline='') as dev_file:
        reader = csv.reader(f,delimiter=',')
        lines = []
        for line in reader:
            lines.append(line)
        length = len(lines)
        numpy.random.shuffle(lines)

        train_len = int(0.8 * length)
        # dev_len = int(0.2 * length)
        training, dev = lines[:train_len], lines[train_len:]

        train_writer = csv.writer(train_file)
        train_writer.writerows(training)
        dev_writer = csv.writer(dev_file)
        dev_writer.writerows(dev)
def test():
    with open(data_dir+'//test.csv','w',newline ='') as test_file:
        lines = [['00f57310e5c8ec7833d6756ba637332e','9171debc316e5e2782e0d2404ca7d09d']]
        test_writer = csv.writer(test_file)
        test_writer.writerows(lines)

train_and_eval()