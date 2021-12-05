def compute(metrics, node):
   replies_sent = 0
   bytes = 0
   rtt = 1
   rttavg = 0
   req_bytes_sent = 0
   req_bytes_rec = 0
   req_sent = 0
   req_rec = 0
   rep_sent = 0
   rep_rec = 0
   num = 0
   ip = 0
   iteration = 0
   echo_req = "08"
   if node == 1:
      ip = "c0a86401"
   elif node == 2:
      ip = "c0a86402"
   elif node == 3:
      ip = "c0a8c801"
   else:
      ip = "c0a8c802"
   for z in metrics:
      iteration += 1
      if ip in str(z[4]):
         if echo_req in z[6]:
            req_sent += 1
            req_bytes_sent += int(z[2], 16)
         else: 
            rep_sent += 1
            #rtt = (int(z[0], 16) - int(metrics[z-1][0], 16))
      else:
         if echo_req in z[6]:
            req_rec +=1
            req_bytes_rec += int(z[2], 16)
         else:
            rep_rec += 1
            #rtt += int(z[0]) - int(metrics[z-1][0])
   rttavg = rtt / len(metrics)
   print("Requests sent: " + str(req_sent))
   print("Request Recieved: " + str(req_rec))
   print("Replies Sent: " + str(rep_sent))
   print("Replies Recieved: " + str(rep_rec))
   print("Echo Request Bytes Sent: " + str(req_bytes_sent))
   print("Echo Request Bytes Received: " + str(req_bytes_rec))
   print("Echo Request Data Sent: " + str(req_bytes_sent - (42 * req_sent)))
   print("Echo Request Data Recieved: " + str(req_bytes_rec - (42 * req_rec)))
   print("Average RTT (ms): " + str(rttavg))
   print("Echo Request Throughput (kB/sec): " + str(req_bytes_sent / rtt))
   print("Echo Request Goodput (kB/sec): " + str(req_bytes_rec / rtt))
   print("Average Reply Delay (us): " + str())
   print("Average Echo Request Hop Count: " + str())
