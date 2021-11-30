def compute():
   replies_sent = 0
   bytes = 0
   rtt = 0
   rttavg = 0
   requests_sent = 0
   requests_rec = 0
   replies_rec = 0
   for z in list:
      if z[2] == "192.168.100.1":
         if "Echo (ping) reply" in z[6]:
            replies_sent += 1
         if "Echo (ping) request" in z[6]:
            requests_sent += 1
      if z[3] == "192.168.100.1":
         if "Echo (ping) reply" in z[6]:
            replies_rec += 1
         if "Echo (ping) request" in z[6]:
            requests_rec += 1

      bytes += float(z[5])
      rtt += float(z[1])
   rttavg = rtt / 1501
   print("Requests sent: " + str(requests_sent))
   print("Request Recieved: " + str(requests_rec))
   print("Replies Sent: " + str(replies_sent))
   print("Replies Recieved: " + str(replies_rec))
   print(bytes)
   print(rttavg)
parse()
