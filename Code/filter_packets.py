def filter(path):
    print('called filter function in filter_packets.py')

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
    i = 40 #the first 16 bytes are the pcap header for the first packet, we're skipping that
    
    count = 0 # total printed packets
    tot_count = 0 # total parsed packets
    ip_count = 0
    icmp_count = 0
    ping_count = 0
    #print(str(len(byte_array)))
    
    while i < len(byte_array): # read until EOF
        tot_count += 1
        pkt_start = i
        pkt_bytes = 0 # how many bytes have been read from this packet
        icmp_type = 20
        #
        # Parse ethernet header
        #
        
        # skip MAC addresses, get to packet type
        i += 12
        pkt_bytes += 12
        type_hex = byte_array[i] + byte_array[i+1]
        if type_hex == '0800':
            #print("IP packet found, byte " + str(pkt_start))
            ip_count += 1
            # get to beginning of IP header / IP version
            i += 2
            pkt_bytes += 2
            ip_bytes = 0 #count to see how many bytes we've processed in the IP header
            #if byte_array[i] == '45': ##i don't think this is necessary anymore? - mani
            #   print("is ipv4")
            i += 2 # move on to IP packet size (skip differentiated services field)
            pkt_bytes += 2
            ip_bytes += 2
            ip_size = int(byte_array[i] + byte_array[i+1], 16)
            i += 7 # move on to protocol number (skip ip identification, ip flags, & TTL)
            ip_bytes += 7
            pkt_bytes += 7
            protocol = int(byte_array[i], 16)
            if protocol is 1:
                #print("ICMP packet found, byte " + str(pkt_start))
                icmp_count += 1
                i += 11
                ip_bytes += 11
                pkt_bytes += 11
                #print(str(i))
                icmp_type = int(byte_array[i], 16)
                if icmp_type is 0 or icmp_type is 8:
                    ping_count += 1
                    for b in range(pkt_start - 16, pkt_start+ip_size+14): #the preceding 16 bytes of each packet is a .pcap header, but we only need them for icmp packets
                        # output byte_array[i] to file to be parsed
                        write_bytes.append(byte_array[b])
            i += (ip_size - ip_bytes)
        #
        # Non-IP Catchers B)
        #
        elif type_hex == '9000':
            #print("Non-IP packet found, byte " + str(i))
            i += 48
            #print(str(i))
        elif type_hex == '0806':
            #print("ARP packet found, byte " + str(i))
            i += 8
            pkt_bytes += 8
            arp_type = int(byte_array[i] + byte_array[i+1], 16)
            if arp_type is 1:
                i += 22
            elif arp_type is 2:
                i += 40
                #print(str(i) + " - type " + str(arp_type))
        elif type_hex == '6002':
            #print("Remote Control packet found, byte " + str(i))
            i += 65
            #print(str(i))
        elif type_hex == '88cc':
            #print("Special packet found, byte " + str(i))
            i += 46
            #print(str(i))
        else:
            pkt_size = int(byte_array[i] + byte_array[i+1], 16)
            #print("Non-IP packet found, byte " + str(i))
            if pkt_size < 46:
                pkt_size += 46 - pkt_size
            i += pkt_size + 2
            #print(str(i))
        i += 16 #there's 16 bytes in between each packet
            
    print("Wrote to " + path[path.rfind("/")+1:-5] + "_filtered.pcap:\t" + str(tot_count) + " packets parsed, "+ str(ping_count) + "/" + str(icmp_count) + "/" + str(ip_count) + " Ping/ICMP/IP packets")
    f = open(path[path.rfind("/")+1:-5] + "_filtered.pcap", "wb")
    for b in write_bytes:
        f.write(bytes.fromhex(b))
    f.close()
