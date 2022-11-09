from tkinter import *
import re

#run w/out debugging fn + cntrl + f5
#restart fn + shift + command + f5

'''
Remember you cant do print("yo  "lel kekW" ")
Because of double quote("""") shouldnt work
Remember this when creating the string literal regex since at most you should only expect characters that are not --> "
'''


class parser:
    def __init__(self):
        self.tokens = None
        self.current_token = ('Empty', 'Empty')

    def set_current_tokens(self, temp_list):
        self.tokens = temp_list

    def accept_token(self):
        print("     accept token from the list:" + self.current_token[1])
        self.current_token = self.tokens.pop(0)
        tempA, tempB = self.current_token
        return tempA, tempB

    def math(self):
        pass

    def exp(self):
        self.current_token = self.tokens.pop(0)
        print("\n----parent node exp, finding children nodes:")
        token_type, token = self.current_token
        if (token_type == 'int' or 'float'):
            print("child node (internal): keyword")
            print(f'keyword has child node (token): {token}')
            token_type, token = self.accept_token()

        # int -> identifier -> = -> int | float
        if (token_type == 'identifier'):
            print("child node (internal): identifier")
            print(f'identifier has child node (token): {token}')
            token_type, token = self.accept_token()
            if (token == '='):
                print("child node (token):" + self.current_token[1])
                token_type, token = self.accept_token()
            else:
                print("expect = as the second element of the expression!")
                return
        print("Child node (internal): math")
        #self.math() <--- write function soon

        if (token == 'print'):
            print("child node (internal): keyword")
            print(f'identifier has child node (token): {token}')
            token_type, token = self.accept_token()

        # print -> ( ->  id | " -> identifier | string
        if (token == 'keyword'):
            print('-' * 4 + 'parent node exp, finding children nodes:')

    def print_tokens(self):
        tempA, tempB = self.tokens.pop(0)
        print(f'Printing tempA: {tempA} , printing tempB: {tempB}')
        #for token in self.tokens:
        #tempA, tempB = token
        #print(f'{tempA} and {tempB}')
        #print(token)


class lexer:
    def __init__(self):
        self.parse_str = None
        self.count = 0
        self.prev = None
        self.tokens = []
        self.r_tokens = []
        self.check_null = re.compile('()')
        self.token_types = {
        'keyword': re.compile('^(int|float|double|if|else|string|print)'),
        'operator': re.compile('^[<|>|=|*|+]'),
        'separator': re.compile('^[\(|\)|:|"|;]'),
        'identifier': re.compile('^([A-Za-z]+\d*)'),
        'int_literal': re.compile('^(\d+)'),
        'float_literal': re.compile('^(\d+\.\d+)'),
        'string_literal': re.compile('^(\w+)')
        }

        self.token_types2 = {
        'keyword': re.compile('^(int|float|double|if|else|string|print)'),
        'identifier': re.compile('^([A-Za-z]+\d*)'),
        'operator': re.compile('^[<|>|=|*|+]'), 
        'separator': re.compile('^[\(|\)|:|\"|;]'),
        'int_literal': re.compile('^(\d+)'),
        'float_literal': re.compile('^(\d+\.\d+)'),
        'string_literal': re.compile('^(.+)\b'),
        }
        '''
            1. Do a set string
            2. run the class match_token_methods 
            3. re-assign set string
            4. loop continously
            '''

    def match_tokens2(self):
        count = 0
        while(self.is_empty()):
            for key, pair in self.token_types2.items():
                if self.prev == '"' and self.parse_str.count('"') == 1:
                    if self.check_match2('string_literal', self.token_types['string_literal']):
                        break
                else:
                    if self.check_match2(key, pair):
                        break 
            #count +=1
            #if count == 20:
                #quit()

        for tokens in self.tokens:
            print(tokens)

    def check_match2(self, key, pair):
        self.parse_str = self.parse_str.strip()
        print(f'printing self.parse_str: {self.parse_str}')
        #result = pair.search(self.parse_str)
        result = pair.match(self.parse_str)
        #print(f'in check_match2 printing result: {result}')
        #print(f'in check_match2 printing pair: {pair}')
        #print(f'in check_math2 printing key: {key}') 
        if result:
            if result.group(0) == '"':
                self.prev = result.group(0)
            else:
                self.prev = key
            self.set_string(pair.sub('', self.parse_str))
            self.tokens.append(f'<{key}, {result.group(0)}>')
            self.r_tokens.append([key, result.group(0)])
            print(f'printing key: {key} and printing result: {result.group(0)}')
            return True
        return False


    def is_empty(self):
        #print(f'printing: {self.parse_str.isspace()}')
        result = re.sub('\s+','',self.parse_str)
        #if result:
            #print(f'result is true, result: {result}')
        return True if result else False
        quit()
        #return True if result
        return False if self.parse_str.isspace() else True
        #return True if result else False

    def match_tokens(self):
        while (self.isEmpty()):  # or self.count == 4, not self.isEmpty()
            for key, pair in self.token_types.items():
                if self.prev == '"' and self.parse_str.count('"') == 1:  #'"'
                    self.check_match('string_literal', self.token_types['string_literal'])
                continue
                self.check_match(key, pair)
            #self.print_tokens()

    #maybe store the old string without whitespace removed
    #check if print is in list and if it is -> extact string from "....." and input it instead of the string in check_match()
    def check_match(self, key, pair):
        result = pair.match(self.parse_str)
        if result:
            if result.group(0) == '"':
                self.prev = result.group(0)
            else:
                self.prev = key
            self.set_string(pair.sub('', self.parse_str))
            self.tokens.append(f'<{key}, {result.group(0)}>')  #<keyword, print>
            self.r_tokens.append([key, result.group(0)])
            #print(f'Printing result: {result.group(0)}')
            #print(f'Printing key: {key}')
            #print(f'Printing leftover string: {self.parse_str}')
            #print(f'Printing value of pair: {pair}')

    def print_tokens(self):
        for token in self.tokens:
            print(token)

    def set_string(self, str_temp):
        self.parse_str = str_temp

    def isEmpty(self):
        #if len(self.parse_str) == count:
        return True if len(self.parse_str) > 0 else False
        pas

    def get_tokens(self):
        return self.r_tokens


