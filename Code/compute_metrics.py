def compute(list, node):
   replies_sent = 0
   bytes = 0
   rtt = 0
   rttavg = 0
   req_bytes_sent = 0
   req_bytes_rec = 0
   req_sent = 0
   req_rec = 0
   rep_sent = 0
   rep_rec = 0
   num = 0
   ip = 0
   echo req = 45 63 68 6f 20 28 70 69 6e 67 29 20 72 65 71 75 65 73 74
   if node == 1:
      ip = 31 39 32 2e 31 36 38 2e 31 30 30 2e 31
   elif node == 2:
      ip = 31 39 32 2e 31 36 38 2e 31 30 30 2e 32
   elif node == 3:
      ip = 31 39 32 2e 31 36 38 2e 32 30 30 2e 31
   else:
      ip = 31 39 32 2e 31 36 38 2e 32 30 30 2e 32
   for z in list:
      if ip in z[1]:
         if echo req in z[4]:
            req_sent += 1
            req_bytes_sent += hex(z[3])
         else: 
            rep_sent += 1
            rtt += hex(z[0]) - hex(list[z-1][0])
      else:
         if echo req in z[4]:
            req_rec +=1
            req_bytes_rec += hex(z[3])
         else:
            rep_rec += 1
            rtt += hex(z[0]) - hex(list[z-1][0])
   rttavg = rtt / len(list)
   print("Requests sent: " + str(requests_sent))
   print("Request Recieved: " + str(requests_rec))
   print("Replies Sent: " + str(replies_sent))
   print("Replies Recieved: " + str(replies_rec))
   print("Echo Request Bytes Sent: " + str(req_sent))
   print("Echo Request Bytes Received: " + str(rep_rec))
   print("Echo Request Data Sent: " + str())
   print("Echo Request Data Recieved: " + str())
   print("Average RTT (ms): " + str(rttavg))
   print("Echo Request Throughput (kB/sec): " + str())
   print("Echo Request Goodput (kB/sec): " + str())
   print("Average Reply Delay (us): " + str())
   print("Average Echo Request Hop Count: " + str())
