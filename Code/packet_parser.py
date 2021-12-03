import sys
def parse(file) :
   print('called parse function in packet_parser.py')
   check = "08"
   check2 = "00"
   check3 = "45"
   metrics_arr = []
   bytes_array = []
   with open(file, 'rb') as myFile:
      bytes = myFile.read(1)
      while bytes:
         bytes_array.append(bytes.hex())
         bytes = myFile.read(1)
   for index, chunk in enumerate(bytes_array):
      metrics = [0,0,0,0,0,0]  
      if check in chunk and index < len(bytes_array) and check2 in bytes_array[index + 1] and check3 in bytes_array[index + 2]:
            metrics[0] = str("test")
            metrics[1] = str(bytes_array[index + 14]) + str(bytes_array[index + 15]) + str(bytes_array[index + 16]) + str(bytes_array[index + 17])
            metrics[2] = str(bytes_array[index + 18]) + str(bytes_array[index + 19]) + str(bytes_array[index + 20]) + str(bytes_array[index + 21])
            metrics[3] = str(bytes_array[index + 4]) + str(bytes_array[index + 5])
            metrics[4] = str(bytes_array[index + 10])
            metrics[5] = str(bytes_array[index + 22])
            metrics_arr.append(metrics)
   return metrics_arr
