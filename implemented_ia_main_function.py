from random import randint
import socket
import time
import sys, os
import blessed
term = blessed.Terminal()
print(term.home + term.clear, end='')

#NOtE TO SELF
#the attack function works now you just need to make the end of the order function  remove dead ants





"""Module providing remote play features for UNamur programmation project (INFOB132).

Sockets are used to transmit orders on local or remote machines.
Firewalls or restrictive networks settings may block them.  

More details on sockets: https://docs.python.org/2/library/socket.html.

Author: Benoit Frenay (benoit.frenay@unamur.be).

"""






def create_server_socket(local_port, verbose):
    """Creates a server socket.
    
    Parameters
    ----------
    local_port: port to listen to (int)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_in: server socket (socket.socket)
    
    """
    
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    if verbose:
        print(' binding on local port %d to accept a remote connection' % local_port)
    
    try:
        socket_in.bind(('', local_port))
    except:
        raise IOError('local port %d already in use by your group or the referee' % local_port)
    socket_in.listen(1)
    
    if verbose:
        print('   done -> can now accept a remote connection on local port %d\n' % local_port)
        
    return socket_in

def create_client_socket(remote_IP, remote_port, verbose):
    """Creates a client socket.
    
    Parameters
    ----------
    remote_IP: IP address to send to (int)
    remote_port: port to send to (int)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_out: client socket (socket.socket)
    
    """

    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state
    
    connected = False
    msg_shown = False
    
    while not connected:
        try:
            if verbose and not msg_shown:
                print(' connecting on %s:%d to send orders' % (remote_IP, remote_port))
                
            socket_out.connect((remote_IP, remote_port))
            connected = True
            
            if verbose:
                print('   done -> can now send orders to %s:%d\n' % (remote_IP, remote_port))
        except:
            if verbose and not msg_shown:
                print('   connection failed -> will try again every 100 msec...')
                
            time.sleep(.1)
            msg_shown = True
            
    return socket_out
    
def wait_for_connection(socket_in, verbose):
    """Waits for a connection on a server socket.
    
    Parameters
    ----------
    socket_in: server socket (socket.socket)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_in: accepted connection (socket.socket)
    
    """
    
    if verbose:
        print(' waiting for a remote connection to receive orders')
        
    socket_in, remote_address = socket_in.accept()
    
    if verbose:
        print('   done -> can now receive remote orders from %s:%d\n' % remote_address)
        
    return socket_in            

def create_connection(your_group, other_group=0, other_IP='127.0.0.1', verbose=False):
    """Creates a connection with a referee or another group.
    
    Parameters
    ----------
    your_group: id of your group (int)
    other_group: id of the other group, if there is no referee (int, optional)
    other_IP: IP address where the referee or the other group is (str, optional)
    verbose: True only if connection progress must be displayed (bool, optional)
    
    Returns
    -------
    connection: socket(s) to receive/send orders (dict of socket.socket)
    
    Raises
    ------
    IOError: if your group fails to create a connection
    
    Notes
    -----
    Creating a connection can take a few seconds (it must be initialised on both sides).
    
    If there is a referee, leave other_group=0, otherwise other_IP is the id of the other group.
    
    If the referee or the other group is on the same computer than you, leave other_IP='127.0.0.1',
    otherwise other_IP is the IP address of the computer where the referee or the other group is.
    
    The returned connection can be used directly with other functions in this module.
            
    """
    
    # init verbose display
    if verbose:
        print('\n[--- starts connection -----------------------------------------------------\n')
        
    # check whether there is a referee
    if other_group == 0:
        if verbose:
            print('** group %d connecting to referee on %s **\n' % (your_group, other_IP))
        
        # create one socket (client only)
        socket_out = create_client_socket(other_IP, 42000+your_group, verbose)
        
        connection = {'in':socket_out, 'out':socket_out}
        
        if verbose:
            print('** group %d successfully connected to referee on %s **\n' % (your_group, other_IP))
    else:
        if verbose:
            print('** group %d connecting to group %d on %s **\n' % (your_group, other_group, other_IP))

        # create two sockets (server and client)
        socket_in = create_server_socket(42000+your_group, verbose)
        socket_out = create_client_socket(other_IP, 42000+other_group, verbose)
        
        socket_in = wait_for_connection(socket_in, verbose)
        
        connection = {'in':socket_in, 'out':socket_out}

        if verbose:
            print('** group %d successfully connected to group %d on %s **\n' % (your_group, other_group, other_IP))
        
    # end verbose display
    if verbose:
        print('----------------------------------------------------- connection started ---]\n')

    return connection
                
def bind_referee(group_1, group_2, verbose=False):
    """Put a referee between two groups.
    
    Parameters
    ----------
    group_1: id of the first group (int)
    group_2: id of the second group (int)
    verbose: True only if connection progress must be displayed (bool, optional)
    
    Returns
    -------
    connections: sockets to receive/send orders from both players (dict)
    
    Raises
    ------
    IOError: if the referee fails to create a connection
    
    Notes
    -----
    Putting the referee in place can take a few seconds (it must be connect to both groups).
        
    connections contains two connections (dict of socket.socket) which can be used directly
    with other functions in this module.  connection of first (second) player has key 1 (2).
            
    """
    
    # init verbose display
    if verbose:
        print('\n[--- starts connection -----------------------------------------------------\n')

    # create a server socket (first group)
    if verbose:
        print('** referee connecting to first group %d **\n' % group_1)        

    socket_in_1 = create_server_socket(42000+group_1, verbose)
    socket_in_1 = wait_for_connection(socket_in_1, verbose)

    if verbose:
        print('** referee succcessfully connected to first group %d **\n' % group_1)        
        
    # create a server socket (second group)
    if verbose:
        print('** referee connecting to second group %d **\n' % group_2)        

    socket_in_2 = create_server_socket(42000+group_2, verbose)
    socket_in_2 = wait_for_connection(socket_in_2, verbose)

    if verbose:
        print('** referee succcessfully connected to second group %d **\n' % group_2)        
    
    # end verbose display
    if verbose:
        print('----------------------------------------------------- connection started ---]\n')

    return {1:{'in':socket_in_1, 'out':socket_in_1},
            2:{'in':socket_in_2, 'out':socket_in_2}}


