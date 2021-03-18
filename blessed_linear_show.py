import blessed, random, time
term = blessed.Terminal()

# clear screen and hide cursor
print(term.home + term.clear + term.hide_cursor)

# define position of the symbol
row = int(2)
col = int(60)

# move cursor + change color of symbol + change color of background + symbol + back to normal
print(term.move_yx(row, col) + term.red + term.on_rosybrown2 + '●' + term.normal, end='', flush=True)

# move symbol forever
index_square = 1

start_index = 23
end_index = 48
print_bool = True 


orders = [(4,5)]

while True:
    # wait a fraction of second
    time.sleep(0.001)
    
    # move cursor + change color of symbol + change color of background + single space + back to normal
    if print_bool == True:
        print(term.move_yx(row, col) + term.on_skyblue + ' ' + term.normal, end='', flush=True)
    else:
        print(term.move_yx(row, col) + term.on_grey + ' ' + term.normal, end='', flush=True)

    # update position symbol
    #(-1,0) is up and (1,0) is down (0,1) is right and (0, -1) is left

    #random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))
    bounds = [10,20,30,40,50] 

    move = [0,1]
    if index_square%3 == 0 and index_square != 0:
        move = [0, 2]
    
    
    if index_square%48 == 0:
        end_index += 24*2
        start_index += 24*2
   
    if index_square%24 == 0:
        move = [2, 0]
        # this moves it down an notch
    elif index_square>start_index and index_square < end_index:
        move[1] = move[1]*-1
        if index_square%3 == 0 and index_square != 52:
            move = [0, -2]
    
    #now you have to stop the cursor in a place 

    if index_square%192 == 0:
        row = 2
        col = 60
        print_bool = False
        move = [0 ,0]
        #order_colour = input('') 
        

    
    index_square += 1
    
    row += move[0]
    if row < 0:
        row = 0
    if row >= term.height:
        row = term.height-1

    col += move[1]
    if col < 0:
        col = 0
    if col >= term.width:
        col = term.width-1

    fh = open(r'C:\Users\benny\OneDrive\Desktop\project ia\row_column_coord.txt', 'a')
    fh.write("%s , %s \n" % (row, col))

    fh.close
    
    # move cursor + change color of symbol + change color of background + symbol + back to normal
    #print(term.move_yx(row, col) + term.red + term.on_rosybrown2 + '●' + term.normal, end='', flush=True)

    
  #_______________________________________________________________________ 

import blessed
term = blessed.Terminal()

print(term.home + term.clear, end='') 

y = 8
for i in range(20):
    x = 50
    print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ') 
    y += 1
    print(term.move_xy(x, y) + term.sienna4("||   ||"), end=' ')
    y += 1
    print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ')
    y += 0
   
    
    for i in range(20):
        x += 5
        y -= 2
        print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ')
        y += 1
        print(term.move_xy(x, y) + term.sienna4("||   ||"), end=' ')
        y += 1
        print(term.move_xy(x, y) + term.sienna4("xx===xx"), end=' ')

        
#exemple   
print(term.move_xy(52, 9) + term.on_seagreen("🐜"), end=' ')
print(term.move_xy(57, 9) + term.sienna4("🐜"), end=' ')
print(term.move_xy(63, 11) + term.sienna4("☐"), end=' ')


#compteur_point_tour    
print(term.move_xy(75, 2) + term.sienna4("x====================================================x"), end=' ') 
print(term.move_xy(75, 3) + term.sienna4("||                        ||                        ||"), end=' ')
print(term.move_xy(75, 4) + term.sienna4("x====================================================x"), end=' ')
print(term.move_xy(90, 5) + term.sienna4("||                  ||"), end=' ')
print(term.move_xy(90, 6) + term.sienna4("x====================x"), end=' ')
