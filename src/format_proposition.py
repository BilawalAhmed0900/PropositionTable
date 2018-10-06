import re


NOT_SYMBOL   = '¬'
AND_SYMBOL   = 'Λ'
OR_SYMBOL    = 'V'
IMPLY_SYMBOL = '→'
BICON_SYMBOL = '↔'
XOR_SYMBOL   = '⊕'


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
		return_list = []
		loop_string = string
		last_bracket_starts, last_bracket_ends = self.get_brackets_position(string)
		simple_brackets = self.extract_bracket(string)

		if len(last_bracket_starts) == len(last_bracket_ends):
			for index in range(len(last_bracket_starts)):
				start_index = last_bracket_starts.pop() - 1
				stop_index = last_bracket_ends.pop()

				loop_string = simple_brackets[index + 1].replace(simple_brackets[index], '\\{}'.format(index))
				return_list.append(loop_string)

		if len(return_list) > 0:
			return simple_brackets, return_list
		else:
			return simple_brackets, simple_brackets


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
			
			for i in [IMPLY_SYMBOL, BICON_SYMBOL, XOR_SYMBOL]:
				if i == IMPLY_SYMBOL:
					repl = r'(not (\1) or (\2))'
				elif i == BICON_SYMBOL:
					repl = r'(\1) == (\2)'
				elif i == XOR_SYMBOL:
					repl = r'(\1) != (\2)'
				while True:
					new_proposition = re.sub(r'([a-zA-Z0-9\ \\\(\)]+)\s*{}\s*([a-zA-Z0-9\ \\\(\)]+)'.format(i), repl, proposition, 1)
					if new_proposition == proposition:
						break
					proposition = new_proposition

			return_list.append(proposition)

		return return_list


	def get_string_from_formatted(self, formatted_list, simple_list):
		"""
			Replace \\number with actual strings from before
		"""
		for i in range(len(formatted_list)):
			if i == 0:
				#print(formatted_list[i])
				#print(self.format_for_eval([simple_list[i]]))
				formatted_list[i] = formatted_list[i].replace('\\{}'.format(i), self.format_for_eval([simple_list[i]])[i])
				#print(formatted_list[i])
				continue

			#print(formatted_list[i])
			formatted_list[i] = formatted_list[i].replace('\\{}'.format(i), formatted_list[i - 1])
			#print(formatted_list[i])

		return formatted_list[len(formatted_list) - 1]


	def get_boolean(self):
		self.simple_brackets, self.formatted_brackets = self.extract_formatted_bracket(self.string)
		self.formatted_for_eval = self.format_for_eval(self.formatted_brackets)
		self.eval_string = self.get_string_from_formatted(self.formatted_for_eval, self.simple_brackets)
		return eval(self.eval_string)


	def get_eval_string(self):
		self.simple_brackets, self.formatted_brackets = self.extract_formatted_bracket(self.string)
		#print(self.simple_brackets)
		#print(self.formatted_brackets)
		self.formatted_for_eval = self.format_for_eval(self.formatted_brackets)
		#print(self.formatted_for_eval)
		self.eval_string = self.get_string_from_formatted(self.formatted_for_eval, self.simple_brackets)
		#print(self.eval_string)
		return self.eval_string
