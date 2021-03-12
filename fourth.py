import sys, os


#NOtE TO SELF
#the attack function works now you just need to make the end of the order function  remove dead ants


#dictionnary 1
player_dict = {1 : {'player_type' : 'AI', 'nb_turns' : 0, 'spawn_level' : 1},
          2 : {'player_type' : 'HUMAN', 'nb_turns' : 0, 'spawn_level' : 1}}

#dictionnary 2
ant_dict = {'Ant-1' : {'level' : 1, 'health' : 3, 'earth' : False, 'square_id' : 0, 'owner' : 1},
          'Ant-2' : {'level' : 2, 'health' : 5, 'earth' : False, 'square_id' : 40, 'owner' : 2},
          'Ant-3' : {'level' : 3, 'health' : 7, 'earth' : False, 'square_id' : 80, 'owner' : 1}}





def map_generator(cpx_file):
    '''
    This function will serve to read the information off of the cpx file and create the map which is our
    position tracker for the game ie the map_position.

    Parameter
    _________
    cpx_file : this file will contain the data containing the map size, anthill and clods (cpx)

    Return
    ______
    map_position : list of position of every square on the map enabling the rest of the function to find elements on the map(map_position)
    '''

    #the map size, anthill position and location of earth will be added separatly
    map_position = []

    index_square = 0
    for i in range(5):  
        for j in range(5):
            map_position.append([j, i, index_square, None])
            index_square += 1

    #map_position[3, 3, 0]

    print(map_position)



