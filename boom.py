
from pylab import *

def generate_naca_point(x, m, p): # The function for plotting NACA airfoil, mentioned in report)
    if x<=p and x>=0:
        return m*((2*p*x)-(x*x))/(p*p)
    elif x>p and x<=1:
        return m*(1-(2*p)+(2*p*x)-(x*x))/((1-p)*(1-p))
    else:
        return 0

def plot_naca_airfoil(m, p, num_points=1000): # Making array of x and y coordinates of the camber
    x_coords = linspace(0,1,num_points)
    y_coords = []
    for i in x_coords :
        y_coords.append(generate_naca_point(i,m,p))
    plot(x_coords,y_coords)
    #show()

def camber_line_slope(x, m, p): # Function for gradient of camber, mentioned in report
    if x < p:
        slope = 2 * m / p**2 * (p - x)
    else:
        slope = 2 * m / (1 - p)**2 * (p - x)
    return slope

def camber_slope_plot(m,p): # plot slope against x coordinate
    points = linspace(0,1,1000)
    slopes_at_points = []
    for i in points:
        slopes_at_points.append(camber_line_slope(i, m, p))
    plot(points, slopes_at_points)
    show()

def compute_A0(alpha, m, p): # Compute A0 through formula given in slides, and the fact that cos(theta)= 1-2*x
    points_integration = linspace(0,pi,101)
    val = 0
    for i in points_integration:
        x = (1-cos(i))/2
        val = val + camber_line_slope(x, m, p)*(pi/100)
    A0 = alpha - val/pi
    return A0

def compute_An(n, m, p): # Function used to code A(n) for an intergral value of n
    point_integration = linspace(0,pi,101)
    val = 0
    for i in point_integration:
        x = (1-cos(i))/2
        val = val + camber_line_slope(x, m, p)*cos(n*i)*(pi/100)
    An = 2*val/pi
    return An

def compute_Cl(alpha, m, p): # Computing Cl using the formula given in slides.
    A0 = compute_A0(alpha, m, p)
    A1 = compute_An(1, m, p)
    Cl = pi*((2*A0)+A1)
    print("Cl --> ", Cl)
    return Cl

def compute_Cm0(alpha, m, p): # Computing Cm0 using formula given in slides
    A0 = compute_A0(alpha, m, p)
    A1 = compute_An(1, m, p)
    A2 = compute_An(2, m, p)
    Cm0 = pi/2*(A0 + A1 - A2/2)
    return Cm0

def summation_for_gamma(x, n, m, p): # A function that peforms summation of small gamma
    summation = 0
    theta = arccos(1-2*x)
    for i in range (1,n):
        summation += (compute_An(i, m, p) * sin(i*theta))
        #print(summation)
    return summation

def compute_gamma(alpha, x, m, p): # Function used to calculate big gamma
    u = 30 # Free Stream velocity as per our simulations
    summation = summation_for_gamma(x, 100, m, p)
    A0 = compute_A0(alpha, m, p)
    theta = arccos(1-2*x)
    gamma = 2*u*((A0*(1+cos(theta))/sin(theta)) + summation)
    return gamma

def compute_velocity(x,y,alpha,m,p):  # Compute net velocity by adding inducted velocity vectors in the free stream velocity, by making a general FBD
    u = 30
    vel_x = 0
    vel_y = 0
    for i in linspace(0.005,0.995,100): #Ignoring the points that are too close
        yi = generate_naca_point(i,m,p)
        r = sqrt((x-i)*(x-i)+(y-yi)*(y-yi))
        v_ind = compute_gamma(alpha,i,m,p)*0.01/(2*pi*r) # FINDING INDUCED VELOCITY
        cost = (x-i)/r
        sint = (y-yi)/r
        vel_x = vel_x + v_ind*sint
        vel_y = vel_y - v_ind*cost #FINDING NET VELOCITY
    vel_x = vel_x + u*cos(alpha)
    vel_y = vel_y + u*sin(alpha) # NET VELOCITY IN TERMS OF AOA
    return [vel_x,vel_y]    #Return X and Y component of velocity

def compute_vector_plot(alpha, m, p): # Compute vector field using quiver function and calling the velocity function
    u = 30
    x_coord,y_coord = meshgrid(linspace(-1,2,20),linspace(-2,2,30))
    c,d = compute_velocity(x_coord,y_coord,alpha,m,p)
    quiver(x_coord,y_coord,c,d)
    plot_naca_airfoil(m, p)
    show()

def custom_function1_point(x): # Defining a scaled down circle with radius 0.5 and center (0.5,0)
    return 0.02*sqrt(0.25-(0.5-x)*(0.5-x))

def plot_custom_function1(): # Function to plot the custom function
    x_coords = linspace(0,1,1000)
    y_coords = []
    for i in x_coords :
        y_coords.append(0.02*sqrt(0.25-(0.5-i)*(0.5-i)))
    plot(x_coords,y_coords)
    #show()

def custom_function2_point(x): # sclaed down ellipse that is 0 at x=0 and 1, with cente at (0.5,0)
    return 0.007*sqrt(2*(0.25-((0.5-x)*(0.5-x))))

def plot_custom_function2():
    x_coords = linspace(0,1,1000)
    y_coords = []
    for i in x_coords :
        y_coords.append(0.007*sqrt(2*(0.25-((0.5-i)*(0.5-i)))))
    plot(x_coords,y_coords)
    #show()

def custom_function3_point(x): # sclaed down ellipse that is 0 at x=0 and 1, with cente at (0.5,0)
    return sqrt(0.0005*0.5*(0.25-(((0.5-x)*(0.5-x)))))

def plot_custom_function3():
    x_coords = linspace(0,1,1000)
    y_coords = []
    for i in x_coords :
        y_coords.append(sqrt(0.0005*0.5*(0.25-(((0.5-i)*(0.5-i))))))
    plot(x_coords,y_coords)
    #show()

