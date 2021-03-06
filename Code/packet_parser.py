import sys

def parse(file) :
    metrics_arr = []
    byte_array = []

    # read filtered pcap
    with open(file, 'rb') as pcap_file:
        byte = pcap_file.read(1)
        while byte:
            byte_array.append(byte.hex())
            byte = pcap_file.read(1)

    i = 24 # skip file header

    while i < len(byte_array):

        metrics = [0,0,0,0,0,0,0] 
        # metrics:
        #   0 - timestamp seconds
        #   1 - timestamp milliseconds
        #   2 - bytes of entire frame (from pcap record header)
        #   3 - IP TTL
        #   4 - source ip
        #   5 - destination ip
        #   6 - ICMP type

        # get seconds of epoch time
        ts = byte_array[i+3] + byte_array[i+2] + byte_array[i+1] + byte_array[i]
        metrics[0] = ts
        i += 4

        # get milliseconds of epoch time
        tms = byte_array[i+3] + byte_array[i+2] + byte_array[i+1] + byte_array[i]
        metrics[1] = tms
        i += 4

        # get frame size
        pkt_len = byte_array[i+3] + byte_array[i+2] + byte_array[i+1] + byte_array[i]
        metrics[2] = pkt_len
        
        i += 8 # get past pcap header

        i += 14 # get past ethernet header

        i += 8 # get past useless part of IP header

        # get TTL
        ttl = byte_array[i]
        metrics[3] = ttl
        i += 4 # get past protocol and checksum in IP header

        # get source and destination ip
        src_ip = byte_array[i] + byte_array[i+1] + byte_array[i+2] + byte_array[i+3]
        metrics[4] = src_ip
        i += 4
        dest_ip = byte_array[i] + byte_array[i+1] + byte_array[i+2] + byte_array[i+3]
        metrics[5] = dest_ip
        i += 4

        # get icmp type
        icmp_type = byte_array[i]
        metrics[6] = icmp_type
        i += 8 # get past icmp header


        i += (int(pkt_len,16) - 42) # get past icmp payload onto next packet


        metrics_arr.append(metrics)

    return metrics_arr
