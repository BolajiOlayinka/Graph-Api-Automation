# import csv

# data_read=[]
# with open('data.csv', newline='') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     for read in csv_reader:
#         data_read.append(read)
#         print(data_read)



with open('data.txt', 'r') as reader:
    print(reader.readline())