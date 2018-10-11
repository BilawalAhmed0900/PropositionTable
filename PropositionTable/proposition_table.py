import sys
import os
import tkinter
import tkinter.ttk
import re


VERSION         = '0.0.4rc2'
MAINPROG_TITLE  = 'Proposition Table v{}'.format(VERSION)
MAINPROG_WIDTH  = 840
MAINPROG_HEIGHT = 480


NOT_SYMBOL   = '¬'
AND_SYMBOL   = 'Λ'
OR_SYMBOL    = 'V'
IMPLY_SYMBOL = '→'
BICON_SYMBOL = '↔'
XOR_SYMBOL   = '⊕'


SYMBOLS = [NOT_SYMBOL, AND_SYMBOL, OR_SYMBOL, IMPLY_SYMBOL, BICON_SYMBOL, XOR_SYMBOL]


class S_Q:
	def __init__(self):
		self.my_list = []
		self.len = 0

	def push(self, element):
		self.my_list.append(element)
		self.len += 1

	def __len__(self):
		return self.len


class Stack(S_Q):
	def pop(self):
		result = self.my_list[-1]
		del self.my_list[-1]
		self.len -= 1
		return result


class Queue(S_Q):
	def pop(self):
		result = self.my_list[0]
		self.my_list.pop(0)
		self.len -= 1
		return result


class BracketsNotFull(Exception):
	def __init__(self, arg):
		super(BracketsNotFull, self).__init__()
		self.arg = arg
		

class ToBool:
	def __init__(self, string):
		self.string = string.rstrip()


	def get_brackets_position(self, string):
		"""
			Get starting and ending positions of brackets, complete brackets
			Starting is stored in stack collection while ending in queue
		"""
		bracket_level = 0
		last_bracket_starts = Stack()
		last_bracket_ends = Queue()
		first_found = False
		index = 0

		for character in string:
			if character == '(':
				bracket_level += 1
				last_bracket_starts.push(index + 1)

				first_found = True
			elif character == ')':
				bracket_level -= 1
				last_bracket_ends.push(index)

			index += 1
			if bracket_level == 0 and first_found:
				break

		if len(last_bracket_starts) == len(last_bracket_ends):
			return last_bracket_starts, last_bracket_ends
		else:
			raise BracketsNotFull("All brakets that are opened hadn't closed")


	def extract_bracket(self, string):
		"""
			Extract string enclosed in a bracket
		"""
		simple_return_list = []
		last_bracket_starts, last_bracket_ends = self.get_brackets_position(string)

		for _ in range(len(last_bracket_starts)):
			start_position = last_bracket_starts.pop()
			end_position = last_bracket_ends.pop()

			simple_return_list.append(string[start_position : end_position])

		simple_return_list.append(string)
		return simple_return_list


	def extract_formatted_bracket(self, string):
		"""
			Extract string enclosed in a bracket, replacing previous with placeholder
		"""
		intermediate_list = []
		loop_string = string
		last_bracket_starts, last_bracket_ends = self.get_brackets_position(string)
		simple_brackets = self.extract_bracket(string)

		if len(last_bracket_starts) == len(last_bracket_ends):
			for index in range(len(last_bracket_starts)):
				start_index = last_bracket_starts.pop() - 1
				stop_index = last_bracket_ends.pop()

				loop_string = simple_brackets[index + 1].replace(simple_brackets[index], '\\{}'.format(index))
				intermediate_list.append(loop_string)

		if len(intermediate_list) > 0:
			r_l = intermediate_list
		else:
			r_l = simple_brackets

		return_list = []
		for index, proposition in enumerate(r_l):
			len_loop_string = len(proposition)	
			proposition = proposition
			for i in [IMPLY_SYMBOL, BICON_SYMBOL, XOR_SYMBOL]:
				if i == IMPLY_SYMBOL:
					repl = r'(not (\1) or (\2))'
					upper_precedence_symbols = AND_SYMBOL + OR_SYMBOL + NOT_SYMBOL + IMPLY_SYMBOL
				elif i == BICON_SYMBOL:
					repl = r'(\1) == (\2)'
					upper_precedence_symbols = AND_SYMBOL + OR_SYMBOL + NOT_SYMBOL + IMPLY_SYMBOL + BICON_SYMBOL
				elif i == XOR_SYMBOL:
					repl = r'(\1) != (\2)'
					upper_precedence_symbols = AND_SYMBOL + OR_SYMBOL + NOT_SYMBOL +  IMPLY_SYMBOL + BICON_SYMBOL + XOR_SYMBOL
				while True:
					new_proposition = re.sub(r'([a-zA-Z0-9\ \\\(\){}]+)\s*{}\s*([a-zA-Z0-9\ \\\(\){}]+)'.format(upper_precedence_symbols, i, upper_precedence_symbols), 
						repl, proposition, 1)
					if new_proposition == proposition:
						break
					proposition = new_proposition

			proposition = proposition
			return_list.append(proposition)

		return simple_brackets, return_list
			


	def format_for_eval(self, list_proposition):
		"""
			Replace symbols with words
			Implication, biconditional and xor will be converted according to conditions below
		"""
		return_list = []
		for proposition in list_proposition:
			proposition = proposition.replace(NOT_SYMBOL, ' not ')
			proposition = proposition.replace(AND_SYMBOL, ' and ')
			proposition = proposition.replace(OR_SYMBOL,  ' or ' )

			return_list.append(proposition)

		return return_list


	def get_string_from_formatted(self, formatted_list, simple_list):
		"""
			Replace \\number with actual strings from before
		"""
		for i in range(len(formatted_list)):
			if i == 0:
				formatted_list[i] = formatted_list[i].replace('\\{}'.format(i), self.format_for_eval([simple_list[i]])[i])
				continue

			formatted_list[i] = formatted_list[i].replace('\\{}'.format(i), formatted_list[i - 1])

		return formatted_list[len(formatted_list) - 1]


	def get_boolean(self):
		self.simple_brackets, self.formatted_brackets = self.extract_formatted_bracket(self.string)
		self.formatted_for_eval = self.format_for_eval(self.formatted_brackets)
		self.eval_string = self.get_string_from_formatted(self.formatted_for_eval, self.simple_brackets)
		return eval(self.eval_string)


	def get_eval_string(self):
		self.simple_brackets, self.formatted_brackets = self.extract_formatted_bracket(self.string)
		self.formatted_for_eval = self.format_for_eval(self.formatted_brackets)
		self.eval_string = self.get_string_from_formatted(self.formatted_for_eval, self.simple_brackets)
		return self.eval_string


