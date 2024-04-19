#quick script to copy xgids into xg and pull out the resulting analysis

import pyautogui
import pyperclip
import time

monitor_width, monitor_height = 1920, 1080
click_x = monitor_width // 2
click_y = monitor_height -1070 #should select right in the middle of extremegammon window

def click_xg():
    pyautogui.click(x = click_x, y = click_y)

def copy_position_from_xg():
    pyautogui.hotkey('ctrl','c')
    temp_pos = pyperclip.paste()
    return temp_pos

def paste_position_into_xg():
    pyautogui.hotkey('ctrl','v')
    pyautogui.hotkey('right', 'enter')

def copy_position_from_dataset(xgid):
    pyperclip.copy(xgid)

def analyze_position_in_xg():
    pyautogui.hotkey('ctrl', '5')
    time.sleep(2)
    

def parse_player_gammon_chances(temp_pos):
    gammon_chance = -1
    temp_pos = temp_pos.split('\r\n')
    for line in temp_pos:
        if 'Player Winning Chances' in line:
            pct_str = line[line.index('G:') + 2:line.index('G:') + 9]

            while not pct_str[-1].isdigit(): #because num could be different lengths, trim non numeric chars from end
                pct_str = pct_str[0:len(pct_str) - 1]
            
            gammon_chance = float(pct_str)
    return gammon_chance

def process_line(line):
    copy_position_from_dataset(line)
    paste_position_into_xg()
    analyze_position_in_xg()
    temp_pos = copy_position_from_xg()
    gammon_chance = parse_player_gammon_chances(temp_pos)
    return gammon_chance
    
def strip_data(data):
    ret_data = []
    for line in data:
        ret_data.append(line.strip())
    return ret_data

def main():
    click_xg()
    output_data = []
    filename_in = 'xgids.txt'
    filename_out = 'gammon_chances.txt'
    with open(filename_in, 'r') as my_file_in:
        data = my_file_in.readlines()
    data = strip_data(data)

    EP = 1
    GR = 8
    for line in data:
        temp_output = process_line(line)
        data_line = (str(GR) + "," + str(EP) + "," + str(temp_output))
        output_data.append(data_line)
        EP += 1
        if EP == 101:
            EP = 1
            GR -= 1


    with open(filename_out, 'w') as my_file_out:
        my_file_out.write('R,E,G\n')
        for gc in output_data:
            my_file_out.write(str(gc) + '\n')

main()

