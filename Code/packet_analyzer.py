from filter_packets import *
from packet_parser import *
from compute_metrics import *

for i in range(1, len(sys.argv)):
    filename = sys.argv[i]
    #list = parse(filename)
    filter(filename)
    #compute(list)
