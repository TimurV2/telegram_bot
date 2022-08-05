from csv import writer

# The data assigned to the list 
list_data = ['123', 'S123h', 'Sci123e']

with open('CSVFILE.csv', 'a', newline='') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(list_data)
    f_object.close()