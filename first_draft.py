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




give_orders(False)



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