def close_connection(connection):
    """Closes a connection with a referee or another group.
    
    Parameters
    ----------
    connection: socket(s) to receive/send orders (dict of socket.socket)
    
    """
    
    # get sockets
    socket_in = connection['in']
    socket_out = connection['out']
    
    # shutdown sockets
    socket_in.shutdown(socket.SHUT_RDWR)    
    socket_out.shutdown(socket.SHUT_RDWR)
    
    # close sockets
    socket_in.close()
    socket_out.close()
    
    
def notify_remote_orders(connection, orders):
    """Notifies orders to a remote player.
    
    Parameters
    ----------
    connection: sockets to receive/send orders (dict of socket.socket)
    orders: orders to notify (str)
        
    Raises
    ------
    IOError: if remote player cannot be reached
    
    """

    # deal with null orders (empty string)
    if orders == '':
        orders = 'null'
    
    # send orders
    try:
        connection['out'].sendall(orders.encode())
    except:
        raise IOError('remote player cannot be reached')


def get_remote_orders(connection):
    """Returns orders from a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (dict of socket.socket)
        
    Returns
    ----------
    player_orders: orders given by remote player (str)

    Raises
    ------
    IOError: if remote player cannot be reached
            
    """
   
    # receive orders    
    try:
        orders = connection['in'].recv(65536).decode()
    except:
        raise IOError('remote player cannot be reached')
        
    # deal with null orders
    if orders == 'null':
        orders = ''
        
    return orders



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

    fh = open(cpx_file, 'r')
    cpx_string = fh.readlines()
    fh.close()
    
    #print(cpx_string)
    

    map_coord = cpx_string[1]
    anthill_coord = cpx_string[3:5]
    clods_coord = cpx_string[6:]
    #print(clods_coord)
    #print(map_coord)
    #print(anthill_coord)
    #print(clods_coord)
    information_clean = []
    cleaned_row = ''
    cleand_column = ''
    state = 'row'

    wanted_strings = ['0','1','2','3','4','5','6','7','8','9']

    for letters in map_coord:
        if letters in wanted_strings and state == 'row':
            cleaned_row += letters
        elif letters == ' ':
            state = 'column'
        elif letters in wanted_strings and state == 'column':
            cleand_column += letters

    information_clean.append(cleaned_row)
    information_clean.append(cleand_column)
    

    cleaned_row = ''
    cleand_column = ''

    state = 'row'

    for letters_1 in anthill_coord:
        state = 'row'
        for character in letters_1:
            #print(state, character, 'this is the cleaned' ,cleand_column)
            if character in wanted_strings and state == 'row':
                cleaned_row += character
            elif character == ' ':
                state = 'column'
                information_clean.append(cleaned_row)
                cleaned_row = ''
            elif character in wanted_strings and state == 'column':
                #print('executed an added', cleand_column)
                cleand_column += character
            
        information_clean.append(cleand_column)
        cleand_column = ''
    

    cleaned_row = ''
    cleand_column = ''
    weight_clods = ''
    index_clods_info = 0

    state = 'row'

    for letters_2 in clods_coord:
        #print(letters_2, 'these are the letter')
        index_clods_info = 0
        for character_clods in letters_2:
            
            if index_clods_info > 2:
                index_clods_info = 0

            if index_clods_info == 0:
                state = 'row'
            elif index_clods_info == 1:
                state ='column'
            elif index_clods_info == 2:
                state = 'weight'
            

            if character_clods == ' ':
                index_clods_info += 1                           
            elif character_clods in wanted_strings and state == 'row':
                cleaned_row += character_clods
            elif character_clods in wanted_strings and state == 'column':
                #print('executed an added', cleand_column)
                cleand_column += character_clods
            elif character_clods in wanted_strings and state == 'weight':
                weight_clods += character_clods


        #print(cleaned_row, 'this the row')
        #print(cleand_column)      
        information_clean.append(cleaned_row)
        information_clean.append(cleand_column)
        information_clean.append(weight_clods)
        cleand_column = ''
        cleaned_row = ''
        weight_clods = ''
    
    
    
    #for anthill_index in range(2):
        
    #!!!!! the inforamation_clean variable is a list containing the map dimesion in the index 0 and 1,
    # the anthill position in index 2 to 5 where the first pair is the coordianates of the anthill 1 and the latter is the same for player 2,
    # the rest of the coordinates have to be broken up in groups of 3 corresponding to the row, column and the weight of the earth
    



    
    #this strip of code initilizes the map and gets it ready to be filled 
    map_col_dim = int(information_clean[0]) 
    map_row_dim = int(information_clean[1]) 
    map_position = []
    index_square = 1
    for i in range(1, map_row_dim + 1):  
        for j in range(1, map_col_dim + 1):
            map_position.append([j, i, index_square, None, 0])
            index_square += 1
    #map_position[3, 3, 0]
    

    #this is what places the anthills

    coord_anthill_1 = information_clean[2:4]
    coord_anthill_2 = information_clean[4:6]
    
    #this calculates the position of the ant in order to find the map_position index
    square_id_anthill_1 = (int(coord_anthill_1[1]) -1 )*map_col_dim + (int(coord_anthill_1[0]) -1 )
    square_id_anthill_2 = (int(coord_anthill_2[1]) -1 )*map_col_dim + (int(coord_anthill_2[0]) -1 )

    #print(square_id_anthill_1, 'this is the result')

    #this sets the position of both anthills in the main map list
    #map_position[square_id_anthill_1][3] = 'Anthill\1'
    #map_position[square_id_anthill_2][3] = 'Anthill\2'

    anthill_1 = square_id_anthill_1
    anthill_2 = square_id_anthill_2
    
    #this part iterates through a set of 3 indexes corresponding to the column, row and weight of clod

    #this figres out how many orders there are

    length_order = len(information_clean[6:])
    #print(information_clean)
    
    for group_3 in range(6, length_order+6, 3):
        temp_calc = []
        
        for iterator in range(3):
           
            temp_calc.append(information_clean[group_3+iterator])

        #print(map_col_dim)
        square_id = (int(temp_calc[1]) -1 )*map_col_dim  + (int(temp_calc[0]) -1 )
        #print(square_id)
        
        weight = int(temp_calc[2])
        map_position[square_id][4] = weight


    #print(map_position)
    #print(information_clean)

    map_position = [map_position, anthill_1, anthill_2]

    return map_position
    
