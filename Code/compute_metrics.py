def compute(list):
   replies_sent = 0
   bytes = 0
   rtt = 0
   rttavg = 0
   requests_sent = 0
   requests_rec = 0
   replies_rec = 0
   req_sent = 0
   req_rec = 0
   rep_sent = 0
   rep_rec = 0
   num = 0
   for z in list:
      num += 1
      if z[2] == "192.168.100.1":
         if "Echo (ping) reply" in z[6]:
            replies_sent += 1
            rep_sent += float(z[5])
         if "Echo (ping) request" in z[6]:
            requests_sent += 1
            req_sent += float(z[5])
      if z[3] == "192.168.100.1":
         if "Echo (ping) reply" in z[6]:
            replies_rec += 1
            rep_rec += float(z[5])
         if "Echo (ping) request" in z[6]:
            requests_rec += 1
            req_rec += float(z[5])

      bytes += float(z[5])
      rtt += float(z[1])
   rttavg = 1510 / num
   print("Requests sent: " + str(requests_sent))
   print("Request Recieved: " + str(requests_rec))
   print("Replies Sent: " + str(replies_sent))
   print("Replies Recieved: " + str(replies_rec))
   print(bytes)
   print(rttavg)
   print("Echo Request Bytes Sent: " + str(req_sent))
   print("Echo Request Bytes Received: " + str(rep_rec))
   print("Echo Request Data Sent: " + str(rep_sent))
   print("Echo Request Data Recieved: " + str(req_rec))

