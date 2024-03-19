import os, random
from sys import platform

playing_field = [
    ["-","-","-"],
    ["-","-","-"],
    ["-","-","-"]
]
my_char = None
ai_char = ''

game = True

def Clear_Console():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "win32":
        clear = lambda: os.system('cls')
        clear()


def Draw_playing_field(pf):
    Clear_Console()
    print('  0 1 2')
    for row in range(3):
        print('{} {} {} {}'.format(row ,*pf[row]))
    print('')

def Start_Game():
    global my_char, ai_char
    my_char = input('Введите символ, за кого хотите играть  X/0:  ').upper()
    ai_char = '0' if my_char == 'X' else 'X'
    if (not my_char == "X" and not my_char == "0"):
        print("Введите только указанные символы")
        Start_Game()

def Input_coordinates():
    global my_char
    print("-------------------------------------------")
    coordinates = input(f"Напишите координаты (два числа строка|столбец) куда поставить {my_char}: ")

    try:
        chek_num = all(int(i) < 3 and int(i) > -1 for i in coordinates)
    except ValueError:
        print("!!!Вводите только числа")
        return
    
    if len(coordinates) == 2 and chek_num:
        if playing_field[int(coordinates[0])][int(coordinates[1])] == "-":
            playing_field[int(coordinates[0])][int(coordinates[1])] = my_char
            Draw_playing_field(playing_field)
        else:
            print("Ячейка занята")
            Input_coordinates()
            return
    else:
        print("Коррдинаты нужно писать так, дава числа: 01 (строка|столбец)")
        Input_coordinates()

def Win(char):
    if Check_Row(char, 3) or Check_Columns(char, 3) or Check_Diagonal(char, 1, 3) or Check_Diagonal(char, -1, 3):
        return True

def Stop_Game(message):
    global game
    game = False
    Clear_Console()
    Draw_playing_field(playing_field)
    print("-----------------------------------------")
    print(message)
    print("-----------------------------------------")

def Check_Drawn_Game():
    dash_char = 0
    for item in playing_field:
        dash_char += item.count('-')
    if dash_char <= 1: return True

###################################### AI ###########################################################

def Random_Step(x, y):
    if playing_field[x][y] == '-':                
        playing_field[x][y] = ai_char
        return True
    else:
        Random_Step(random.randrange(0, 3),random.randrange(0, 3))

def Insert_Char_Row(num_row):
    playing_field[num_row] = [ai_char if item == "-" else item for item in playing_field[num_row]]

def Insert_Char_Col(num_col):
    num_row = 0
    while num_row < 3:
        if playing_field[num_row][num_col] == "-":
            playing_field[num_row][num_col] = ai_char
        num_row += 1

def Insert_Char_Diagonal(dir):
    num_col = -1 if dir < 0 else 0
    num_row = 0
    
    while num_row < 3:
        if playing_field[num_row][num_col] == "-":
            playing_field[num_row][num_col] = ai_char
        num_row += 1
        num_col += 1 * dir

def Strategy(char): 
    check_row = Check_Row(char, 2, 1)
    check_col = Check_Columns(char, 2, 1)
    check_diag = Check_Diagonal(char, 1, 2, 1) or Check_Diagonal(char, -1, 2, 1)

    if check_row != None:
        Insert_Char_Row(check_row)
        return True
    elif check_col != None:
        Insert_Char_Col(check_col)
        return True
    elif check_diag != None:
        Insert_Char_Diagonal(check_diag)
        return True
    return False

def Check_Row(char, count, dash_char = 0):
    num_row = 0
    
    while num_row < 3:
        if playing_field[num_row].count(char) == count and playing_field[num_row].count('-') == dash_char:
            return num_row
        num_row += 1


def Check_Columns(char, count, dash_char = 0):
    num_col = 0

    while num_col < 3:
        count_char, dch, num_row= 0, 0, 0

        while num_row < 3:
            if playing_field[num_row][num_col] == char:
                count_char += 1
            elif playing_field[num_row][num_col] == '-':
                dch += 1
            num_row += 1

        if count_char == count and dch == dash_char:
            return num_col
        num_col += 1

def Check_Diagonal(char, dir, count, dash_char = 0):
    num_col = -1 if dir < 0 else 0
    num_row, dch, count_char = 0, 0, 0
    
    while num_row < 3:
        if playing_field[num_row][num_col] == char:
            count_char += 1
        elif playing_field[num_row][num_col] == '-':
            dch += 1
        num_row += 1
        num_col += 1 * dir
    
    if count_char == count and dch == dash_char:
        return dir

def AI_step():
    Strategy(ai_char) or Strategy(my_char) or Random_Step(random.randrange(0, 3),random.randrange(0, 3))
    Draw_playing_field(playing_field)

Clear_Console()
Start_Game()
Draw_playing_field(playing_field)

while game:
    if my_char == "0":
        Input_coordinates()
        if Check_Drawn_Game():
            Stop_Game("Ничья!!!")
            break
        elif Win(my_char):
            Stop_Game("Вы победили!!!")
            break
        AI_step()
        if Win(ai_char):
            Stop_Game("Компьютер победил!!!")
            break
    else:
        AI_step()
        if Check_Drawn_Game():
            Stop_Game("Ничья!!!")
            break
        elif Win(ai_char):
            Stop_Game("Компьютер победил!!!")
            break
        Input_coordinates()
        if Win(my_char):
            Stop_Game("Вы победили!!!")
            break