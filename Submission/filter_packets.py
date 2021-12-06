def filter(path):

    # read raw bytes from file into byte_array
    filepath = path
    if not (path.endswith(".pcap")):
        print("Error: File path '" + path + "' not .pcap format")
        return
    byte_array = []
    with open(filepath, "rb") as myFile:
        bytes = myFile.read(1)
        while bytes:
            byte_array.append(bytes.hex())
            bytes = myFile.read(1)
    
    i = 0 # current byte we are looking at in byte_array
    write_bytes = []
    while i < 24: #get global header
        write_bytes.append(byte_array[i])
        i += 1
    
    count = 0 # total printed packets
    tot_count = 0 # total parsed packets
    ip_count = 0
    icmp_count = 0
    ping_count = 0
    
    while i < len(byte_array): # read until EOF
        tot_count += 1
        pkt_bytes = 8 # how many bytes have been read from this packet, starting at 8 for pcap header
        # getting total packet length
        pkt_size = int("".join(reversed(["".join(byte_array[i+pkt_bytes:i+pkt_bytes+4]).split(" ")[0][j:j+2] for j in range(0,8,2)])), 16)
        pkt_bytes = 12
        pkt_size = int("".join(reversed(["".join(byte_array[i+pkt_bytes:i+pkt_bytes+4]).split(" ")[0][j:j+2] for j in range(0,8,2)])), 16)
        
        pkt_bytes += 16 # skip MAC addresses, get to packet type
        type_hex = byte_array[i+pkt_bytes] + byte_array[i+pkt_bytes+1]
        if type_hex == '0800': # IP packet found
            ip_count += 1
            # skip to protocol field
            pkt_bytes += 11
            protocol = int(byte_array[i + pkt_bytes], 16)
            if protocol is 1: # ICMP packet found
                icmp_count += 1
                pkt_bytes += 11
                icmp_type = int(byte_array[i + pkt_bytes], 16)
                if icmp_type is 0 or icmp_type is 8: # echo message found
                    ping_count += 1
                    for b in range(i, i+pkt_size+16):
                        # output to file to be parsed
                        write_bytes.append(byte_array[b])
        i += pkt_size + 16
            
    print("Wrote to " + path[path.rfind("/")+1:-5] + "_filtered.pcap:\t" + str(tot_count) + " packets parsed, "+ str(ping_count) + "/" + str(icmp_count) + "/" + str(ip_count) + " Ping/ICMP/IP packets")
    f = open(path[path.rfind("/")+1:-5] + "_filtered.pcap", "wb")
    for b in write_bytes:
        f.write(bytes.fromhex(b))
    f.close()
