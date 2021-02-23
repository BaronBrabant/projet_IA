import sys, os

#dictionnary 1
dict_1 = {1 : {'player_type' : 'AI', 'nb_turns' : 0, 'spawn_level' : 1},
          2 : {'player_type' : 'HUMAN', 'nb_turns' : 0, 'spawn_level' : 1}}

#dictionnary 2
dict_2 = {'Ant-1' : {'level' : 1, 'health' : 3, 'earth' : False, 'square_id' : 0},
          'Ant-2' : {'level' : 2, 'health' : 5, 'earth' : False, 'square_id' : 40},
          'Ant-3' : {'level' : 3, 'health' : 7, 'earth' : False, 'square_id' : 80}}


#test on dictionnary
#print(dict_1[2]['player_type'])



#List keeping position of everything in the map
#prints it out on the game board
list_position = []

for i in range(9):
    for j in range(9):
        square_position = []
        square_position = [j , i, 1, 'ant_1']
        list_position.append(square_position)

s = '''
{0} {1} {2}    {3} {4} {5}     {6} {7} {8}
{9} {10} {11}  {12} {13} {14}  {15} {16} {17} 
{18} {19} {20} {21} {22} {23}  {24} {25} {26}

{27} {28} {29}  {30} {31} {32}  {33} {34} {35}
{36} {37} {38}  {39} {40} {41}  {42} {43} {44}
{45}{46} {47}   {48} {49} {50}  {51} {52} {53}

{54} {55} {56}  {57} {58} {59} {60} {61} {62}   
{63} {64} {65}  {66} {67} {68} {69} {70} {71} 
{72} {73} {74}  {75} {76} {77} {78} {79} {80}
'''
#prints the gameboard by formating the list into it 
#print(s.format(*list_position))


#List anthill for level of spawn 
anthill_earth = [False,False,False,False,False,False,False,False]

print(anthill_earth)


#list to remember health points per level, where index are the levels
attack_list = [[1, 3], [2, 5], [3, 7]]

def give_orders(game_status):
    '''
    This will be the sole function with an input and will serve as an interface for the game to give all orders at the same time.
    These will be chains of characters which if formated correctly in the form r1-c1:*r2-c2, r1-c1:@r2-c2, r1-c1:lift or r1-c1:drop will be 
    interpreted by the game to execute orders and send the order to the correct function to be executed.

    orders:
    * = attack
    @ = movement 
    lift = lift motte
    drop = //

    Parameters
    __________
    game_status : this is a boolean value to determin if the game is over or not (bool)
    orders : string of charcaters which will be translated to orders (str)

    version : v1
    ---------
    spécification : Benjamin Richter (v1. 21/02/21)
    '''

    if game_status == False:
        #this first part of the function is going to either be the input of interpret the order
        orders_string = input('Please input orders')
        if orders_string != '':
            #this part needs to clean the string to interpret the order
            #it will do this by separating the string at every empty space ''
            list_indiviudal_orders = []
            list_attack = []
            list_movement = []
            list_drop = []
            list_lift = []

            list_indiviudal_orders.append(orders_string.split(' '))
            length_orders = len(list_indiviudal_orders[0])

            for chacaracter_list in list_indiviudal_orders[0]:
                for character in chacaracter_list:
                    #This is going to go through each list and recognise the orders
                    #when it recognises the order it sends them to each function 
                    #and executes them 
                    if character == '@':
                        print('yes')
                        #this will be a  movement
                        #send list containing order to the movement()
                        list_movement.append(chacaracter_list)
                    if character == '*':
                        print('attack')
                        #this will be attack
                        list_attack.append(chacaracter_list)
                        print(list_indiviudal_orders)
                    if character == 'd':
                        #this will be drop
                        list_drop.append(chacaracter_list)
                    if character == 'l':
                        list_lift.append(chacaracter_list)


    print(list_indiviudal_orders)
    print(list_movement)

#test for order function 
#give_orders(False)


def tchebyshev(coordinates):
    """
    This function calculates the Tchebyshev distance by 
    taking the c1,c2,r1 and r2 position to caluclate the distance between the given points
    
    parameters :
    ------------
    coordinates : list of four position values that the function needs (list)

    return:
    tchebyshev_distance : (tuple)
    version :
    ---------
    spécification : Frédéric Sauvage (v1. 21/02/21)
    """

    tchebyshev_x1 = coordinates[0]
    tchebyshev_x2 = coordinates[1]
    tchebyshev_y1 = coordinates[2]
    tchebyshev_y2 = coordinates[3]

    net_x = tchebyshev_x2 - tchebyshev_x1
    net_y = tchebyshev_y2 - tchebyshev_y1

    if net_x < 0:
        net_x = net_x*-1

    if net_y < 0:
        net_y = net_y*-1

    tchebyshev_tuple = (net_x, net_y)

    return tchebyshev_tuple



def thebyshev_distance(coordinates_agressor, coordinates_defender) :
    """
    This function takes the list_1 to find the position of the ant and calculates if the wanted attack is in range, if not 
    the order will be ignored.
    
    parameters :
    ------------
    list_1 : take the player and the second element of the list_1 (int)
    tchebyshev : take position x,y(tuple)
    return :
    posibility_attack : the ants can attack or not (bool)
    spécification : Frédéric Sauvage (v1. 21/02/21)
    version :
    ---------
    spécification : Frédéric Sauvage (v1. 21/02/21)
    """

    #this has to start by looking at the origin coordinates and
    #find about which ant it is talking about 
    coordinates = [coordinates_agressor[0], coordinates_defender[0], coordinates_agressor[1], coordinates_defender[1]]
    
    tchebyshev_tuple = tchebyshev(coordinates)
    if tchebyshev_tuple[0] > 3 or tchebyshev_tuple[1] >3:
        return False
    else:
        return True 



def ant_attack (dico_2, list_orders) :
    """
    This function uses the tchebyshev_distance() function to calculate the possibilty of the shot 
    and if succesful removes life points from ants in the dico_2.
    parameters : 
    ------------
    Tchebyshev_distance : take position x,y(tuple)
    dico_2 : take the first element in dico_2(int)
    return:
    dico_2 : replace second value in liste for eash ant life point less attack (int)
    version :
    ---------
    spécification : Frédéric Sauvage, Julien Emegenbirn (v1. 21/02/21)
    """

    #this will receive a list of orders, it will figure out how many orders there are,
    #will seperate the row and column positions for who is attacking who and will feed
    #it to the Tchebyshev function in order check if the enemy is in range or not
    #if the enemy is in range it will confirm the order and execute them all simoulantiousely

    