#map_generator(r'C:\Users\benny\OneDrive\Desktop\project ia\small.cpx')



#test on dictionnary
#print(player_dict[2]['player_type'])


#List anthill for level of spawn 





#list to remember health points per level, where index are the levels


def give_orders(game_status, ant_dict, player_dict, map_position, anthill_1, anthill_2):
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
        orders_string = ai_decision(ant_dict, map_position, anthill_1, anthill_1)
        order_string_2 = input('')
        #input (print ( term.move_xy (100, 100) + term.yellow('Please input orders'), end = '') ) # <--- input in another function difficulty playing ai 
        if orders_string != '':
            #this part needs to clean the string to interpret the order
            #it will do this by separating the string at every empty space ''
            list_indiviudal_orders = []
            list_attack = []
            list_movement = []
            list_drop_lift = []
            


            list_indiviudal_orders.append(orders_string.split(' '))
    

            for chacaracter_list in list_indiviudal_orders[0]:
                #print(chacaracter_list)
                #print('evolution sort', list_movement)
                #this is to make sure that the code only accepts one order at time and to ingore wrongly formatted orders
               
                
                for character in chacaracter_list:
                    #This is going to go through each list and recognise the orders
                    #when it recognises the order it sends them to each function 
                    #and executes them 
                    if character == 'd' or character == 'l':
                        #this will be drop
                        list_drop_lift.append(chacaracter_list)
                        
             
                    if character == '*':
                        #print('attack')
                        #this will be attack
                        list_attack.append(chacaracter_list)
                        
                        
                    if character == '@':
                        #print('yes')
                        #this will be a  movement
                        #send list containing order to the movement()
                        list_movement.append(chacaracter_list)
                
            #here needs to be the ai function which will add its orders to the list and process them at the same time
            if list_drop_lift != []:
                motte_de_terre(ant_dict, list_drop_lift, map_position)
            #HERE GOES DROP LIFT FUNCTION <---------
            ant_attack(ant_dict, list_attack, '1', map_position)
            #ant_attack()
            movement(ant_dict, map_position, list_movement, '1', map_position)

        player_dict[1]['nb_turns'] = player_dict[1]['nb_turns'] + 1

        used_orders = []
        if order_string_2 != '':
            #this part needs to clean the string to interpret the order
            #it will do this by separating the string at every empty space ''
            list_indiviudal_orders = []
            list_attack = []
            list_movement = []
            list_drop_lift = []
            


            list_indiviudal_orders.append(order_string_2.split(' '))
    

            for chacaracter_list in list_indiviudal_orders[0]:
                #print(chacaracter_list)
                #print('evolution sort', list_movement)
                #this is to make sure that the code only accepts one order at time and to ingore wrongly formatted orders
               
                
                for character in chacaracter_list:
                    #This is going to go through each list and recognise the orders
                    #when it recognises the order it sends them to each function 
                    #and executes them 
                    if character == 'd' or character == 'l':
                        #print('lift, drop')
                        list_drop_lift.append(chacaracter_list)
                        #print(list_attack, 'IF THIS DOESNT WORK I DUNNO)')
             
                    if character == '*':
                        #print('attack')
                        #this will be attack
                        list_attack.append(chacaracter_list)
                        
                        
                    if character == '@':
                        
                        #this will be a  movement
                        #send list containing order to the movement()
                        list_movement.append(chacaracter_list)
                
 
            if list_drop_lift != []:
                motte_de_terre(ant_dict, list_drop_lift, map_position)
         
            ant_attack(ant_dict, list_attack, '2', map_position)
           
            movement(ant_dict, map_position, list_movement, '2', map_position)

        player_dict[2]['nb_turns'] = player_dict[2]['nb_turns'] + 1
    
            


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
    if tchebyshev_tuple[0] > 3 or tchebyshev_tuple[1] > 3:
        return False
    else:
        return True 

