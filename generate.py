import csv

# result=[]
# with open('data.csv', 'r') as reader:
#     csv_reader=reader.read()
#     csv_reader.append(result)
# print(result)
    

data_read=[]
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for read in csv_reader:
        data_read.append(read)



data_read_result=[]
for i in range(0, len(data_read), 2):
    data_read_result.append(data_read[i])

real_data=data_read_result[0]

for data in data_read_result:
    print(data[0])


# for data in data_read:
#         print(data)

# print(data_read)


# with open('data.txt', 'r') as reader:
#     print(reader.readline())