#from filter_packets import *
from packet_parser import *
from compute_metrics import *
filename = sys.argv[1]
list = parse(filename)
#filter()
compute(list)
#print(list)