#still needs to delete dead ants after round is done
def ant_attack (ant_dict, list_orders, player, map_position):
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
    #print('this is the health before')
    

    new_list1 = []
    list_unwanted = ['-', ':', '*']
    list_length = len(list_orders)
    #print(list_orders, 'this is how the order arrives')

    for i in range(list_length):
        new_list1.append('')
        for character in list_orders[i]:
            #print(character)
            if character not in list_unwanted:
                new_list1.append(character)
            else:
                new_list1.append('')
    new_list1.append('')
    

    save_nb = ''
    cleaned_list = []
    for numbers in new_list1:
        #print(numbers)
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
    #print(cleaned_list, 'this shows me if the probeleme is within the cleaner or not')

    #now we can use the cleaned data to find how many order are given 
    #and call the tchebychez and according amount of times


    #IMPORTANT 
    #An attack is a set of 4 coordinates so attacks_nb = 4 represents one attack and attack_nb = 16 is 4 attacks
    amount_attacks = len(cleaned_list)
    #print('amount attacks',amount_attacks)
    amount_attacks = int(amount_attacks)/4
    amount_attacks = int(amount_attacks)

    map_dimension_row = map_position[-1][1] 
    

    #IMPORTANT 
    #An attack is a set of 4 coordinates so attacks_nb = 4 represents one attack and attack_nb = 16 is 4 attacks
    #This is done to let the code iterate through the four coordinates at a time and check if the order is legal
    

    attack_offset = 0
    #(amount_attacks, 'this is was stopping the function from starting')
    
    for attacks_nb in range(0, amount_attacks):
        
        attacks_nb = attacks_nb + attack_offset
        #print(attacks_nb)

        column_1 = attacks_nb + 0
        row_1 = attacks_nb + 1
        column_2 = attacks_nb + 2
        row_2 = attacks_nb + 3

        attack_coord = [cleaned_list[column_1], cleaned_list[row_1]]
        
        if attack_coord not in used_orders:
            
            if thebyshev_distance([cleaned_list[column_1],cleaned_list[row_1]], [cleaned_list[column_2], cleaned_list[row_2]]) == True:
                #attacks
                #print('attack')
                #this snippets checks who's turn it is 
                square_id_att = int((int(cleaned_list[row_1])-1 )*map_dimension_row + (int(cleaned_list[column_1] -1)))
                square_id_def = int((int(cleaned_list[row_2])-1 )*map_dimension_row + (int(cleaned_list[column_2]-1 )))
                #print(square_id_att, 'this is index ')

                if player == '1':
                    #print('triggered')
                    #this means player one is playing
                    #this will calulcate the square_id with the coordinates and confirm it belongs to the player with ant_dict
                    #we need to change the 5 into a 20 when moving to full siyed map
                    if map_position[square_id_att][3] == '🐜':
                        map_position[square_id_att][3] = None
                    if map_position[square_id_att][3] != None and map_position[square_id_def][3] != None:
                        if ant_dict[map_position[square_id_att][3]]['owner'] == 1 and ant_dict[map_position[square_id_att][3]]['health'] > 0:
                            #this checks if the ant belongs to the player one
                            used_orders.append([cleaned_list[column_1],cleaned_list[row_1]])
                            #this checks if the ant is alive
                            amount_damage = attack_list[ant_dict[map_position[square_id_att][3]]['level']][1]
                            #this checks the level of the ant to apply damage#
                            #print(map_position[square_id_def][3])
                            ant_dict[map_position[square_id_def][3]]['health'] = ant_dict[map_position[square_id_def][3]]['health'] - amount_damage        
                else:
                    if map_position[square_id_att][3] == '🐜':
                        map_position[square_id_att][3] = None
                    if map_position[square_id_att][3] != None and map_position[square_id_def][3] != None:
                        if ant_dict[map_position[square_id_att][3]]['owner'] == 2 and ant_dict[map_position[square_id_att][3]]['health'] >= 0:
                            #this checks if the ant belongs to the player two
                            used_orders.append([cleaned_list[column_1],cleaned_list[row_1]])
                            #this checks if the ant is alive

                            amount_damage = attack_list[ant_dict[map_position[square_id_att][3]]['level']][1]
                            #this checks the level of the ant to apply damage#

                            ant_dict[map_position[square_id_def][3]]['health'] = ant_dict[map_position[square_id_def][3]]['health'] - amount_damage        
          
            attack_offset += 3

    
    #THIS DELETS THE ANTS AT THE END OF THE ROUND
   
    if player == '2':
        
        amount_ants = len(ant_dict)
        for ant_id in ant_dict:
            #print(ant_dict['Ant-%s'%counter]['health'] , 'this is what the counter ext6racts for healthj')
            
            if ant_dict[ant_id]['health'] <= 0:
                
                square_id_del = ant_dict[ant_id]['square_id']
                square_id_del -= 1
                if map_position[square_id_del][3] != None and map_position[square_id_del][3] == str(ant_id):
                    if ant_dict[ant_id]['earth'] != 0:
                        earth_weight = ant_dict[ant_id]['earth']
                        map_position[square_id_del][4] = earth_weight
                        #this condition makes sure that squares where ants died previously don't delet the future ants going over it 
                        map_position[square_id_del][3] = None
                    else:
                        map_position[square_id_del][3] = None
    
    #as all attacks can be fed to him he will delet all dead ants simoutansiously
    #remove health
    
    
    #NOTES TO SELF

    #so far you have a check for the range and a check for if it belongs to the right player 
    
#ant_attack(ant_dict, ['10-12:*20-20', '11-12:*11-11'])



def movement(ant_dict1, list_position_earth, order_list, player, map_position):
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

    max_out_bound = map_position[-1][0] * map_position[-1][1] - 1
    
    min_out_bound = 0
    map_dimension_row = map_position[-1][1]  


    #this records all legal orders
    legal_orders = []

    #this uses the imported orders to clean them into coordinates  

    list_wanted = ['0','1','2','3','4','5','6','7','8','9']
    cleaned_list = []
    #print(order_list)
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
    #print('this is legal', legal_orders)
    #print(cleaned_list_2)

    
    
    
    #jusqu ici le porgramme rend les ordres lisibles au code et determine si l'ordre est legal ou non
    #apres ceci le reste de la fonction va regarder les possibilites qui l'empecheraient et l'execute


    

    #ok this is the start of the movement restirction first imma program two ants moving on the same position

    if player == '1':
        for legal_order in legal_orders:
            origin_coord = [legal_order[0], legal_order[1]]
            square_id_destination = int(legal_order[2])-1 + (int(legal_order[3])-1) * map_dimension_row
            
            if origin_coord not in used_orders:
                if map_position[square_id_destination][3] == None :


                    square_id_origin = (int(legal_order[0])-1 ) + (int(legal_order[1])-1 ) * map_dimension_row
                    ant_name = map_position[square_id_origin][3]
                    if square_id_destination <= max_out_bound and square_id_destination >= min_out_bound:
                        if ant_name != None and ant_name != '🐜' :
                            if ant_dict[ant_name]['earth'] == 0:    
                                #print('ant found in map position')
                                ant_name = str(ant_name)
                                #print(ant_name)
                                if ant_dict[ant_name]['owner'] == 1:

                                    #this changes the square id position in the ant dict
                                    ant_dict[ant_name]['square_id'] = square_id_destination
                                    #this resets the list_position to None and adds the ant to the position
                                    map_position[square_id_origin][3] = None
                                    map_position[square_id_destination][3] = ant_name
                                    #now this should should add the origin coordinates to the already executed list

                                    used_orders.append(origin_coord)
                            elif ant_dict[ant_name]['earth'] > 0 and map_position[square_id_destination][4] == 0:
                                #print('ant found in map position')
                                ant_name = str(ant_name)
                                #print(ant_name)
                                if ant_dict[ant_name]['owner'] == 1:

                                    #this changes the square id position in the ant dict
                                    ant_dict[ant_name]['square_id'] = square_id_destination
                                    #this resets the list_position to None and adds the ant to the position
                                    map_position[square_id_origin][3] = None
                                    map_position[square_id_destination][3] = ant_name
                                    #now this should should add the origin coordinates to the already executed list

                                    used_orders.append(origin_coord)

    else:      
                   
        for legal_order in legal_orders:
            origin_coord = []
            square_id_destination = (int(legal_order[2])-1 ) + (int(legal_order[3])-1 ) * map_dimension_row
             
            if origin_coord not in used_orders:
           
                if map_position[square_id_destination][3] == None:
                
                    
                    square_id_origin = (int(legal_order[0])-1 ) + (int(legal_order[1])-1 ) * map_dimension_row
                    ant_name = map_position[square_id_origin][3]
                    if square_id_destination <= max_out_bound and square_id_destination >= min_out_bound:
                        if ant_name != None and ant_name != '🐜':
                            if ant_dict[ant_name]['earth'] == 0:
                                ant_name = str(ant_name)
                                print(ant_name)
                                if ant_dict[ant_name]['owner'] == 2:

                                    #this changes the square id position in the ant dict
                                    ant_dict[ant_name]['square_id'] = square_id_destination
                                    #this resets the list_position to None and adds the ant to the position
                                    map_position[square_id_origin][3] = None
                                    map_position[square_id_destination][3] = ant_name
                                    #now this should should add the origin coordinates to the already executed list

                                    used_orders.append(origin_coord)
                            elif ant_dict[ant_name]['earth'] > 0 and map_position[square_id_destination][4] == 0:
                                ant_name = str(ant_name)
                                #print(ant_name)
                                if ant_dict[ant_name]['owner'] == 2:
                                
                                    #this changes the square id position in the ant dict
                                    ant_dict[ant_name]['square_id'] = square_id_destination
                                    #this resets the list_position to None and adds the ant to the position
                                    map_position[square_id_origin][3] = None
                                    map_position[square_id_destination][3] = ant_name
                                    #now this should should add the origin coordinates to the already executed list

                                    used_orders.append(origin_coord)

