def ant_level(list_2):
    """
    This will check how many squares of earth are around the anthill of the player. 
    This is used to see if the player has won i.e. if he has all 8 spots around him filled with earth but
    also to determin the level of spawning ants. It takes the list of position as parameter and returns the 
    amount of filled spots and the level of the new spawning ant.
    
    Parameters:
    -----------
    list_2 : list of cases around the spawn point where are motte or not (list)
    
    :return:
    full_cases : number of cases with a motte (int)
    ant_spawn_level : level of the new ant (int)
    
    Version :
    Specification : Julien Emegenbirn (v1. 19/02/2021)
    ---------
    """

def motte_de_terre(dico_2):
    """
    This function serves to pickup and drop a piece of earth. 
    It takes the dico_2 as paramter to establish whether the ant is already carrying something or not.
    
    Parameters :
    ------------
    dico_2 : The third elements of all the list in the dictionary (bool)
    
    :return:
    ant_charge : If the ant as already a motte (bool)
    Version :
    ---------
    Specification : Julien Emegenbirn (v1. 19/02/2021)
    """

def ant_spawn(dico_1) :
    """
    This function serves to spawn a new ant when all other orders
    have been executed. It takes the dico_1 as parameter in order
    to obtain the level of the anthill to spawn the correct level ant.
    
    Parameters :
    ------------
    dico_1 : the third element of the list for every key (int)
    
    :return:
    new_ant : add a new list in the dico_2 (list)
    Version :
    ---------
    Specification : Julien Emegenbirn (v1. 19/02/2021)
    """

def tchebyshev() :
    """
    This function calculates the Tchebyshev distance
    
    parameters :
    ------------

    return:
    tchebyshev_distance : (tuple)
    version :
    ---------
    spécification : Frédéric Sauvage (v1. 21/02/21)
    """
def thebyshev_distance(list_1,Tchebyshev) :
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
def ant_attack (tchebyshev_distance,dico_2) :
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

    def colour_code_map(dico2, list_position_earth):
    '''
    This function adds a colour code to the background of one game square to 
    tell the player if the ant, which is on top of a piece of earth, 
    has the ability to lift the piece of earth or not.

    Parameters
    __________

    dico2 : dictionnary containting list filled with infomation on ants (list1)
    list1[0] : contains force of ants to determin their strength to carry earth (int)
    list1[1] : contains boolean value determining if the ant is already carrying something (bool)
    list_position_earth : list containing all pieces of earth (list)

    Return
    ______ 

    allowed_or_not : boolean value determining if the piece of earth can be picked up (bool)


    version : v1
    ---------
    spécification : Benjamin Richter (v1. 21/02/21)
    '''

 
def movement(dico2, list_position_earth, movement_input):
    '''
    This function will take the desired movement_input, will check if the inputed position of the wanted ant is correct by checking
    its position in the list_position_earth and will finally allow the player to move its ant to the desired position if it does 
    not infringe any game rules such as moving onto a squre filled with earth while already carrying some through the dico2.
    If the movement is succesful the list inputed as the list_position_earth will be updated with the new game coordinates.

    Parameters
    __________

    dico2 : dictionary containing information on the ant such as its health and if it is carrying earth or not (dict)
    list_position_earth : this is the list containing information on what is happening on every square of the map (list)
    movement_input : this will be a string under the format r1-c1:*r2-c2 where as many of those orders can be inputed simultaneously as wanted(str)
    
    version : v1
    ---------
    spécification : Benjamin Richter (v1. 21/02/21)
    '''


def give_orders(game_status,orders):
    '''
    This will be the sole function with an input and will serve as an interface for the game to give all orders at the same time.
    These will be chains of characters which if formated correctly in the form r1-c1:*r2-c2, r1-c1:@r2-c2, r1-c1:lift or r1-c1:drop will be 
    interpreted by the game to execute orders and send the order to the correct function to be executed.

    Parameters
    __________

    game_status : this is a boolean value to determin if the game is over or not (bool)
    orders : string of charcaters which will be translated to orders (str)

    version : v1
    ---------
    spécification : Benjamin Richter (v1. 21/02/21)
    '''
