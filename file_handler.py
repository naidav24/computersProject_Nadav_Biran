#check if the file is in rows or columns
def check_file_type(file_in_string_format):
    file_in_array = file_in_string_format.split()
    #this could be obviously be done much easier using string manipulation
    #but this way is cooler.
    #we check if the characters are numbers in the relevant spots
    #to see if the file is in rows or in columns
    try:
        temp = int(file_in_array[1])
        file_type = "row"
    except(ValueError):
        file_type = "column"
    return(file_type)

#open the file and read it
def extract_data(filename):
    data_file = open(filename, 'r')
    file_in_string_format = data_file.read()
    return(manage_file(file_in_string_format))

#turn the raw data into an handleable array
def manage_file(file_in_string_format):
    file_type=check_file_type(file_in_string_format)
    data = [["x"],["y"],["dx"],["dy"]]
    #for a file in columns
    if file_type=="column":
        #split the file to columns and find their titles
        file_in_columns=file_in_string_format.split("\n")
        column_titles=file_in_columns[0].split()
        #keep only numeral data
        file_in_columns=file_in_columns[1:-3]
        #arrange the array
        temp_data= [["x"],["y"],["dx"],["dy"]] 
        for row in file_in_columns:
            #turn the row into a list of floats
            row=row.split()
            row=list(map(float, row))
            #match each number in the row to the relevant parameter (x,dx,y,dy)
            for i in range(len(row)):
                title_index=temp_data.index([column_titles[i].lower()])
                data[title_index].append(row[i])
    #for a file in rows
    elif file_type=="row":
        #split into rows
        file_in_rows=file_in_string_format.split("\n")
        for i in range(0,4):
            #turn the rows into lists
            file_in_rows[i]=file_in_rows[i].split(" ")
            #find the title of each row
            title=file_in_rows[i][0]
            title_index=data.index([title.lower()])
            #remove the row title from the row list
            file_in_rows[i]=file_in_rows[i][1:]
            #turn numbers from strings to float
            file_in_rows[i]=list(map(float, file_in_rows[i]))
            #add information to the right index in data array
            data[title_index].extend(file_in_rows[i])
    #remove titles and sort according to x
    for item in (data):
        temp=item.pop(0)
    #sort the measurements according to their x value
    for i in range(1,4):
        new_x, data[i]=zip(*sorted(zip(data[0],data[i])))
        new_x=list(new_x)
        data[i]=list(data[i])
    data[0]=new_x
    #locate axis names
    relevant_file=file_in_string_format.split("\n")
    relevant_file=relevant_file[-3:-1]
    relevant_file[0]=relevant_file[0].split(": ")[1]
    relevant_file[1]=relevant_file[1].split(": ")[1]
    return([data,relevant_file])

#check the validity of the data according to the error types given
def check_data_validity(data):
    data_list_length=[]
    #check for the error of x, y, dx, or dy being in different lengths
    for i in range(0,4):
        data_list_length.append(len(data[i]))
    if data_list_length.count(len(data[0]))!=4:
        return("Length Error")
    #check for invalid uncertainty values
    for i in range(2,4):
        for uncert in data[i]:
            if uncert<=0:
                return("Uncert Error")
    return("Valid")
