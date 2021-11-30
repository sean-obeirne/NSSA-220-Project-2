import sys
def parse() :
   print('called parse function in packet_parser.py')
   file_name= sys.argv[1]
   f = open(file_name, 'r')
   line_check = "Protocol Length Info"
   lines = f.readlines()
   metrics_arr = []
   x=0
   final_list = []
   for index, line in enumerate(lines):
      metrics = []  
      metrics_fmt = []
      if line_check in line:
         x = index + 1
         metrics = lines[x].split(" ")
         for y in metrics:
            if not y:
               pass
            else:
               metrics_fmt.append(y)
         metrics_arr.append(metrics_fmt)
      else:
         pass
   for a in metrics_arr:
      if len(a) > 7:
         while 7 < len(a):
            a[6] += " " + a[7]
            a.remove(a[7])

