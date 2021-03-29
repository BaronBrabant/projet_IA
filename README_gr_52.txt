You'll need to intitialize the map before you can play, you can do this by giving the full path
of the .cpx file as parameter to the map_generator() function.
This code only works for the small.cpx file for now.
Once the file path is included you can launch the game.

The first order should be a blank statement aka. not giving an order and the map will load itself.

When the game is launched, you can give the ants instructions in the following format:

move : 
ex: 18-19:@19-19 #the ant who is in 18-19 will move to the case 19-19.

attack:
ex: 18-19:* 19-19 # the ant who is in 18-19 will attack the end in 19-19.

lift a motte :
ex: 18-19: lift #the ant who is in 18-19 will take the motte who is in the case 18-19.

drop a motte :
ex: 18-19: drop #the ant who is in 18-19 will drop the motte on the case 18-19
