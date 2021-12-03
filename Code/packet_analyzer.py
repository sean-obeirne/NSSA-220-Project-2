from filter_packets import *
from packet_parser import *
from compute_metrics import *

for i in range(1, len(sys.argv)):
    filename = sys.argv[i]
    filter(filename)
    parsed_list = parse("Node" + str(i) + "_filtered.pcap")
    compute(parsed_list, i)
