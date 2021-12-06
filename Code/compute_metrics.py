# need this function to left-pad millisecond data with zeros (sometimes)
# needed when millisecond number is small
# otherwise decimal places are off during rtt calculation (subtraction)
def hex_to_timestamp(hexsecs, hexmils):
    seconds = str(int(hexsecs, 16))
    milliseconds = str(int(hexmils, 16))
    while len(milliseconds) < 6: # max millisecond hex string has 6 characters
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
#
# Initialize Variables
#
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
    f = open("NodeStats.csv", "a")
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
        return

#
# Calculate Data from Metrics
#
    for z in metrics:
        timestamps.append(hex_to_timestamp(z[0], z[1]))

        if ip in str(z[4]):
            if echo_req in z[6]: # we sent an echo request
                req_sent += 1
                req_bytes_sent += int(z[2], 16)
            else: # we sent an echo reply 
                rep_sent += 1
                reply_delay += (timestamps[i] - timestamps[i-1])

        else:
            if echo_req in z[6]: # we received an echo request
                req_rec +=1
                req_bytes_rec += int(z[2], 16)
            else: # we received an echo reply
                rep_rec += 1
                rtt += timestamps[i] - timestamps[i-1]
                ttl += int(metrics[i-1][3], 16) - int(z[3], 16) + 1

        i += 1

#
# Output Data
#
    req_data_sent = req_bytes_sent - (42 * req_sent)
    req_data_rec = req_bytes_rec - (42 * req_rec)
    rttavg = round((1000 * rtt) / rep_rec, 2)
    avg_reply_delay = round((1000000 * reply_delay) / rep_sent, 2)
    avg_ttl = round(ttl / rep_rec, 2)
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
    print("Average Echo Request Hop Count: " + str(avg_ttl))
    f.write("Node " + str(node) + "\n\n")
    f.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received \n")
    f.write(str(req_sent) + "," + str(req_rec) + "," + str(rep_sent) + "," + str(rep_rec) + "\n")
    f.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes) \n")
    f.write(str(req_bytes_sent) + "," + str(req_data_sent) + "\n")
    f.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes) \n")
    f.write(str(req_bytes_rec) + "," + str(req_data_rec) + "\n\n")
    f.write("Average RTT (milliseconds)," + str(rttavg) + "\n")
    f.write("Echo Request Throughput (kB/sec)," + str(round((req_bytes_sent/1000)/rtt, 1) ) + "\n")
    f.write("Echo Request Goodput (kB/sec)," + str(round((req_data_sent /1000) / rtt, 1) ) + "\n")
    f.write("Average Reply Delay (microseconds)," + str(avg_reply_delay) + "\n")
    f.write("Average Echo Request Hop Count," + str(avg_ttl) + "\n")
    f.write("\n")
 