class gui:


    def __init__(self):
        self.master = Tk()
        self.lexer = lexer()
        self.parser = parser()
        self.output_count = 1.0
        self.counter = 1.0
        self.current_count = 0
        self.frame_1 = Frame(self.master)
        self.inner_frame_left = Frame(self.frame_1)
        self.inner_frame_right = Frame(self.frame_1)
        self.master.title('Lexical Analyzer for Tiny Pie')
        self.master.grid_columnconfigure(0, weight=1)  #this centers the frame
        #Label stuff for frame 1
        self.text_box_input_label = Label(self.frame_1,
                                        text='Source Code Input: ',
                                        height=2,
                                        anchor='s')
        self.text_box_output_label = Label(self.frame_1,
                                        text='Lexical Analyzed Result: ',
                                        height=2,
                                        anchor='s')

        #label stuff for inner frame
        self.current_line_label = Label(self.inner_frame_left,
                                        text='Current Processing Line: ',
                                        anchor='n')

        #entry stuff inner frame left
        self.current_entry = Entry(self.inner_frame_left, width=10, justify=CENTER)
        self.current_entry.insert(0, 0)
        #buttons stuff inner frame left
        self.next_line_button = Button(self.inner_frame_left,
                                    width=12,
                                    text=' Next Line ',
                                    bg='#97d1a6',
                                    command=self.next)

        #button stuff inner frame right
        self.quit_program_button = Button(self.inner_frame_right,
                                        width=12,
                                        text=' Quit  ',
                                        bg='#97d1a6',
                                        command=quit)
        #input stuff
        self.text_box_input = Text(self.frame_1, width=35, height=15, padx=20)
        self.text_box_output = Text(self.frame_1, width=35, height=15, padx=20)
        #grid stuff for frame
        self.text_box_input_label.grid(row=0, column=0)
        self.text_box_input.grid(
        row=1, column=0, padx=25)  #, padx=100, pady=100 dont forget pady=(0,5)
        self.text_box_output_label.grid(row=0, column=1)
        self.text_box_output.grid(row=1, column=1, padx=25)
        #grid stuff for inner frame
        self.current_line_label.grid(row=0, column=0)
        self.current_entry.grid(row=0, column=1, padx=(35, 0), sticky=E)
        self.next_line_button.grid(row=1, column=1, pady=(5, 10))
        self.quit_program_button.grid(row=1, column=3, sticky=S, pady=(15, 0))
        self.frame_1.grid(row=0)
        self.inner_frame_left.grid(row=2, column=0)
        self.inner_frame_right.grid(row=2, column=1)

    def next(self):
        tokens = []
        output = self.text_box_input.get(self.counter, self.counter + 1)
        test_str = output
        output = re.sub('\s+', '', output)
        if len(output) > 0:
            self.current_count += 1
        else:
            return
        #self.lexer.set_string(output) m

        #strip the output string at least once before setting it.
        self.lexer.set_string('print("Yo this is my attempt")') #test_str
        self.lexer.match_tokens2()
        #self.lexer.match_tokens()
        #self.parser.set_current_tokens(self.lexer.get_tokens())
        #self.parser.exp()
        #self.parser.print_tokens() #testing how the tokens look like



        tokens = self.lexer.tokens
        for token in tokens:
            self.text_box_output.insert(self.output_count, token + '\n')
            self.output_count += 1
        self.lexer.tokens.clear()
        self.lexer.parse_str = None

        self.counter += 1
        self.current_entry.delete(0)
        self.current_entry.insert(0, self.current_count)

    def run_gui(self):
        self.master.mainloop()


if __name__ == '__main__':
    my_gui = gui()
    my_gui.run_gui()