#movement('a','a',['4-3:@3-2','4-3:@3-4', '4-3:@3-4', '4-3:@4-2', '4-3:@4-4', '4-3:@5-2', '4-3:@5-3', '4-3:@5-4'])

def motte_de_terre(ant_dict, list_orders, map_position):
    """
    This function serves to pickup and drop a piece of earth. 
    It takes the dico_2 as paramter to establish whether the ant is already carrying something or not.
    
    Parameters :
    ------------
    ant_dict : The third elements of all the list in the dictionary (bool)
    list_orders : list of filtered orders (list)
    map_position : list containing entities on map (list)
    
    :return:
    ant_charge : If the ant as already a motte (bool)
    Version :
    ---------
    Specification : Julien Emegenbirn (v1. 19/02/2021)
    """

    #this cleaner only needs the origin coordinates to check if the ant is carrying something or not

        
    map_dimension_row = map_position[-1][1]  
    #this uses the imported orders to clean them into coordinates  

    list_wanted = ['0','1','2','3','4','5','6','7','8','9', 'd', 'l']
    cleaned_list = []
    
    for order in list_orders:
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

    number_orders = len(cleaned_list_2)
    #print(cleaned_list_2[0], ' this is the cleaneed ;list 2 and not an int')

    for index_order in range(0, number_orders , 3):
        square_id = (int(cleaned_list_2[int(index_order)]) -1 ) + (int(cleaned_list_2[index_order + 1]) - 1 ) * map_dimension_row
        print(square_id)
        #rint(square_id)
        if cleaned_list_2[index_order+2] == 'l':
            #print(map_position[square_id][3], 'THIS IS THE SOURCE OF ALL EVIL')
            if map_position[square_id][3] != None:
                if ant_dict[map_position[square_id][3]]['earth'] == 0 and map_position[square_id][4] != 0:
                    weight_lift = map_position[square_id][4]
                    ant_dict[map_position[square_id][3]]['earth'] =  weight_lift
                    #now its picked up and should dissapear from the map
                    map_position[square_id][4] = 0 
                    #print('NICE LIFT BRO')
                    #print(ant_dict)


        elif cleaned_list_2[index_order+2] == 'd':
            
            if ant_dict[map_position[square_id][3]]['earth'] != 0 and map_position[square_id][4] == 0:
                
                weight_carry = ant_dict[map_position[square_id][3]]['earth']
                map_position[square_id][4] = weight_carry
                #now its picked up and should dissapear from the map
                ant_dict[map_position[square_id][3]]['earth'] = 0 

    for coordinat in cleaned_list_2:
        used_orders.append(coordinat)
        

def ant_spawn(player_dict, level_ant_1, level_ant_2, ant_dict, map_position, anthills_square_ids):
    """
    This function serves to spawn a new ant when all other orders
    have been executed. It takes the dico_1 as parameter in order
    to obtain the level of the anthill to spawn the correct level ant.
    
    Parameters :
    ------------
    player_dict : dictionnary with players info (dict)
    level_ant_1 : level of which the ant should spawn as (int)
    level_ant_2 : level of which the ant should spawn as (int)
    ant_dict : dict containing ants info (dict)
    map_position : list containing all infos on the entities on the map (list)

    :return:
    new_ant : add a new list in the dico_2 (list)
    Version :
    ---------
    Specification : Julien Emegenbirn (v1. 19/02/2021)
    """
    ant_counter = len(ant_dict)

    

    if (player_dict[1]['nb_turns'])%5 == 0 and (player_dict[2]['nb_turns'])%5 == 0:
        #condtition for new ant to spawn is fullfilled

        if map_position[anthills_square_ids[0]][3] == None:
            ant_counter += 1
            ant_name = 'Ant-%s' % ant_counter
            ant_dict['%s'%ant_name] = {'level' : level_ant_1, 'health' : 3, 'earth' : 0, 'square_id' : anthills_square_ids[0], 'owner' : 1}
            map_position[anthills_square_ids[0]][3] = ant_name

        if map_position[anthills_square_ids[1]][3] == None:
            ant_counter += 1
            ant_name = 'Ant-%s' % ant_counter
            ant_dict['%s'%ant_name] = {'level' : level_ant_2, 'health' : 3, 'earth' : 0, 'square_id' : anthills_square_ids[1], 'owner' : 2}
            map_position[anthills_square_ids[1]][3] = ant_name

    print(level_ant_1, 'this is level ant')


