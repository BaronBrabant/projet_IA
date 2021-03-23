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


-----------------------------------------------------------------------------------------------
#V2
import blessed
term = blessed.Terminal()
map_position = [[0, 0, 1, None, 0], [1, 0, 2, 'Ant-1', 0], [2, 0, 3, None, 0], [3, 0, 4, None, 0], [4, 0, 5, None, 0], [5, 0, 6, None, 0], [6, 0, 7, None, 0], [7, 0, 8, None, 0], [8, 0, 9, None, 0], [9, 0, 10, None, 0], [10, 0, 11, None, 0], [11, 0, 12, None, 0], [12, 0, 13, None, 0], [13, 0, 14, None, 0], [14, 0, 15, None, 0], [15, 0, 16, None, 0], [16, 0, 17, None, 0], [17, 0, 18, None, 0], [18, 0, 19, None, 0], [19, 0, 20, None, 0], [0, 1, 21, None, 0], [1, 1, 22, None, 0], [2, 1, 23, None, 0], [3, 1, 24, None, 0], [4, 1, 25, None, 0], [5, 1, 26, None, 0], [6, 1, 27, None, 0], [7, 1, 28, None, 0], [8, 1, 29, None, 0], [9, 1, 30, None, 0], [10, 1, 31, None, 0], [11, 1, 32, None, 0], [12, 1, 33, None, 0], [13, 1, 34, None, 0], [14, 1, 35, None, 0], [15, 1, 36, None, 0], [16, 1, 37, None, 0], [17, 1, 38, None,
0], [18, 1, 39, None, 0], [19, 1, 40, None, 0], [0, 2, 41, None, 0], [1, 2, 42, None, 0], [2, 2, 43, None, 0], [3, 2, 44, None, 0], [4, 2, 45, None, 0], [5, 2, 46, None, 0], [6, 2, 47, None, 0], [7, 2, 48, None, 0], [8, 2, 49, None, 0], [9, 2, 50, None, 0], [10, 2, 51, None, 0], [11, 2, 52, None, 0], [12, 2, 53, None, 0], [13, 2, 54, None, 0], [14, 2, 55, None, 0], [15, 2, 56, None, 0], [16, 2, 57,
None, 0], [17, 2, 58, None, 0], [18, 2, 59, None, 0], [19, 2, 60, None, 0], [0, 3, 61, None, 0], [1, 3, 62, None, 0], [2, 3, 63, None, 0], [3, 3, 64, 'Anthill\x01', 0], [4, 3, 65, None, 0], [5, 3, 66,
None, 0], [6, 3, 67, None, 0], [7, 3, 68, None, 0], [8, 3, 69, None, 0], [9, 3, 70, None, 0], [10, 3, 71, None, 0], [11, 3, 72, None, 0], [12, 3, 73, None, 0], [13, 3, 74, None, 0], [14, 3, 75, None, 0], [15, 3, 76, None, 0], [16, 3, 77, None, 0], [17, 3, 78, None, 0], [18, 3, 79, None, 0], [19, 3, 80, None, 0], [0, 4, 81, None, 0], [1, 4, 82, None, 0], [2, 4, 83, None, 0], [3, 4, 84, None, 0], [4,
4, 85, None, 0], [5, 4, 86, None, 0], [6, 4, 87, None, 0], [7, 4, 88, None, 0], [8, 4, 89, None, 0], [9, 4, 90, None, 0], [10, 4, 91, None, 0], [11, 4, 92, None, 0], [12, 4, 93, None, 0], [13, 4, 94, None, 0], [14, 4, 95, None, 0], [15, 4, 96, None, 0], [16, 4, 97, None, 0], [17, 4, 98, None, 0], [18, 4, 99, None, 0], [19, 4, 100, None, 0], [0, 5, 101, None, 0], [1, 5, 102, None, 0], [2, 5, 103, None, 0], [3, 5, 104, None, 0], [4, 5, 105, None, 0], [5, 5, 106, None, 0], [6, 5, 107, None, 0], [7, 5, 108, None, 0], [8, 5, 109, None, 0], [9, 5, 110, None, 0], [10, 5, 111, None, 0], [11, 5, 112, None, 0], [12, 5, 113, None, 0], [13, 5, 114, None, 0], [14, 5, 115, None, 0], [15, 5, 116, None, 0], [16, 5, 117, None, 0], [17, 5, 118, None, 0], [18, 5, 119, None, 0], [19, 5, 120, None, 0], [0, 6, 121, None, 0], [1, 6, 122, None, 0], [2, 6, 123, None, 0], [3, 6, 124, None, 0], [4, 6, 125, None, 0], [5, 6, 126, None, 0], [6, 6, 127, None, 0], [7, 6, 128, None, 0], [8, 6, 129, None, 0], [9, 6, 130, None, 0], [10, 6, 131, None, 0], [11, 6, 132, None, 0], [12, 6, 133, None, 0], [13, 6, 134, None, 0], [14, 6, 135, None, 0], [15, 6, 136, None, 0], [16, 6, 137, None, 0], [17, 6, 138, None, 0], [18, 6, 139, None, 0], [19, 6, 140, None, 0], [0, 7, 141, None, 0], [1, 7, 142, None, 0], [2, 7, 143, None, 0], [3, 7, 144, None, 0], [4, 7, 145, None, 0], [5, 7, 146, None, 0], [6, 7, 147, None, 0], [7, 7, 148, None, 0], [8, 7, 149, None, 0], [9, 7, 150, None, 0], [10, 7, 151, None, 0], [11, 7, 152, None, 0], [12, 7, 153, None, 0], [13, 7, 154, None, 0], [14, 7, 155, None, 0], [15, 7, 156, None, 0], [16, 7, 157, None, 0], [17, 7, 158, None, 0], [18, 7, 159, None, 0], [19, 7, 160, None, 0], [0, 8, 161, None, 0], [1, 8, 162, None, 0], [2, 8, 163, None, 0], [3, 8, 164, None, 0], [4, 8, 165, None, 0], [5, 8, 166, None, 0], [6, 8, 167, None, 0], [7, 8, 168, None, 0], [8, 8, 169, None, 0], [9, 8, 170, None, 0], [10, 8, 171, None, 0], [11, 8, 172, None, 0], [12, 8, 173, None, 0], [13, 8, 174, None, 0], [14,
8, 175, None, 0], [15, 8, 176, None, 0], [16, 8, 177, None, 0], [17, 8, 178, None, 0], [18, 8, 179, None, 0], [19, 8, 180, None, 0], [0, 9, 181, None, 0], [1, 9, 182, None, 0], [2, 9, 183, None, 0], [3, 9, 184, None, 0], [4, 9, 185, None, 0], [5, 9, 186, None, 0], [6, 9, 187, None, 0], [7, 9, 188, None, 0], [8, 9, 189, None, 0], [9, 9, 190, None, 1], [10, 9, 191, None, 1], [11, 9, 192, None, 1], [12, 9, 193, None, 1], [13, 9, 194, None, 0], [14, 9, 195, None, 0], [15, 9, 196, None, 0], [16, 9, 197, None, 0], [17, 9, 198, None, 0], [18, 9, 199, None, 0], [19, 9, 200, None, 0], [0, 10, 201, None, 0], [1, 10, 202, None, 0], [2, 10, 203, None, 0], [3, 10, 204, None, 0], [4, 10, 205, None, 0], [5, 10, 206, None, 0], [6, 10, 207, None, 0], [7, 10, 208, None, 0], [8, 10, 209, None, 0], [9, 10, 210, None, 1], [10, 10, 211, None, 1], [11, 10, 212, None, 1], [12, 10, 213, None, 1], [13, 10, 214, None, 0], [14, 10, 215, None, 0], [15, 10, 216, None, 0], [16, 10, 217, None, 0], [17, 10, 218, None, 0],
[18, 10, 219, None, 0], [19, 10, 220, None, 0], [0, 11, 221, None, 0], [1, 11, 222, None, 0], [2, 11, 223, None, 0], [3, 11, 224, None, 0], [4, 11, 225, None, 0], [5, 11, 226, None, 0], [6, 11, 227, None, 0], [7, 11, 228, None, 0], [8, 11, 229, None, 0], [9, 11, 230, None, 1], [10, 11, 231, None, 1], [11, 11, 232, None, 1], [12, 11, 233, None, 1], [13, 11, 234, None, 0], [14, 11, 235, None, 0], [15, 11, 236, None, 0], [16, 11, 237, None, 0], [17, 11, 238, None, 0], [18, 11, 239, None, 0], [19, 11, 240, None, 0], [0, 12, 241, None, 0], [1, 12, 242, None, 0], [2, 12, 243, None, 0], [3, 12, 244, None, 0], [4, 12, 245, None, 0], [5, 12, 246, None, 0], [6, 12, 247, None, 0], [7, 12, 248, None, 0], [8, 12, 249, None, 0], [9, 12, 250, None, 1], [10, 12, 251, None, 1], [11, 12, 252, None, 1], [12, 12, 253, None, 0], [13, 12, 254, None, 0], [14, 12, 255, None, 0], [15, 12, 256, None, 0], [16, 12, 257, None, 0], [17, 12, 258, None, 0], [18, 12, 259, None, 0], [19, 12, 260, None, 0], [0, 13, 261, None, 0], [1, 13, 262, None, 0], [2, 13, 263, None, 0], [3, 13, 264, None, 0], [4, 13, 265, None, 0], [5, 13, 266, None, 0], [6, 13, 267, None, 0], [7, 13, 268, None, 0], [8, 13, 269, None, 0], [9, 13, 270, None, 0], [10, 13, 271, None, 0], [11, 13, 272, None, 0], [12, 13, 273, None, 0], [13, 13, 274, None, 0], [14, 13, 275, None, 0], [15, 13, 276, None, 0], [16, 13, 277, None, 0], [17, 13, 278, None, 0], [18, 13, 279, None, 0], [19, 13, 280, None, 0], [0, 14, 281, None, 0], [1, 14, 282, None, 0], [2, 14, 283, None, 0], [3, 14, 284, None, 0], [4, 14, 285, None, 0], [5, 14, 286, None, 0], [6, 14, 287, None, 0], [7, 14, 288, None, 0], [8, 14, 289, None, 0], [9, 14, 290, None, 0], [10, 14, 291, None, 0], [11, 14, 292, None, 0], [12, 14, 293, None, 0], [13, 14, 294, None, 0], [14, 14, 295, None, 0], [15, 14, 296, None, 0], [16, 14, 297, None, 0], [17, 14, 298, None, 0], [18, 14, 299, None, 0], [19, 14, 300, None, 0], [0, 15, 301, None, 0], [1, 15, 302, None, 0], [2, 15, 303, None, 0], [3, 15, 304,
None, 0], [4, 15, 305, None, 0], [5, 15, 306, None, 0], [6, 15, 307, None, 0], [7, 15, 308, None, 0], [8, 15, 309, None, 0], [9, 15, 310, None, 0], [10, 15, 311, None, 0], [11, 15, 312, None, 0], [12,
15, 313, None, 0], [13, 15, 314, None, 0], [14, 15, 315, None, 0], [15, 15, 316, None, 0], [16, 15, 317, None, 0], [17, 15, 318, None, 0], [18, 15, 319, None, 0], [19, 15, 320, None, 0], [0, 16, 321, None, 0], [1, 16, 322, None, 0], [2, 16, 323, None, 0], [3, 16, 324, None, 0], [4, 16, 325, None, 0], [5, 16, 326, None, 0], [6, 16, 327, None, 0], [7, 16, 328, None, 0], [8, 16, 329, None, 0], [9, 16,
330, None, 0], [10, 16, 331, None, 0], [11, 16, 332, None, 0], [12, 16, 333, None, 0], [13, 16, 334, None, 0], [14, 16, 335, None, 0], [15, 16, 336, None, 0], [16, 16, 337, None, 0], [17, 16, 338, None, 0], [18, 16, 339, None, 0], [19, 16, 340, None, 0], [0, 17, 341, None, 0], [1, 17, 342, None, 0], [2, 17, 343, None, 0], [3, 17, 344, None, 0], [4, 17, 345, None, 0], [5, 17, 346, None, 0], [6, 17, 347, None, 0], [7, 17, 348, None, 0], [8, 17, 349, None, 0], [9, 17, 350, None, 0], [10, 17, 351, None, 0], [11, 17, 352, None, 0], [12, 17, 353, None, 0], [13, 17, 354, None, 0], [14, 17, 355, None, 0], [15, 17, 356, None, 0], [16, 17, 357, None, 0], [17, 17, 358, None, 0], [18, 17, 359, None, 0], [19, 17, 360, None, 0], [0, 18, 361, None, 0], [1, 18, 362, None, 0], [2, 18, 363, None, 0], [3, 18, 364, None, 0], [4, 18, 365, None, 0], [5, 18, 366, None, 0], [6, 18, 367, None, 0], [7, 18, 368, None, 0], [8, 18, 369, None, 0], [9, 18, 370, None, 0], [10, 18, 371, None, 0], [11, 18, 372, None, 0], [12, 18, 373, None, 0], [13, 18, 374, None, 0], [14, 18, 375, None, 0], [15, 18, 376, None, 0], [16, 18, 377, None, 0], [17, 18, 378, None, 0], [18, 18, 379, 'Anthill\x02', 0], [19, 18, 380, None, 0], [0, 19, 381, None, 0], [1, 19, 382, None, 0], [2, 19, 383, None, 0], [3, 19, 384, None, 0], [4, 19, 385, None, 0], [5, 19, 386, None, 0], [6, 19, 387, None, 0], [7, 19, 388, None, 0], [8, 19, 389, None,
0], [9, 19, 390, None, 0], [10, 19, 391, None, 0], [11, 19, 392, None, 0], [12, 19, 393, None, 0], [13, 19, 394, None, 0], [14, 19, 395, None, 0], [15, 19, 396, None, 0], [16, 19, 397, None, 0], [17, 19, 398, None, 0], [18, 19, 399, 'Ant-1', 1], [19, 19, 400, 'Ant-2', 0]]
x = 52
y = 9
for coord in map_position:
    y += 2 
    x += 5
    coord[0] = y
    coord[1] = x


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


list_x = []
list_y = []

for i in range (10):
    if map_position[i][0] != None and 'Anthill\x01' and 'Anthill\x02':
        list_x.append(map_position[i][0])
        list_y.append(map_position[i][1])
for i in range(len(list_x)):
    print(term.move_xy(list_x[i], list_y[i]) + term.on_seagreen("🐜"), end=' ')

        
#exemple   

#print(term.move_xy(57, 9) + term.sienna4("🐜"), end=' ')
#print(term.move_xy(63, 11) + term.sienna4("☐"), end=' ')





#compteur_point_tour    
print(term.move_xy(75, 2) + term.sienna4("x====================================================x"), end=' ') 
print(term.move_xy(75, 3) + term.sienna4("||                        ||                        ||"), end=' ')
print(term.move_xy(75, 4) + term.sienna4("x====================================================x"), end=' ')
print(term.move_xy(90, 5) + term.sienna4("||                  ||"), end=' ')
print(term.move_xy(90, 6) + term.sienna4("x====================x"), end=' ')

