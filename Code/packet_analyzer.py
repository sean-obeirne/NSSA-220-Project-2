#from filter_packets import *
from packet_parser import *
from compute_metrics import *
filename = "../Captures/Node1.txt"
list = parse(filename)
#filter()
compute(list)