def ant_level(anthills_square_ids, map_position, player_dict, ant_dict):
    """
    This will check how many squares of earth are around the anthill of the player. 
    This is used to see if the player has won i.e. if he has all 8 spots around him filled with earth but
    also to determin the level of spawning ants. It takes the list of position as parameter and returns the 
    amount of filled spots and the level of the new spawning ant.
    
    Parameters:
    -----------
    anthills_square_ids : list of square id of both in order to find if the squares surrounding it are filled or not (list)
    map_position : list containing position of all entities on the map (list)
    player_dict : dictionnary cointaining all infos related to the player itself (dict)
    ant_dict ; dict containing ant info needed for the ant_spawn function within it (dict)
    
    :return:
    full_cases : number of cases with a motte (int)
    ant_spawn_level : level of the new ant (int)
    
    Version :
    Specification : Julien Emegenbirn (v1. 19/02/2021)
    ---------
    """
    map_dimension_row = map_position[-1][1]  
    anthill_id_1 = anthills_square_ids[0]
    
    anthill_id_2 = anthills_square_ids[1]

    #print(anthill_id_1, anthill_id_2)

    coord_anthill_1 = []
    coord_anthill_2 = []

    #this next bit of code should caculate the position of the squares around it and check if theyre filled

    #right left value

    # THIS IS FOR PLAYER ONE

    coord_anthill_1.append(anthill_id_1)
    coord_anthill_1.append(anthill_id_1)
    #top then left right from the top position pov
    coord_anthill_1.append(anthill_id_1-map_dimension_row)
    coord_anthill_1.append(coord_anthill_1[2]-1 )
    coord_anthill_1.append(coord_anthill_1[2]+1 )
    #bottom then left and right
    coord_anthill_1.append(anthill_id_1+map_dimension_row)
    coord_anthill_1.append(coord_anthill_1[5]-1 )
    coord_anthill_1.append(coord_anthill_1[5]+1 )    

    # THIS IS FOR PLAYER TWO 


    coord_anthill_2.append(anthill_id_2)
    coord_anthill_2.append(anthill_id_2)
    #top then left2right from the top position pov
    coord_anthill_2.append(anthill_id_2-map_dimension_row)
    coord_anthill_2.append(anthill_id_2-map_dimension_row-1 )
    coord_anthill_2.append(anthill_id_2-map_dimension_row+1 )
    #bottom then l2ft and right
    coord_anthill_2.append(anthill_id_2+map_dimension_row)
    coord_anthill_2.append(anthill_id_2+map_dimension_row-1 )
    coord_anthill_2.append(anthill_id_2+map_dimension_row+1 )    
    #print(coord_anthill_2)

    # THIS ITERATE THROUGH THE SQUARE IDS TO CHECK IF WEIGHT I ABOVE 0
    anthill_1_earth = []
    anthill_2_earth = []

    for element_id in range(8):
        
        if map_position[coord_anthill_1[element_id]][4] > 0:
            anthill_1_earth.append(True)
        if map_position[coord_anthill_2[element_id]][4] > 0:
            anthill_2_earth.append(True)

    #print(anthill_2_earth)
    player_level_1 = 0
    for element_bool_1 in anthill_1_earth:
        if element_bool_1 == True:
            player_level_1 += 1

    player_level_2 = 0
    for element_bool_2 in anthill_2_earth:
        if element_bool_2 == True:
            player_level_2 += 1

    print('player level', player_level_1)
    print(anthill_1_earth)

    if player_level_1 <= 2:
        level_ant_1 = 1
    elif  player_level_1 <= 5:
        level_ant_1 = 2
    else:
        level_ant_1 = 3    


    if player_level_2 <= 2:
        level_ant_2 = 1
    elif  player_level_2 <= 5:
        level_ant_2 = 2
    else:
        level_ant_2 = 3  
    


    player_dict[1]['level'] = player_level_1
    player_dict[2]['level'] = player_level_2
    

    ant_spawn(player_dict, level_ant_1, level_ant_2, ant_dict, map_position, [anthill_id_1, anthill_id_2])
    
    return (player_level_1, player_level_2) , (level_ant_1, level_ant_2)



