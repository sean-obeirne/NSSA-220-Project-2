import sys
def to_bin(string):
    bits = bin(int(string,16))[2:]
    for i in range(len(bits),8):
        bits = "0" + bits
    return bits

def parse(file) :
    print('called parse function in packet_parser.py')
    check = "08"
    check2 = "00"
    check3 = "45"
    metrics_arr = []
    byte_array = []
    with open(file, 'rb') as myFile:
        byte = myFile.read(1)
        while byte:
            byte_array.append(byte.hex())
            byte = myFile.read(1)
    i = 24 # skip file header
    print("byte_array length: " + str(len(byte_array)))
    while i < len(byte_array):
        print("this index: " + str(i))
        metrics = [0,0,0,0,0,0] 
        # metrics:
        #   0 - timestamp
        #   1 - src ip
        #   2 - dest ip
        #   3 - bytes of entire frame
        #   4 - 
        #   5 - echo req / rep
        #   6 - 
        #   7 - 

        # get seconds of epoch time
        ts = int(byte_array[i+3] + byte_array[i+2] + byte_array[i+1] + byte_array[i], 16)
        i += 4
        # get milliseconds of epoch time
        tms = int(byte_array[i+3] + byte_array[i+2] + byte_array[i+1] + byte_array[i], 16)
        i += 4
        # combine and save timestamp
        timestamp = str(ts) + "." + str(tms)
        metrics[0] = timestamp

        pkt_len = int(byte_array[i+3] + byte_array[i+2] + byte_array[i+1] + byte_array[i], 16)
        metrics[3] = pkt_len
        
        i += 8 # get past pcap header

        i += 14 # get past ethernet header

        # get source and destination ip
        i += 12 # get past useless part of IP header
        src_ip = byte_array[i] + byte_array[i+1] + byte_array[i+2] + byte_array[i+3]
        i += 4
        dest_ip = byte_array[i] + byte_array[i+1] + byte_array[i+2] + byte_array[i+3]
        i += 4
        metrics[1] = src_ip
        metrics[2] = dest_ip


        i += (pkt_len - 34)



        print("this timestamp: " + str(metrics[0]))
        print("this source ip: " + str(metrics[1]))
        print("this dest ip: " + str(metrics[2]))
        print("this packet size: " + str(metrics[3]))
        metrics_arr.append(metrics)


"""
    for index, chunk in enumerate(byte_array):
        if check in chunk and index < len(byte_array) and check2 in byte_array[index + 1] and check3 in byte_array[index + 2]:
            metrics[3] = str(byte_array[index + 4]) + str(byte_array[index + 5])
            metrics[4] = str(byte_array[index + 10])
            metrics[5] = str(byte_array[index + 22])
            metrics_arr.append(metrics)
    return metrics_arr
"""