#test on dictionnary
#print(player_dict[2]['player_type'])



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
attack_list = [[0, 0], [1, 3], [2, 5], [3, 7]]

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

    version : Benjamin Richter (v1. 23/02/2021)
    ---------
    spécification : Benjamin Richter (v1. 21/02/21)
    '''

    if game_status == False:
        used_ants = []
        #this first part of the function is going to either be the input of interpret the order
        orders_string = input('Please input orders') # <--- input in another function difficulty playing ai 
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
                print(chacaracter_list)
                print('evolution sort', list_movement)
                #this is to make sure that the code only accepts one order at time and to ingore wrongly formatted orders
                print('this is the length', len(chacaracter_list))
                if len(chacaracter_list) <= 9:
                    for character in chacaracter_list:
                        #This is going to go through each list and recognise the orders
                        #when it recognises the order it sends them to each function 
                        #and executes them 

                        if character == 'd':
                            #this will be drop
                            list_drop.append(chacaracter_list)
                        if character == 'l':
                            list_lift.append(chacaracter_list)
                        if character == '*':
                            print('attack')
                            #this will be attack
                            list_attack.append(chacaracter_list)
                            print(list_indiviudal_orders)
                        if character == '@':
                            print('yes')
                            #this will be a  movement
                            #send list containing order to the movement()
                            list_movement.append(chacaracter_list)
                    
            #here needs to be the ai function which will add its orders to the list and process them at the same time
            
            #HERE GOES DROP LIFT FUNCTION <---------
            ant_attack(ant_dict, list_attack, 1)
            ant_attack()
            movement(ant_dict, map_position, list_movement, 1)
            


    #print(list_indiviudal_orders)
    #print(list_movement)

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
    version : Benjamin Richter (v1. 23/02/2021)
    ---------
    spécification : Frédéric Sauvage (v1. 21/02/21)
    """

    tchebyshev_x1 = int(coordinates[0])
    tchebyshev_x2 = int(coordinates[1])
    tchebyshev_y1 = int(coordinates[2])
    tchebyshev_y2 = int(coordinates[3])

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
    This function takes the map_position to find the position of the ant and calculates if the wanted attack is in range, if not 
    the order will be ignored.
    
    parameters :
    ------------
    map_position : take the player and the second element of the map_position (int)
    tchebyshev : take position x,y(tuple)
    return :
    posibility_attack : the ants can attack or not (bool)
    spécification : Frédéric Sauvage (v1. 21/02/21)
    version : Benjamin Richter (v1. 23/02/2021)
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

#this is an example of a map to test the code 
temp_list = [[0, 0, 0, None], [1, 0, 1, 'Mound-1'], [2, 0, 2, None], [3, 0, 3, None],  [4, 0, 4, None], 
            [0, 1, 5, None], [1, 1, 6, None], [2, 1, 7, None], [3, 1, 8, 'Mound-2'], [4, 1, 9, None], 
            [0, 2, 10, None], [1, 2, 11, 'Ant-1'], [2, 2, 12, 'Ant-2'], [3, 2, 13, None], [4, 2, 14, None], 
            [0, 3, 15, None], [1, 3, 16, None],  [2, 3, 17, 'Ant-3'], [3, 3, 18, None], [4, 3, 19, None], 
            [0, 4, 20, None], [1, 4, 21, None], [2, 4, 22, None], [3, 4, 23, 'Mound-3'],  [4, 4, 24, None]]

#still needs to delete dead ants after round is done
def ant_attack (ant_dict, list_orders, player) :
    """
    This function uses the tchebyshev_distance() function to calculate the possibilty of the shot 
    and if succesful removes life points from ants in the ant_dict.
    parameters : 
    ------------
    Tchebyshev_distance : take position x,y(tuple)
    ant_dict : take the first element in ant_dict(int)
    return:
    ant_dict : replace second value in liste for eash ant life point less attack (int)
    version : Benjamin Richter (v1. 23/02/2021)
    ---------
    spécification : Frédéric Sauvage, Julien Emegenbirn (v1. 21/02/21)
    """

    #this will receive a list of orders, it will figure out how many orders there are,
    #will seperate the row and column positions for who is attacking who and will feed
    #it to the Tchebyshev function in order check if the enemy is in range or not
    #if the enemy is in range it will confirm the order and execute them all simoulantiousely

    #10-10:*12-12
    print('this is the health before')
    print(ant_dict[temp_list[12][3]]['health'])

    new_list1 = []
    list_unwanted = ['-', ':', '*']
    list_length = len(list_orders)
   

    for i in range(list_length):
        new_list1.append('')
        for character in list_orders[i]:
            if character not in list_unwanted:
                new_list1.append(character)
            else:
                new_list1.append('')
    new_list1.append('')

    save_nb = ''
    cleaned_list = []
    for numbers in new_list1:
        print(numbers)
        if numbers != '':
            save_nb = save_nb + numbers 
        elif numbers == '' and save_nb != '':
            cleaned_list.append(save_nb)
            save_nb = ''

    #this shows the given list and how the data looks when inputed
    #print(list_orders)   

    #this shows the data after it has been 'cleaned'
    #print(new_list1)

    #this shows the cleaned data put back together for the game to use
    #print(cleaned_list)

    #now we can use the cleaned data to find how many order are given 
    #and call the tchebychez and according amount of times


    #IMPORTANT 
    #An attack is a set of 4 coordinates so attacks_nb = 4 represents one attack and attack_nb = 16 is 4 attacks
    amount_attacks = len(cleaned_list)
    print('amount attacks',amount_attacks)
    amount_attacks = int(amount_attacks)/4
    amount_attacks = int(amount_attacks)

    #IMPORTANT 
    #An attack is a set of 4 coordinates so attacks_nb = 4 represents one attack and attack_nb = 16 is 4 attacks
    #This is done to let the code iterate through the four coordinates at a time and check if the order is legal
    

    attack_offset = 0
    for attacks_nb in range(amount_attacks):
        attacks_nb = attacks_nb + attack_offset
        print(attacks_nb)

        column_1 = attacks_nb + 0
        row_1 = attacks_nb + 1
        column_2 = attacks_nb + 2
        row_2 = attacks_nb + 3

        if thebyshev_distance([cleaned_list[column_1],cleaned_list[row_1]], [cleaned_list[column_2], cleaned_list[row_2]]) == True:
            #attacks
            print('attack')
            #this snippets checks who's turn it is 
            square_id_att = int(int(cleaned_list[row_1])*5 + int(cleaned_list[column_1]))
            square_id_def = int(int(cleaned_list[row_2])*5 + int(cleaned_list[column_2]))
            print(square_id_att, 'this is index ')
            if player == '1':
                #this means player one is playing
                #this will calulcate the square_id with the coordinates and confirm it belongs to the player with ant_dict
                #we need to change the 5 into a 20 when moving to full siyed map
                if temp_list[square_id_att][3] != None:
                    if ant_dict[temp_list[square_id_att][3]]['owner'] == 1:
                        #this checks if the ant belongs to the player one
                        if ant_dict[temp_list[square_id_att][3]]['health'] > 0:
                            #this checks if the ant is alive

                            amount_damage = attack_list[ant_dict[temp_list[square_id_att][3]]['level']][1]
                            #this checks the level of the ant to apply damage#

                            ant_dict[temp_list[square_id_def][3]]['health'] = ant_dict[temp_list[square_id_def][3]]['health'] - amount_damage        
            else:
                if temp_list[square_id_att][3] != None:
                    if ant_dict[temp_list[square_id_att][3]]['owner'] == 2:
                        #this checks if the ant belongs to the player two
                        if ant_dict[temp_list[square_id_att][3]]['health'] > 0:
                            #this checks if the ant is alive

                            amount_damage = attack_list[ant_dict[temp_list[square_id_att][3]]['level']][1]
                            #this checks the level of the ant to apply damage#

                            ant_dict[temp_list[square_id_def][3]]['health'] = ant_dict[temp_list[square_id_def][3]]['health'] - amount_damage        
        else:
            print('attack failed')
        attack_offset += 3

    #print('this is the health after')
    #print(ant_dict[temp_list[12][3]]['health'])
    #print(ant_dict[temp_list[11][3]]['health'])

    #as all attacks can be fed to him he will delet all dead ants simoutansiously
    #remove health
    
    
    #NOTES TO SELF

    #so far you have a check for the range and a check for if it belongs to the right player 
    
#ant_attack(ant_dict, ['10-12:*20-20', '11-12:*11-11'])


used_orders = []

def movement(ant_dict1, list_position_earth, order_list, player):
    '''
    This function will take the desired order_list, will check if the inputed position of the wanted ant is correct by checking
    its position in the list_position_earth and will finally allow the player to move its ant to the desired position if it does 
    not infringe any game rules such as moving onto a squre filled with earth while already carrying some through the dico2.
    If the movement is succesful the list inputed as the list_position_earth will be updated with the new game coordinates.
    This will also use the Tchebychec function directly by checking if any distance is higher than 1 in the tuble returned by the function.

    Parameters
    __________
    dico2 : dictionary containing information on the ant such as its health and if it is carrying earth or not (dict)
    list_position_earth : this is the list containing information on what is happening on every square of the map (list)
    order_list : this will be a string under the format r1-c1:*r2-c2 where as many of those orders can be inputed simultaneously as wanted(str)
    
    

    version : Benjamin Richter (v1. 22/02/21, v2. 25/02/21)
    ---------
    spécification : Benjamin Richter (v1. 21/02/21)
    '''
    #THIS VARIABLE SETS THE UPPER AND LOWER LIMITS OF THE MAP

    max_out_bound = 24
    min_out_bound = 0



    #this records all legal orders
    legal_orders = []

    #this uses the imported orders to clean them into coordinates  

    list_wanted = ['0','1','2','3','4','5','6','7','8','9']
    cleaned_list = []
    print(order_list)
    for order in order_list:
        
        cleaned_list.append('')
        for character in order:
            #print(character)
            if character in list_wanted:
                cleaned_list.append(character)
            else:
                cleaned_list.append('') 
        cleaned_list.append('')

    #print(cleaned_list)

    save_nb = ''
    cleaned_list_2 = []
    for numbers in cleaned_list:
        #print(numbers)
        if numbers != '':
            save_nb = save_nb + numbers 
        elif numbers == '' and save_nb != '':
            cleaned_list_2.append(save_nb)
            save_nb = ''

    #print(cleaned_list_2, 'this the clean maybe the error too')


    amount_orders = len(cleaned_list_2)
    separated_list = []
    for i in range(0, amount_orders, 4):
        new_list = []
    
        for j in range(i, i+4):
            new_list.append(cleaned_list_2[j])

        separated_list.append(new_list)
    #print('this is the seprated', separated_list)

    #this checks if the orders are duable and executes them later if they are
    for coordinates in separated_list:
        tchebyshev_tuple = tchebyshev([coordinates[0],coordinates[2], coordinates[1],coordinates[3]])
        #print(tchebyshev_tuple)
        if tchebyshev_tuple[0] <= 1 and tchebyshev_tuple[1] <= 1:
            legal_orders.append(coordinates)


    #print(separated_list)
    print('this is legal', legal_orders)
    #print(cleaned_list_2)

    #!!!!!!!! il faut encore programmer les out of bounds
    
    
    #jusqu ici le porgramme rend les ordres lisibles au code et determine si l'ordre est legal ou non
    #apres ceci le reste de la fonction va regarder les possibilites qui l'empecheraient et l'execute


    

    #ok this is the start of the movement restirction first imma program two ants moving on the same position

    if player == 1:
        for legal_order in legal_orders:
            origin_coord = []
            square_id_destination = int(legal_order[2]) + int(legal_order[3]) * 5

            if temp_list[square_id_destination][3] == None:

                print('wanted destination is free')
                square_id_origin = int(legal_order[0]) + int(legal_order[1]) * 5
                ant_name = temp_list[square_id_origin][3]
                if square_id_destination <= max_out_bound and square_id_destination >= min_out_bound:
                    if ant_name != None:
                        print('ant found in list position')
                        ant_name = str(ant_name)
                        print(ant_name)
                        if ant_dict[ant_name]['owner'] == 1 and ant_dict[ant_name]['earth'] == False:
                            
                            print('this is the variables fault')
                            #this changes the square id position in the ant dict
                            ant_dict[ant_name]['square_id'] = square_id_destination
                            #this resets the list_position to None and adds the ant to the position
                            temp_list[square_id_origin][3] = None
                            temp_list[square_id_destination][3] = ant_name
                            #now this should should add the origin coordinates to the already executed list
                            for origin_coordinates in range(2):
                                origin_coord.append(legal_order[origin_coordinates])
                                used_orders.append(origin_coord)
                        elif ant_dict[ant_name]['owner'] == 1:



    else:
        for legal_order in legal_orders:
            square_id_destination = int(legal_order[2]) + int(legal_order[3]) * 5

            if temp_list[square_id_destination][3] == None:

                print('order is legal')


#movement('a','a',['4-3:@3-2','4-3:@3-4', '4-3:@3-4', '4-3:@4-2', '4-3:@4-4', '4-3:@5-2', '4-3:@5-3', '4-3:@5-4'])


map_position = map_generator('This is where the cpx file will go')
game_status = False

while game_status == False:

    give_orders(game_status)
