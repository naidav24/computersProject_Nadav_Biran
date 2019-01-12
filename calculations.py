#calculate chi2 and chi2reduced using the formulas given for a linear function
def chi_square_calcs(data_table, a, b):
    chi=0
    N=len(data_table[0])
    #calculate chi2 by iterating on the measurements
    for i in range(0,len(data_table[0])):
        temp=data_table[1][i]-(a*(data_table[0][i])+b)
        temp=temp/(data_table[3][i])
        temp=temp**2
        chi=chi+temp
    #calculate chi2reduced
    chi_reduced=chi/(N-2)
    return([chi,chi_reduced])

#calculate the values for different paramters' "roof" values
#using the given formulas. there are temporary values used for the calculations
def calc_z_roof(data_table, z):
    temp_one=0
    temp_two=0
    for i in range(0,len(data_table[0])):
        temp_three=z[i]/((data_table[3][i])**2)
        temp_four=1/((data_table[3][i])**2)
        temp_one=temp_one+temp_three
        temp_two=temp_two+temp_four
    result=temp_one/temp_two
    return(result)

#find the value of a of the linear function that rusults in the minimal
#chi2 value, using given formula
def minimum_a(data_table):
    xy=[]
    x_square=[]
    for i in range(0,len(data_table[0])):
        xiyi=data_table[0][i]*data_table[1][i]
        xy.append(xiyi)
        xi_square=(data_table[0][i])**2
        x_square.append(xi_square)
    xy_roof=calc_z_roof(data_table,xy)
    x_square_roof=calc_z_roof(data_table,x_square)
    x_roof=calc_z_roof(data_table,data_table[0])
    y_roof=calc_z_roof(data_table,data_table[1])
    temp_one=xy_roof-x_roof*y_roof
    temp_two=x_square_roof-(x_roof)**2
    a=temp_one/temp_two
    return(a)

#find the value of b of the linear function that rusults in the minimal
#chi2 value, using given formula
def minimum_b(data_table,a):
    x_roof=calc_z_roof(data_table,data_table[0])
    y_roof=calc_z_roof(data_table,data_table[1])
    b=y_roof-a*x_roof
    return(b)

#find the value of da and db for the a and b we found to give minimal chi2
def da_db_square(data_table):
    dy_square=[]
    x_square=[]
    for i in range(0,len(data_table[0])):
        xi_square=(data_table[0][i])**2
        x_square.append(xi_square)
        dyi_square=(data_table[3][i])**2
        dy_square.append(dyi_square)
    dy_square_roof=calc_z_roof(data_table,dy_square)
    x_square_roof=calc_z_roof(data_table,x_square)
    x_roof=calc_z_roof(data_table,data_table[0])
    N=len(data_table[0])
    da_square=dy_square_roof/(N*(x_square_roof-(x_roof**2)))
    db_square=da_square*x_square_roof
    return([da_square, db_square])
