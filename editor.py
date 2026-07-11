import re

data = []  # Store content as lines
cur_line = 0     
cur_index = 0
inputs = None
cur_cmd = None
cur_text = None
row_cursor = False
line_cursor = False
states = []
last_valid_inputs = []
clipboard = None 


def print_help():
    print(
            "? - display this help info",
            ". - toggle row cursor on and off",
            "; - toggle line cursor on and off",
            "h - move cursor left",
            "j - move cursor up",
            "k - move cursor down",
            "l - move cursor right",
            "^ - move cursor to beginning of the line",
            "$ - move cursor to end of the line",
            "w - move cursor to beginning of next word",
            "b - move cursor to beginning of previous word",
            "i - insert <text> before cursor",
            "a - append <text> after cursor",
            "x - delete character at cursor",
            "dw - delete word and trailing spaces at cursor",
            "yy - copy current line to memory",
            "p - paste copied line(s) below line cursor",
            "P - paste copied line(s) above line cursor",
            "dd - delete line",
            "o - insert empty line below",
            "O - insert empty line above", 
            "u - undo previous command",
            "r - repeat last command",
            "s - show content",
            "q - quit program",
            sep="\n"                        # Set the separator to a newline character
            )


def copy_list_of_str(lst: list[str]) -> list[str]:
    return [s[:] for s in lst]

def store_state():
    global cur_cmd, cur_text, row_cursor, line_cursor, cur_line, cur_index, data
    if cur_cmd in ['?', 's', 'u']:
        return
    snapshot = (
        cur_cmd,
        cur_text,
        row_cursor,
        line_cursor,
        cur_line,
        cur_index,
        copy_list_of_str(data)
    )
    states.append(snapshot)

def load_state():
    global cur_cmd, cur_text, row_cursor, line_cursor, cur_line, cur_index, data
    if not states:
        # print("No previous state to restore.")
        return
    snapshot = states.pop()
    cur_cmd, cur_text, row_cursor, line_cursor, cur_line, cur_index, data = snapshot

def register_last_inputs(cmd, text):
    global last_valid_inputs
    if cmd in ['?', 's']:
        return
    last_valid_inputs.append((cmd, text))

def switch_row_cursor():
    global row_cursor
    row_cursor = not row_cursor

def switch_line_cursor():
    global line_cursor
    line_cursor = not line_cursor

def move_left_cur_index():
    global cur_index
    if cur_index > 0:
            cur_index -= 1

def move_right_cur_index():
    global cur_index
    if cur_index < len(data[cur_line]) - 1:
            cur_index += 1

def move_up_cur_index():
    global cur_line, cur_index
    if cur_line > 0:
        cur_line -= 1
        cur_index = min(cur_index, len(data[cur_line]) - 1)

def move_down_cur_index():
    global cur_line, cur_index
    if cur_line < len(data) - 1:
        cur_line += 1
        cur_index = min(cur_index, len(data[cur_line]) - 1)

def move_head_cur_index():
    global cur_index
    cur_index = 0

def move_tail_cur_index():
    global cur_index
    cur_index = len(data[cur_line]) - 1

def insert_text(text):
    global data, cur_line, cur_index
    if not data:
        data.append(text)
    else:
        line = data[cur_line]
        data[cur_line] = line[:cur_index] + text + line[cur_index:]


def append_text(text):
    global data, cur_line, cur_index
    if len(data) == 0:
        data.append(text)
        cur_index = len(text) - 1
    else:
        ogn_text = data[cur_line]
        data[cur_line] = ogn_text[:cur_index+1] + text + ogn_text[cur_index+1:]
        cur_index += len(text)

def move_to_next_word():
    global data, cur_line, cur_index
    if not data:
        return

    line = data[cur_line]
    i = cur_index + 1
    while i < len(line) and line[i] != ' ':
        i += 1
    while i < len(line) and line[i] == ' ':
        i += 1
    if i < len(line):
        cur_index = i  

def move_to_prev_word():
    global data, cur_line, cur_index
    if not data or cur_index <= 0:
        return

    line = data[cur_line]
    i = cur_index
    while i > 0 and line[i] == ' ':
        i -= 1
    while i > 0 and line[i - 1] != ' ':
        i -= 1
    cur_index = i

def delete_char_at_cursor():
    global data, cur_line, cur_index
    if not data:
        return
    line = data[cur_line]
    if len(line) == 0:
        return 
    if cur_index < 0 or cur_index >= len(line):
        return  
    data[cur_line] = line[:cur_index] + line[cur_index + 1:]
    if len(data[cur_line]) == 0:
        cur_index = 0
    elif cur_index >= len(data[cur_line]):
        cur_index = len(data[cur_line]) - 1

def delete_word():
    global data, cur_line, cur_index
    if not data:
        return

    line = data[cur_line]
    length = len(line)

    if cur_index >= length:
        return  

    i = cur_index

    if line[i] != ' ':
        while i < length and line[i] != ' ':
            i += 1
    while i < length and line[i] == ' ':
        i += 1
    data[cur_line] = line[:cur_index] + line[i:]

    if not data[cur_line]:
        cur_index = 0
    elif cur_index >= len(data[cur_line]):
        cur_index = len(data[cur_line]) - 1