def ai_decision(ant_dict , map_position, anthill, anthill_1):
    

    map_dimension_row = map_position[-1][1]
    row_anthill = anthill // map_dimension_row +1
    col_anthill = anthill % map_dimension_row +1
    if anthill == anthill_1:
        player_now = '1'
    else:
        player_now = '2'
    
    

    direction = (' ', 'N','NE','E','SE','S','SO','O','NO')
    grid_x = map_position[-1][0]
    
    grid_y =  map_position[-1][1]
    order_ai = ''

    target_empty=False
    while not target_empty:
        
        for ant_name in ant_dict:
            if str(ant_dict[ant_name]['owner']) == player_now:
                order_executed = False
                num = randint(0,len(direction)-1)


                index_id = ant_dict[ant_name]['square_id']  
                move_chance = randint(0, 100)
                ys = map_position[index_id ][1] 
                xs = map_position[index_id ][0] 

                xt, yt = xs, ys
                distance_anthill = tchebyshev((xs, col_anthill, ys, row_anthill))

                if map_position[index_id][4] > 0 and (distance_anthill[0] > 1 or distance_anthill[1] > 1):               
                    string_order ='%s-%s:lift ' % (xs, ys)
                    order_ai += string_order
                    order_executed = True 

                if ((distance_anthill[0] == 1 and distance_anthill[1] == 1) or (distance_anthill[0] == 0 and distance_anthill[1] == 1) or (distance_anthill[0] == 1 and distance_anthill[1] == 0)) and ant_dict[ant_name]['earth'] > 0 and map_position[ant_dict[ant_name]['square_id']] != anthill and map_position[ant_dict[ant_name]['square_id']][4] == 0:

                    string_order = '%s-%s:drop ' % (xs, ys)
                    order_ai += string_order
                    order_executed = True

                if ant_dict[ant_name]['earth'] > 0:
                    net_difference_row = row_anthill - ys
                    net_difference_col = col_anthill - xs
                    
                    if abs(net_difference_row) != 1 and abs(net_difference_col) != 1:
                        
                        if net_difference_col == 0 and net_difference_row < 0:
                            if yt > 1 : yt-=1
                        elif net_difference_col > 0 and net_difference_row < 0:
                            if xt < grid_x : xt+=1
                            if yt > 1 : yt-=1
                        elif net_difference_col > 0 and net_difference_row == 0:
                            if xt < grid_x : xt+=1
                        elif net_difference_col > 0 and net_difference_row > 0:
                            if xt < grid_x :  xt+=1
                            if yt < grid_y  : yt+=1
                        elif net_difference_col == 0 and net_difference_row > 0:
                            if yt < grid_y : yt+=1
                        elif net_difference_col < 0 and net_difference_row > 0:
                            if xt > 1 : xt-=1
                            if yt < grid_y : yt+=1
                        elif net_difference_col < 0 and net_difference_row == 0:
                            if xt > 1 : xt-=1
                        elif net_difference_col < 0 and net_difference_row < 0 :
                            if xt > 1 : xt-=1
                            if yt > 1 : yt-=1
                        string_order = '%s-%s:@%s-%s ' % (xs, ys, xt, yt)
                        order_ai += string_order
                        order_executed = True

                for ant_nb in ant_dict:
                    id_square_ant = ant_dict[ant_nb]['square_id']
                    row_ant = map_position[id_square_ant][1]
                    col_ant = map_position[id_square_ant][0]
                    if str(ant_nb) != str(ant_name):

                        #if ant_dict[ant_name]['owner'] != ant_dict[ant_nb]['owner']:

                        if thebyshev_distance((xs, ys), (col_ant, row_ant)) == True:
                            if ant_dict[ant_nb]['owner'] != ant_dict[ant_name]['owner']:
                                if ant_dict[ant_nb]['health'] > 0:
                                    string_order = '%s-%s:*%s-%s ' % (xs, ys,col_ant, row_ant)
                                    order_ai += string_order

                
                if move_chance < 85 and order_executed == False:

                    if direction[num] == 'N' :
                        if yt > 1 : yt-=1
                    elif direction[num] == 'NE' :
                        if xt < grid_x : xt+=1
                        if yt > 1 : yt-=1
                    elif direction[num] == 'E' :
                        if xt < grid_x : xt+=1
                    elif direction[num] == 'SE' :
                        if xt < grid_x :  xt+=1
                        if yt < grid_y  : yt+=1
                    elif direction[num] == 'S' :
                        if yt < grid_y : yt+=1
                    elif direction[num] == 'SO' :
                        if xt > 1 : xt-=1
                        if yt < grid_y : yt+=1
                    elif direction[num] == 'O' :
                        if xt > 1 : xt-=1
                    elif direction[num] == 'NO' :
                        if xt > 1 : xt-=1
                        if yt > 1 : yt-=1
                    string_order = '%s-%s:@%s-%s ' % (xs, ys, xt, yt)
                    order_ai += string_order
                
        #print(order_ai)
        return order_ai

