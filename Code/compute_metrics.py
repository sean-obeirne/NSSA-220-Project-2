# need this function to left-pad millisecond data with zeros when millisecond number is small
def hex_to_timestamp(hexsecs, hexmils):
    seconds = str(int(hexsecs, 16))
    milliseconds = str(int(hexmils, 16))
    while len(milliseconds) < 6:
        milliseconds = "0" + milliseconds
    return float(seconds + "." + milliseconds)
    

# metrics structure (all in hex):
#   0 - timestamp seconds
#   1 - timestamp milliseconds
#   2 - bytes of entire frame (from pcap record header)
#   3 - IP TTL
#   4 - source ip
#   5 - destination ip
#   6 - ICMP type
def compute(metrics, node):
    timestamps = list()
    ttl = 0
    rtt = 0
    reply_delay = 0
    rttavg = 0
    req_bytes_sent = 0
    req_bytes_rec = 0
    req_sent = 0
    req_rec = 0
    rep_sent = 0
    rep_rec = 0
    num = 0
    ip = 0
    i = 0
    echo_req = "08"
    if node == 1:
        ip = "c0a86401"
    elif node == 2:
        ip = "c0a86402"
    elif node == 3:
        ip = "c0a8c801"
    elif node == 4:
        ip = "c0a8c802"
    else:
        print("Error: no IP known for Node " + str(node))
        exit(1)
    for z in metrics:
        # timestamps.append(float( str(int(z[0], 16)) + "." + str(float(z[1], 16)) ))
        timestamps.append(hex_to_timestamp(z[0], z[1]))
        # print("this timestamp: " + str(timestamps[i]))
        if ip in str(z[4]):
            if echo_req in z[6]: # we sent an echo request
                req_sent += 1
                req_bytes_sent += int(z[2], 16)
            else: # we sent an echo reply 
                rep_sent += 1
                if echo_req in metrics[i-1][6] and ip in metrics[i-1][5]:
                    reply_delay += (timestamps[i] - timestamps[i-1])
                else:
                    print("WARNING: MISMATCH IN REQUEST TO REPLY, USING NEXT VALUE")
                    reply_delay += (timestamps[i] - timestamps[i-2])
                    
        else:
            if echo_req in z[6]: # we received an echo request
                req_rec +=1
                req_bytes_rec += int(z[2], 16)
            else: # we received an echo reply
                rep_rec += 1
                if echo_req in metrics[i-1][6] and ip in metrics[i-1][4]:
                    rtt += timestamps[i] - timestamps[i-1]
                    ttl += 1 
                else:
                    print("WARNING: MISMATCH IN REQUEST TO REPLY, USING NEXT VALUE")
                    rtt += timestamps[i] - timestamps[i-2]
        i += 1
    req_data_sent = req_bytes_sent - (42 * req_sent)
    req_data_rec = req_bytes_rec - (42 * req_rec)
    rttavg = round((1000 * rtt) / rep_rec, 2)
    avg_reply_delay = round((1000000 * reply_delay) / rep_sent, 2)
    print("Requests sent: " + str(req_sent))
    print("Request Recieved: " + str(req_rec))
    print("Replies Sent: " + str(rep_sent))
    print("Replies Recieved: " + str(rep_rec))
    print("Echo Request Bytes Sent: " + str(req_bytes_sent))
    print("Echo Request Bytes Received: " + str(req_bytes_rec))
    print("Echo Request Data Sent: " + str(req_data_sent))
    print("Echo Request Data Recieved: " + str(req_data_rec))
    print("Average RTT (ms): " + str(rttavg))
    print("Echo Request Throughput (kB/sec): " + str( round((req_bytes_sent/1000) / rtt, 1) ))
    print("Echo Request Goodput (kB/sec): " + str( round((req_data_sent /1000) / rtt, 1) ))
    print("Average Reply Delay (us): " + str(avg_reply_delay))
    print("Average Echo Request Hop Count: " + str())