def copy_line():
    global clipboard, data, cur_line
    if not data: 
        return
    clipboard = data[cur_line]

def insert_empty_line_below():
    global data, cur_line, cur_index
    if not data:
        data.append("")
        cur_line = 0
        cur_index = 0
    else:
        data.insert(cur_line + 1, "")
        cur_line += 1
        cur_index = 0  

def insert_empty_line_above():
    global data, cur_line, cur_index
    if not data:
        data.append("")
        cur_line = 0
        cur_index = 0
    else:
        data.insert(cur_line, "")
        cur_index = 0  


def paste_below():
    global data, clipboard, cur_index, cur_line
    if clipboard is None:
        return
    if not data:
        data.append(clipboard)
        cur_line = 0
        cur_index = 0
    else:
        data.insert(cur_line + 1, clipboard)
        move_down_cur_index()

def paste_above():
    global data, clipboard, cur_index, cur_line
    if clipboard is None:
        return
    if not data:
        data.append(clipboard)
        cur_line = 0
        cur_index = 0
    else:
        data.insert(cur_line, clipboard)
        move_up_cur_index()

def delete_current_line():
    global data, cur_line, cur_index

    if not data:
        return

    data.pop(cur_line)

    if data:
        ogn_index = cur_index
        if cur_line >= len(data):
            cur_line = len(data) - 1
        line_index_max = len(data[cur_line])-1
        if line_index_max < ogn_index:
            cur_index = line_index_max
        
        
    else:
        cur_line = 0
        cur_index = 0

def repeat():
    global last_valid_inputs
    while True:
        # last_valid_inputs.pop()
        inputs = last_valid_inputs.pop()
        # print("cur cmd is ", inputs[0], " text is ", inputs[1])
        if not inputs:
            return
        if inputs[0] != 'u':
            break
        else:
            inputs = last_valid_inputs.pop()
        # print("cur cmd is ", inputs[0], " text is ", inputs[1])
        


    handle_inputs(inputs[0], inputs[1])

def undo():
    load_state()
    


def handle_inputs(cmd, text):
    if cmd == "?":
        print_help()
    if cmd == ".":
        switch_row_cursor()
    if cmd == ";":
        switch_line_cursor()
    if cmd == "h":
        move_left_cur_index()
    if cmd == "l":
        move_right_cur_index()
    if cmd == "j":
        move_up_cur_index()
    if cmd == "k":
        move_down_cur_index()
    if cmd == "^":
        move_head_cur_index()
    if cmd == "$":
        move_tail_cur_index()
    if cmd == "i":
        insert_text(text)
    if cmd == "a":
        append_text(text)
    if cmd == "w":
        move_to_next_word()
    if cmd == "b":
        move_to_prev_word()
    if cmd == "x":
        delete_char_at_cursor()
    if cmd == "dw":
        delete_word()
    if cmd == "yy":
        copy_line()
    if cmd == "o":
        insert_empty_line_below()
    if cmd == "O":
        insert_empty_line_above()
    if cmd == "p":
        paste_below()
    if cmd == "P":
        paste_above()
    if cmd == 'dd':
        delete_current_line()
    if cmd == 'u':
        undo()
        global cur_cmd
        cur_cmd = 'u'
    if cmd == 'r':
        repeat()
        cur_cmd = 'r'
    if cmd == 's':
        pass
    register_last_inputs(cur_cmd, cur_text)
    



        
def display():
    global row_cursor, line_cursor
    global cur_line, cur_index
    global data
    global cur_cmd
    
    if cur_cmd == "?":
        return

    for i, line in enumerate(data):
        prefix = "*" if i == cur_line else " "
        if line_cursor:
            line = prefix + line

        if i != cur_line:
            print(line)
        else:
            if row_cursor:
                if line_cursor:
                    pos = max(0, min(cur_index+1, len(line)-1))
                else:
                    pos = max(0, min(cur_index, len(line)-1))
                if line != "":
                    print(line[:pos] + "\033[42m" + line[pos] + "\033[0m" + line[pos+1:])

            else:
                print(line)
    


def check_inputs(inputs) -> bool:
    global cur_cmd, cur_text
    patterns = {
        "single": r"^[?.hl^$wbxursjkqpP;Oo]$",
        "dw": r"^dw$",
        "dd": r"^dd$",
        "yy": r"^yy$", 
        "i": r"^i.+", 
        "a": r"^a.+", 
    }
    if (re.match(patterns["single"], inputs) or re.match(patterns["dw"], inputs) or re.match(patterns["yy"], inputs) or re.match(patterns["dd"], inputs)):
        cur_cmd = inputs
        cur_text = None
        return True 
    
    if (re.match(patterns["i"], inputs) or re.match(patterns["a"], inputs)):
        cur_cmd = inputs[0]
        cur_text = inputs[1:]
        return True


    return False

def main():
    global inputs, cur_cmd, cur_text
    while True:
        inputs = input(">")     # Set command prompt

        valid = check_inputs(inputs)  
        if not valid:
            continue  

        if cur_cmd == "q":     
            break 
        else:
            store_state() 
            handle_inputs(cur_cmd, cur_text)
            display()


if __name__ == "__main__":
    main()