def add_text(edit: tkinter.Text, value: str) -> None:
	edit.insert(tkinter.INSERT, value)


def remove_duplicates(values: list) -> list:
	output = []
	seen = set()
	for value in values:
		# If value has not been encountered yet,
		# ... add it to both list and set.
		if value not in seen and not value == '':
			output.append(value)
			seen.add(value)
	return output


def get_proposition_list(propositon_string: str) -> list:
	# This line does this
	# Replace any symbol in SYMBOLS with whitespace, removing \n at end
	# and split using whitespaces to form list
	list_of_entites = re.sub(r'{}|\(|\)'.format('|'.join(SYMBOLS)), ' ', propositon_string).rstrip().split(' ')
	list_of_entites = remove_duplicates(list_of_entites)

	return list_of_entites


def build_table(table_frame: tkinter.Frame, propositon_list: list, propositon_string: str) -> None:
	WIDTH_OF_PROPOSITION = 35
	for child in table_frame.winfo_children():
		child.destroy()

	column_name_list = propositon_list + [propositon_string]

	style = tkinter.ttk.Style()
	style.configure('Treeview', rowheight=25)

	table = tkinter.ttk.Treeview(table_frame, column=column_name_list)
	table.column("#0", minwidth=0, width=0)

	scrollbar = tkinter.ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
	table.configure(yscrollcommand=scrollbar.set)

	for column_name in propositon_list:
		table.column(column_name, minwidth=WIDTH_OF_PROPOSITION, width=WIDTH_OF_PROPOSITION, anchor='center')
		table.heading(column_name, text=column_name)

	width = MAINPROG_WIDTH - (WIDTH_OF_PROPOSITION*len(propositon_list)) - 20
	table.column(propositon_string, minwidth=width, width=width, anchor='center')
	table.heading(propositon_string, text=propositon_string)

	formatted_proposition_string = ToBool(propositon_string).get_eval_string()
	simple_proposition_list = []

	original_number_of_simple_propositon = int(2 ** len(propositon_list))	
	number_of_simple_propositon = original_number_of_simple_propositon
	while number_of_simple_propositon > 1:
		possible_values = []
		for _ in range(number_of_simple_propositon//2):
			possible_values.append(True)

		for _ in range(number_of_simple_propositon//2):
			possible_values.append(False)

		simple_proposition_list.append(possible_values * (original_number_of_simple_propositon // number_of_simple_propositon))
		number_of_simple_propositon //= 2
	
	for index in range(len(simple_proposition_list[0])):
		this_vals = []
		this_proposition_string = formatted_proposition_string
		for i in range(len(simple_proposition_list)):
			this_vals.append(simple_proposition_list[i][index])

		for index, proposition_name in enumerate(propositon_list):
			this_proposition_string = re.sub(r'\b{}\b'.format(proposition_name), str(this_vals[index]), this_proposition_string)

		this_vals.append(eval(this_proposition_string))
		table.insert('', 'end', text='', value=this_vals)

	scrollbar.pack(side="right", fill="y")
	table.pack(side="left", expand=True, fill='both')
	


def add_widgets(main_frame: tkinter.Frame, usable_height: int) -> None:
	proposition_text = tkinter.Label(main_frame, text='Proposition: ')
	proposition_text.place(x=10, y=14)
	proposition_edit = tkinter.Text(main_frame, height=1, font=('Helvetica', 18))
	proposition_edit.focus()
	proposition_edit.place(x=85, y=8, width=MAINPROG_WIDTH - 85 - 10)

	# Size of buttons in pixels
	build_button_width = 100
	other_button_width = 25

	# Xor button is 25 pixels left from build button while other are only 5 pixels
	build_button_x = MAINPROG_WIDTH - 10 - build_button_width
	xor_button_x   = build_button_x - 25 - other_button_width
	bicon_button_x = xor_button_x   - 5  - other_button_width
	imply_button_x = bicon_button_x - 5  - other_button_width
	or_button_x    = imply_button_x - 5  - other_button_width
	and_button_x   = or_button_x    - 5  - other_button_width
	not_button_x   = and_button_x   - 5  - other_button_width

	not_button = tkinter.Button(main_frame, text=NOT_SYMBOL, height=1,
		command=lambda: add_text(proposition_edit, NOT_SYMBOL))
	not_button.place(x=not_button_x, y=45, width=other_button_width)
	
	and_button = tkinter.Button(main_frame, text=AND_SYMBOL, height=1,
		command=lambda: add_text(proposition_edit, AND_SYMBOL))
	and_button.place(x=and_button_x, y=45, width=other_button_width)

	or_button = tkinter.Button(main_frame, text=OR_SYMBOL, height=1,
		command=lambda: add_text(proposition_edit, OR_SYMBOL))
	or_button.place(x=or_button_x, y=45, width=other_button_width)

	imply_button = tkinter.Button(main_frame, text=IMPLY_SYMBOL, height=1,
		command=lambda: add_text(proposition_edit, IMPLY_SYMBOL))
	imply_button.place(x=imply_button_x, y=45, width=other_button_width)

	bicon_button = tkinter.Button(main_frame, text=BICON_SYMBOL, height=1,
		command=lambda: add_text(proposition_edit, BICON_SYMBOL))
	bicon_button.place(x=bicon_button_x, y=45, width=other_button_width)

	xor_button = tkinter.Button(main_frame, text=XOR_SYMBOL, height=1,
		command=lambda: add_text(proposition_edit, XOR_SYMBOL))
	xor_button.place(x=xor_button_x, y=45, width=other_button_width)

	# A frame for Treeview so, we can rebuild it for different propotion by deleting all
	# widgets of this frame
	table_frame = tkinter.Frame(main_frame)

	# Seperation is 10. so actual width is MAINPROG_WIDTH minus margins from both ends(10 and 10)
	# Same for height(85 and 10)
	table_frame.place(x=10, y=85, width=MAINPROG_WIDTH - 20, height=usable_height - 95)
	
	build_table_button = tkinter.Button(main_frame, text='Build Table...', height=1,
		command=lambda: build_table(table_frame, get_proposition_list(proposition_edit.get('1.0', tkinter.END)), 
			proposition_edit.get('1.0', tkinter.END) ) )
	build_table_button.place(x=build_button_x, y=45, width=build_button_width)


def main() -> None:
	root = tkinter.Tk()
	root.title(MAINPROG_TITLE)
	root.resizable(0,0)
	root.update()

	main_frame = tkinter.Frame(root, width=MAINPROG_WIDTH, height=MAINPROG_HEIGHT)
	main_frame.pack()

	add_widgets(main_frame, MAINPROG_HEIGHT)

	root.mainloop()


if __name__ == '__main__':
	main()