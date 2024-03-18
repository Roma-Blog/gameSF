import os, random
from sys import platform

playing_field = [
    ["-","-","-"],
    ["-","-","-"],
    ["-","-","-"]
]
my_char = None
ai_char = ''

step = 0

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
    coordinates = input(f"Напишите координаты (два числа столбец|строка) куда поставить {my_char}: ")

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
        print("Коррдинаты нужно писать так, дава числа: 01 (столбец|строка)")
        Input_coordinates()

def Win(char):
    if Check_Row(char) or Check_Columns(char) or Check_Diagonal(char, 1) or Check_Diagonal(char, -1):
        return True

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

def Win_Strategy(): 
    if Check_Row(ai_char) or Check_Columns(ai_char) or Check_Diagonal(ai_char, 1) or Check_Diagonal(ai_char, -1):
        return True

def Protect_Strategy():
    if Check_Row(my_char) or Check_Columns(my_char) or Check_Diagonal(my_char, 1) or Check_Diagonal(my_char, -1):
        return True

def Check_Row(char):
    num_row = 0
    while num_row < 3:
        if playing_field[num_row].count(char) == 3:
            return 'Win'
        elif playing_field[num_row].count(char) == 2 and playing_field[num_row].count('-') == 1:
            Insert_Char_Row(num_row)
            return True
        num_row += 1

def Check_Columns(char):
    num_col = 0

    while num_col < 3:
        count_char, dash_char, num_row= 0, 0, 0

        while num_row < 3:
            if playing_field[num_row][num_col] == char:
                count_char += 1
            elif playing_field[num_row][num_col] == '-':
                dash_char += 1
            num_row += 1

        if count_char == 3:
            return 'Win'
        elif count_char == 2 and dash_char == 1:
            Insert_Char_Col(num_col)
            return True
        num_col += 1

def Check_Diagonal(char, dir):
    num_col = -1 if dir < 0 else 0
    num_row, dash_char, count_char = 0, 0, 0
    
    while num_row < 3:
        if playing_field[num_row][num_col] == char:
            count_char += 1
        elif playing_field[num_row][num_col] == '-':
            dash_char += 1
        num_row += 1
        num_col += 1 * dir
    
    if count_char == 3:
        return 'Win'
    elif count_char == 2 and dash_char == 1:
        Insert_Char_Diagonal(dir)
        return True

def AI_step():
    Win_Strategy() or Protect_Strategy() or Random_Step(random.randrange(0, 3),random.randrange(0, 3))
    Draw_playing_field(playing_field)




Clear_Console()
Start_Game()
Draw_playing_field(playing_field)

while True:
    if my_char == "0":
        Input_coordinates()
        if Win(my_char):
            print("Вы победили!")
        AI_step()
    else:
        AI_step()
        Input_coordinates()

