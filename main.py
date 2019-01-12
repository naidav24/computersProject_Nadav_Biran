import file_handler
import sys
import calculations
import matplotlib.pyplot as plt
import bonus
import numpy as np

#the main function for the main project
def fit_linear(filename):
    [data_table,axis_titles] = file_handler.extract_data(filename)
    #check the validity of the input file and stop the program if invalid
    validity_status=file_handler.check_data_validity(data_table)
    if validity_status=="Length Error":
        print("Input file error: Data lists are not the same length.")
        sys.exit(0)
    if validity_status=="Uncert Error":
        print("Input file error: Not all uncertainties are positive.")
        sys.exit(0)
    #calculate the a and the b of the linear function
    a = calculations.minimum_a(data_table)
    b = calculations.minimum_b(data_table, a)
    [da_square, db_square] = calculations.da_db_square(data_table)
    da = da_square ** (1 / 2.0)
    db = db_square ** (1 / 2.0)
    #calculate chi2 and chi2reduced
    [chi_square, chi_reduced] = calculations.chi_square_calcs(data_table, a, b)
    result_print(a,b,da,db,chi_square,chi_reduced)
    plot_create(data_table,axis_titles,a,b)

#The main function of the Bonus
def search_best_parameter(filename):
    [bonus_data, bonus_axis_titles, a_b_info]=bonus.bonus_manage_file(filename)
    [a_min, b_min,da, db, chi_square, chi_reduced,a_data]=bonus.find_a_and_b(bonus_data, bonus_axis_titles, a_b_info)
    result_print(a_min, b_min,da, db, chi_square, chi_reduced)
    bonus_plot_create(b_min, a_data,bonus_data)
    plot_create(bonus_data, bonus_axis_titles, a_min,b_min)

#print the results in the required format
def result_print(a,b,da,db,chi_square,chi_reduced):
    print("a=", a, "+-", da)
    print("b=", b, "+-", db)
    print("chi2=", chi_square)
    print("chi2_reduced=", chi_reduced)

#create the plot for the main project
def plot_create(data_table,axis_titles,a,b):
    plt.axis([min(data_table[0]) - 2, max(data_table[0]) + 2, min(data_table[1]) - 2, max(data_table[1]) + 2])
    #create and plot the linear function
    lin_fun = list(map((a).__mul__, data_table[0]))
    lin_fun = list(map((b).__add__, lin_fun))
    plt.plot(data_table[0], lin_fun, 'r-')
    #set the measurements in the polt
    plt.errorbar(data_table[0], data_table[1], xerr=data_table[2], yerr=data_table[3], fmt='b,')
    plt.xlabel(axis_titles[0])
    plt.ylabel(axis_titles[1])
    #save the plot
    plt.savefig("linear_fit.svg")

#create the plot for the bonus
def bonus_plot_create(b_min, a_data,bonus_data):
    #prepare the x axis data (the a's)
    a_data = list(map(float, a_data))
    a_list=list(np.arange(a_data[0], a_data[1],a_data[2]))
    a_list.sort()
    chi_list=[]
    #find the chi2 relevant to each a
    for a in a_list:
        chi_list.append(calculations.chi_square_calcs(bonus_data, a, b_min)[0])
    #create the plot
    plt.axis([a_list[0] - 2,max(a_list) + 2, min(chi_list) - 2, max(chi_list) + 2])
    plt.plot(a_list,chi_list,'b')
    plt.xlabel("a")
    temp_string="chi2(a,b = " + str(b_min) + ")"
    plt.ylabel(temp_string)
    #save the plot
    plt.savefig('numeric_sampling.svg')