def compute_A0_custom(alpha): # Find A0 for the corresponding custom function
    points_integration = linspace(0,pi,101)
    val = 0
    for i in points_integration:
        x = (1-cos(i))/2
        val = val + custom_function1_point(x)*(pi/100) #input the number of the custom function used
    A0 = alpha - val/pi
    return A0

def compute_An_custom(n):
    point_integration = linspace(0,pi,101)
    val = 0
    for i in point_integration:
        x = (1-cos(i))/2
        val = val + custom_function1_point(x)*cos(n*i)*(pi/100) #input the number of the custom function
    An = 2*val/pi
    return An

def compute_Cl_custom(alpha): #formula for computing the Cl of custom airfoil
    A0 = compute_A0_custom(alpha)
    A1 = compute_An_custom(1)
    Cl = pi*((2*A0)+A1)
    print("Cl --> ", Cl)
    return Cl

def summation_for_gamma_custom(x, n):
    summation = 0
    theta = arccos(1-2*x)
    for i in range (1,n):
        summation += (compute_An_custom(i) * sin(i*theta))
        #print(summation)
    return summation

def compute_gamma_custom(alpha, x):
    u = 30 # Free Stream velocity as per our simulations
    summation = summation_for_gamma_custom(x, 100)
    A0 = compute_A0_custom(alpha)
    theta = arccos(1-2*x)
    gamma = 2*u*((A0*(1+cos(theta))/sin(theta)) + summation)
    return gamma

def compute_velocity_custom(x,y,alpha): # COMPUTE VELOCITY OF THE CUSTOM FUNCTION
    u = 30
    vel_x = 0
    vel_y = 0
    for i in linspace(0.005,0.995,100):
        yi = custom_function1_point(i) # CHANGE THE FUNCTION NUMBER USED HERE
        r = sqrt((x-i)*(x-i)+(y-yi)*(y-yi))
        v_ind = compute_gamma_custom(alpha,i)*0.01/(2*pi*r)
        cost = (x-i)/r
        sint = (y-yi)/r
        vel_x = vel_x + v_ind*sint
        vel_y = vel_y - v_ind*cost
    vel_x = vel_x + u*cos(alpha)
    vel_y = vel_y + u*sin(alpha)
    return [vel_x,vel_y]

def compute_vector_plot_custom(alpha): # VECTOR PLOT OF THE CUSTOM FUNCTION
    u = 30
    x_coord,y_coord = meshgrid(linspace(-1,2,20),linspace(-2,2,30))
    c,d = compute_velocity_custom(x_coord,y_coord,alpha)
    quiver(x_coord,y_coord,c,d)
    plot_custom_function1()   # CHANGE THE FUNCTION NUMBER USED HERE
    show()

def compute_circulation(alpha, m, p): # COMPUTE CIRCULATION THROUGH LINE INTERGRAL, A CIRCLE
    circulation = 0.0
    for theta in np.linspace(0, 2*np.pi, 101):
        #  Parametric coordinates of a circle centered at origin
        x_coord = 2*np.cos(theta)
        y_coord = 2*np.sin(theta)
        # Tangential unit vector along the circle at current point
        tangent_x, tangent_y = -2*np.sin(theta), 2*np.cos(theta)
        velocity_x, velocity_y = compute_velocity(x_coord, y_coord, alpha, m, p)
        circulation_segment = tangent_x * velocity_x + tangent_y * velocity_y
        circulation += circulation_segment
    circulation *= 2*np.pi / 100
    circulation *= -1 # Sign Convention for us
    print("Line integral circulation:", circulation)
    return circulation  # This function can take upto 5 minutes



def compute_bound_circulation(alpha, m, p): # THE CODE FOR BOUND CIRCULATION
    u = 30
    num_points = 1000
    points = linspace(0.0001, 0.9999, num_points)
    circulation = 0
    for i in range(0, num_points-1):
        x = points[i]
        x_1 = points[i+1]
        y = generate_naca_point(x, m, p)
        y_1 = generate_naca_point(x_1,m,p)
        gamma_local = compute_gamma(alpha, x, m, p)
        ds = sqrt((0.001)*(0.001)+(y-y_1)*(y-y_1)) # DEFINING INTEGRATION ELEMENT ds
        circulation += gamma_local*ds
    print("Bound circulation = ", circulation)
    return circulation


number = int(input("Please enter 4 digit NACA airfoil: ")) # function that takes in the NACA number of the airfoil

def master_function(number):
    m = (number//1000)/100
    p = (number//100 - 10*(number//1000))/10

    #camber_slope_plot(m, p)
    for i in range(-4,11):
        compute_Cl(i * pi / 180, m, p)

    print('Cm0 is')
    print(compute_Cm0(0, m, p))
    compute_An(1, 0.03, 0.2)
    compute_vector_plot(3*pi/180, m, p)
    #summation_for_gamma(0.005, 100, 0.03, 0.2)
    #total_circulation(0,0.03,0.2)
    plot_naca_airfoil(m, p)

    plot_custom_function1()
    plot_custom_function2()
    plot_custom_function3()
    plt.legend(['NACA 1211', 'Custom Fn 1', 'Custom Fn 2', 'Custom Fn 3'], loc="best")
    show()
    for i in range(-4,11):  #Cl of airfoil from -4 to 10 degree
        compute_Cl_custom(i * pi / 180)

    compute_vector_plot_custom(3*pi/180)
    compute_bound_circulation(3*pi/180, m, p)
    compute_circulation(3*pi/180, m, p)

master_function(number)

# DO NOT MISS TO CHANGE THE CUSTOM FUNCTION NUMBERS WHERE NECESSARY