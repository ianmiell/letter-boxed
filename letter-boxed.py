from itertools import permutations, chain, combinations

def read_words_from_file(file_path):
	try:
		with open(file_path, 'r') as file:
			# Read each line, strip any surrounding whitespace, and store in a list
			words = [line.strip() for line in file if line.strip().isupper()]
		return words
	except FileNotFoundError:
		print(f"Error: File not found at {file_path}")
		return []
	except Exception as e:
		print(f"An error occurred: {e}")
		return []

def generate_combinations(sets, valid_words):
	def matches_start_of_any(word):
		for valid_word in valid_words:
			if valid_word.startswith(word):
				return True
			if valid_word > word:  # Stop early due to sorted order
				break
		return False
	def helper(word, prev_set):
		# If the word does not match the start of any word, discard this word
		if not matches_start_of_any(word):
			return
		if word in valid_words and len(word) > 2:
			results.append(word)
		# Recurse by adding a character from a different set
		for i, current_set in enumerate(sets):
			if i != prev_set:  # Ensure current set is not the previous one
				for char in current_set:
					helper(word + char, i)
	results = []
	for i, initial_set in enumerate(sets):
		for char in initial_set:
			helper(char, i)
	return results

def find_valid_combinations_of_words_limited(returned_words, original_characters, max_words=3):
	# Generate all subsets of words with a length of up to max_length
	def all_combinations(words, max_length):
		return chain.from_iterable(combinations(words, r) for r in range(1, max_length + 1))
	def check_solution(solution_list):
		l=len(solution_list)
		i=0
		while i+1 < l:
			if solution_list[i][-1] != solution_list[i+1][0]:
				return False
			i=i+1
		return True
	valid_combinations = []
	for subset in all_combinations(returned_words, max_words):  # Limit combinations to max_words
		for perm in permutations(subset):  # Check all permutations of the subset
			combined = set(''.join(perm))  # Create a set of ordered characters
			if ''.join(sorted(combined)) == original_characters:  # Check character match
				if check_solution(perm):
					valid_combinations.append(perm)
	return valid_combinations

if __name__ == "__main__":
	# Specify the file path
	file_path = 'scrabble-dictionary.txt'
	# Read the words from the file
	words_array = read_words_from_file(file_path)
	input_characters = ''
	while len(input_characters) != 12:
		input_characters = input("Enter exactly 12 characters: ").strip().upper()
	sets = [set(input_characters[i:i+3]) for i in range(0, 12, 3)]
	original_characters = set.union(*sets)
	possible_words = generate_combinations(sets, words_array)
	# Flatten original characters into a single sorted string for comparison
	flattened_characters = ''.join(sorted(original_characters))
	valid_combinations = find_valid_combinations_of_words_limited(possible_words, flattened_characters)
	for combination in valid_combinations:
		print(combination)