def colour_map(map_position, anthill_1, anthill_2, ant_dict):
    map_dimension_row = map_position[-1][1] 
    map_dimension_col = map_position[-1][0]  
    y = 8
    for i in range(map_dimension_row):
        x = 50
        print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ') 
        y += 1
        print(term.move_xy(x, y) + term.sienna4("||   ||"), end=' ')
        y += 1
        print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ')
        y += 0
    

        for i in range(map_dimension_col -1):
            x += 5
            y -= 2
            print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ')
            y += 1
            print(term.move_xy(x, y) + term.sienna4("||   ||"), end=' ')
            y += 1
            print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ')

    y = 7
    x = 53
    for count_col in range(1, map_dimension_col + 1):
        
        print(term.move_xy(x, y) + term.sienna4("%s"% count_col), end=' ')
        x += 5

    y = 9
    x = 48
    for count_row in range(1, map_dimension_col + 1):
        
        print(term.move_xy(x, y) + term.sienna4("%s"% count_row), end=' ')
        y += 2    



    #compteur_point_tour    
    print(term.move_xy(75, 2) + term.sienna4("x====================================================x"), end=' ') 
    print(term.move_xy(75, 3) + term.sienna4("||                        ||                        ||"), end=' ')
    print(term.move_xy(75, 4) + term.sienna4("x====================================================x"), end=' ')
    print(term.move_xy(90, 5) + term.sienna4("||                  ||"), end=' ')
    print(term.move_xy(90, 6) + term.sienna4("x====================x"), end=' ')


    print(term.move_xy(175, 6) + term.sienna4("x=======PLAYER 1=======x"), end=' ')
    print(term.move_xy(230, 6) + term.sienna4("x=======PLAYER 2=====x"), end=' ')

    
    

    health_1 = 'Progress: [▮ ]'
    health_2 = 'Progress: [▮▮ ]'
    health_3 = 'Progress: [▮▮▮ ]'
    health_4 = 'Progress: [▮▮▮▮ ]'
    health_5 = 'Progress: [▮▮▮▮▮ ]'
    health_6 = 'Progress: [▮▮▮▮▮▮ ]'
    health_7 = 'Progress: [▮▮▮▮▮▮▮ ]'

    earth_1 = '🚫'
    earth_2 =  '💿'
    earth_3 = '📀'

    ant_on_anthill_1 = map_position[anthill_1][3]
    ant_on_anthill_2 = map_position[anthill_2][3]

    #this is the code which transaltes it into the map colours and UTF-8

    for u in range(len(map_position)):
        

        
        if map_position[u][3] == None:
            map_position[u][3] = ' '
        else: 
            map_position[u][3] = '🐜'

        if u == int(anthill_1) and ant_on_anthill_1 == None:
            map_position[u][3] = "\U0001F3E1"

        

      
        if map_position[u][4] == 1:
            map_position[u][4] = '🚫' 
        elif map_position[u][4] == 2:
            map_position[u][4] = '💿'
        elif map_position[u][4] == 3:
            map_position[u][4] ='📀'
       
       
    #this is the code which prints everything on the screen

    #this shows the healthbar of the ants
    
    y_health = 10
    for i in range(1, len(ant_dict)+1):
        
       

        if ant_dict['Ant-%s'%i]['health'] > 0:
            if int(ant_dict['Ant-%s'%i]['owner']) == 1:
                x_health = 175
                ant_health =  int(ant_dict['Ant-%s'%i]['health'])
                if ant_health == 1:
                    health_showed = health_1
                elif ant_health == 2:
                    health_showed = health_2
                elif ant_health == 3:
                    health_showed = health_3
                elif ant_health == 4:
                    health_showed = health_4
                elif ant_health == 5:
                    health_showed = health_5
                elif ant_health == 6:
                    health_showed = health_6
                elif ant_health == 7:
                    health_showed = health_7

                if term.does_styling:
                    with term.location(x_health, y_health):
                        
                        print(term.blue(health_showed))
                
            
            if int(ant_dict['Ant-%s'%i]['owner']) == 2:
                x_health = 230
                
                ant_health =  int(ant_dict['Ant-%s'%i]['health'])
                if ant_health == 1:
                    health_showed = health_1
                elif ant_health == 2:
                    health_showed = health_2
                elif ant_health == 3:
                    health_showed = health_3
                elif ant_health == 4:
                    health_showed = health_4
                elif ant_health == 5:
                    health_showed = health_5
                elif ant_health == 6:
                    health_showed = health_6
                elif ant_health == 7:
                    health_showed = health_7

                if term.does_styling:
                    with term.location(x_health, y_health - 1):
                        print(term.red(health_showed))
                
        y_health += 1



   
    i = 0 #numlist
    j = 3 #utf8
   
    y = 7
    for i in range(map_dimension_row):
        x = 47
        y += 2
        for k in range(map_dimension_row):
            x+= 5
            idk = (i * map_dimension_row) + k
            if  map_position[idk][j] == '🐜':
                for ants_in_dict in ant_dict:
                    if int(ant_dict[ants_in_dict]['square_id']) == idk and int(ant_dict[ants_in_dict]['health']) > 0 :
                        if int(ant_dict[ants_in_dict]['owner']) == 1:
                            if  int(ant_dict[ants_in_dict]['level']) == 1:
                                print(term.move_xy(x, y) + term.on_aqua('🐜'), end=' ')
                            elif int(ant_dict[ants_in_dict]['level']) == 2:
                                print(term.move_xy(x, y) + term.on_deepskyblue3('🐜'), end=' ')
                            elif int(ant_dict[ants_in_dict]['level']) == 3:
                                print(term.move_xy(x, y) + term.on_navy('🐜'), end=' ')

                        if int(ant_dict[ants_in_dict]['owner']) == 2:
                            if  int(ant_dict[ants_in_dict]['level']) == 1:
                                print(term.move_xy(x, y) + term.on_indianred1('🐜'), end=' ')
                            elif int(ant_dict[ants_in_dict]['level']) == 2:
                                print(term.move_xy(x, y) + term.on_firebrick1('🐜'), end=' ')
                            elif int(ant_dict[ants_in_dict]['level']) == 3:
                                print(term.move_xy(x, y) + term.on_firebrick4('🐜'), end=' ')
                                
            if map_position[idk][j] == "\U0001F3E1":                     
                print(term.move_xy(x, y) + map_position[idk][j], end=' ')
            if map_position[idk][4] != 0:
                if map_position[idk][4] != '🐜' and map_position[idk][3] != '🐜': 
                    print(term.move_xy(x, y) + map_position[idk][4], end=' ')


    
    #this translates back to usable data

    for jk in range(len(map_position)):
        if map_position[jk][3] == ' ':
            map_position[jk][3] = None
        elif map_position[jk][3] == '🐜':
            for ij in range(1, len(ant_dict) + 1):
                ant_index = 'Ant-%s' % ij
                if ant_dict[ant_index]['square_id'] == jk:
                    if ant_dict['Ant-%s' % ij]['health'] > 0:
                        map_position[jk][3] = ant_index
        else:
            map_position[jk][3] = None
            
        

        if map_position[jk][4] == earth_1:    
            map_position[jk][4] = 1   
        elif map_position[jk][4] == earth_2:
            map_position[jk][4] = 2
        elif map_position[jk][4] == earth_3:
            map_position[jk][4] = 3
        else:
            map_position[jk][4] = 0


    


def main_game_function(CPX_file, group_1, type_1, group_2, type_2):

    map_position = map_generator(CPX_file)
    anthill_1 = map_position[1] 
    anthill_2 = map_position[2] 
    map_position = map_position[0]
    used_orders = []

    #dictionnary 1
    player_dict = {1 : {'player_type' : str(type_1), 'nb_turns' : 0, 'spawn_level' : 1},
              2 : {'player_type' :  str(type_2), 'nb_turns' : 0, 'spawn_level' : 1}}

    #dictionnary 2
    ant_dict = {}

    anthill_1 = 0
    anthill_2 = 0

    anthill_1_earth = [False,False,False,False,True,False,False,False]
    anthill_1_earth = [False,False,False,False,True,False,False,False]

    attack_list = [[0, 0], [1, 1], [2, 2], [3, 3]]

    game_status = False
    while game_status == False:



    
        used_orders = []

        ant_level([anthill_1, anthill_2], map_position, player_dict, ant_dict)
        colour_map(map_position, anthill_1, anthill_2, ant_dict)
 

        give_orders(game_status, ant_dict, player_dict, map_position, anthill_1, anthill_2)
    
main_game_function((r'C:\Users\benny\OneDrive\Desktop\project ia\small3.cpx'), 1, 1, 1, 1)
    
