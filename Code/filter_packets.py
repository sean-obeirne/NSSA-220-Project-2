import sys

def filter():
    print('called filter function in filter_packets.py')

    # read raw bytes from file into byte_array
    filepath = sys.argv[1]
    byte_array = []
    with open(filepath, "rb") as myFile:
        bytes = myFile.read(1)
        while bytes:
            byte_array.append(bytes.hex())
            bytes = myFile.read(1)
    
    i = 0 # current byte we are looking at in byte_array

    # get past global header
    i = 40

    count = 0 # total printed packets
    tot_count = 0 # total parsed packets
    # parse one packet
    while i < len(byte_array): # read until EOF
        tot_count += 1

        pkt_bytes = 0 # how many bytes have been read from this packet

        #
        # Parse ethernet header
        #
        
        # skip MAC addresses, get to packet type
        i += 12
        pkt_bytes += 12

        type_hex = byte_array[i] + byte_array[i+1]
        if type_hex == '0800':
            type_byte = 'IP'
            print("IP packet found")
        else:
            type_byte = 'UNRECOGNIZED ETHERNET TYPE'

        # get to beginning of IP header / IP version
        i += 2
        pkt_bytes += 2


        #
        # Parse IP header
        #
        
        ip_bytes = 0 # count to see how many bytes we've processed in the IP header

        if byte_array[i][0] == '4':
            version = '4' # IPv4
        else:
            version = 'ERROR'
        if byte_array[i][1] == '5':
            header_len = '20'
        else:
            header_len = 'ERROR' # invalid IP header length
        i += 2 # move on to IP packet size (skip differentiated services field)
        pkt_bytes += 2
        ip_bytes += 2

        ip_size = int(byte_array[i] + byte_array[i+1], 16)
        i += 7 # move on to protocol number (skip ip identification, ip flags, & TTL)
        ip_bytes += 7
        pkt_bytes += 7

        protocol = int(byte_array[i], 16)
        if protocol is 1:
            protocol_str = 'ICMP'
            print("ICMP packet found!")
        else:
            i += (ip_size - ip_bytes)
            continue # invalid protocol, process next packet

        for b in range(0,ip_size-ip_bytes): # loop to end of packet
            # output byte_array[i] to file to be parsed
            i += 1
