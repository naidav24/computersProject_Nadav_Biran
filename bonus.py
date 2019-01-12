import file_handler
import calculations
import numpy as np

#manage the opening and rendering of the input file into a usable array
def bonus_manage_file(filename):
    #open the input file
    data_file = open(filename, 'r')
    file_in_string_format = data_file.read()
    #seperate the maesurements from the information about the ranges
    #for a and b
    seperation_index=file_in_string_format.find("\na ")
    measurements=file_in_string_format[:seperation_index]
    a_b_info=file_in_string_format[(seperation_index+1):]
    [bonus_data, bonus_axis_titles]=file_handler.manage_file(measurements)
    #arrange the information about a and b
    a_b_info=a_b_info.split("\n")
    a_b_info=a_b_info[:-1]
    return([bonus_data, bonus_axis_titles,a_b_info])

#find the values of a and b that result in the minimal chi2 value
def find_a_and_b(bonus_data, bonus_axis_titles, a_b_info):
    #eliminate the strings "a" and "b" from the information about a and b
    #and turn them into a useful list
    a_data=a_b_info[0].split()[1:]
    b_data=a_b_info[1].split()[1:]
    #turn a and b lists into lists of floats instead of strings
    a_data=list(map(float,a_data))
    b_data=list(map(float,b_data))
    #check all relevant a and b values for the minimal chi2
    current_chi=0
    a_min=0
    b_min=0
    for a in list(np.arange(a_data[0],a_data[1],a_data[2])):
        for b in list(np.arange(b_data[0], b_data[1],b_data[2])):
            temp_chi=calculations.chi_square_calcs(bonus_data,a,b)[0]
            #set a first value for chi2 to be equated to
            if ((a==a_data[0]) and (b==b_data[0])):
               a_min=a
               b_min=b
               current_chi=temp_chi
            #check if the chi2 for current a and b is lower than the current
            #minimal chi2
            elif current_chi>=temp_chi:
                current_chi=temp_chi
                a_min=a
                b_min=b
    #calculate chi2reduced
    chi_reduced=calculations.chi_square_calcs(bonus_data,a_min,b_min)[1]
    return([a_min, b_min,abs(a_data[2]), abs(b_data[2]), current_chi, chi_reduced, a_data])
