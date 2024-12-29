from itertools import permutations, chain, product, combinations

def read_words_from_file(file_path):
    """
    Reads upper-cased words from a file into an array.

    :param file_path: Path to the input file
    :return: List of upper-cased words
    """
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
    if len(sets) != 4 or not all(len(s) == 3 for s in sets):
        raise ValueError("Input must be a list of 4 sets, each containing exactly 3 letters.")

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
            #print('discarding: ' + word)
            return
        if word in valid_words and len(word) > 2:
            print('adding: ' + word)
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
    """
    Find combinations of words that use all the characters in the original set of letters exactly once,
    limiting the number of words in each combination to max_words or fewer.

    :param returned_words: A list of words generated from the sets.
    :param original_characters: A set of characters that must be used exactly once across all words.
    :param max_words: The maximum number of words in a combination.
    :return: A list of valid combinations of words.
    """
    # Flatten original characters into a single string for comparison
    original_characters = ''.join(sorted(original_characters))

    def all_combinations(words, max_length):
        """
        Generate all subsets of words with a length of up to max_length.
        """
        return chain.from_iterable(combinations(words, r) for r in range(1, max_length + 1))

    valid_combinations = []
    for subset in all_combinations(returned_words, max_words):  # Limit combinations to max_words
        subset_list = list(subset)
        #print(subset_list)
        l=len(subset_list)
        #print(l)
        i=0
        j=1
        rejecting=False
        #print(subset_list)
        ##while j < l:
        ##    if subset_list[i][-1] != subset_list[j][0]:
        ##        #print('rejecting: ' + str(subset_list))
        ##        rejecting=True
        ##        break
        ##    i=i+1
        ##    j=j+1
        ##if rejecting:
        ##    continue
        for perm in permutations(subset):  # Check all permutations of the subset
            combined = ''.join(perm)
            if ''.join(sorted(combined)) == original_characters:  # Check character match
                valid_combinations.append(perm)
                print(perm)

    return valid_combinations


if __name__ == "__main__":
    # Specify the file path
    # TODO: choose dictionary
    file_path = 'scrabble-dictionary.txt'
    #file_path = 'common-seven-letter-words.txt'

    # Read the words from the file
    words_array = read_words_from_file(file_path)
    # TODO: input chars on cl
    sets = [
        {"M", "E", "A"},
        {"H", "D", "O"},
        {"L", "Y", "C"},
        {"T", "I", "V"}
    ]
    original_characters = set.union(*sets)
    possible_words = generate_combinations(sets, words_array)
    #possible_words = ['CHIAO', 'CHIEL', 'CHIELD', 'CHID', 'CHIDE', 'CHIDED', 'CHILE', 'CHILD', 'CHILDE', 'CHILI', 'CHILIAD', 'CHILIADAL', 'CHILIADIC', 'CHIC', 'CHICA', 'CHICALOTE', 'CHICHI', 'CHICO', 'COMTE', 'COMIC', 'COMICAL', 'COAL', 'COALA', 'COALED', 'COACH', 'COACHED', 'COACT', 'COACTED', 'COAT', 'COATED', 'COACH', 'COACHED', 'COED', 'COELOM', 'COELOMIC', 'COELIAC', 'COELIAC', 'COY', 'COYED', 'COYOTE', 'COL', 'COLA', 'COLE', 'COLED', 'COLECTOMY', 'COLOCATE', 'COLOCATED', 'COLOTOMY', 'COLOCATE', 'COLOCATED', 'COLD', 'COLT', 'COLIC', 'COCA', 'COCO', 'COCOA', 'COCCAL', 'COCCOID', 'COCCOIDAL', 'COT', 'COTE', 'COTED', 'COCA', 'COCO', 'COCOA', 'COCCAL', 'COCCOID', 'COCCOIDAL', 'COCCI', 'COCCID', 'COCCIDIA', 'COCCIC', 'COIL', 'COILED', 'CIAO', 'CILIA', 'CILIATE', 'CILIATED', 'CILIOLATE', 'CILICE', 'CICADA', 'CICALA', 'CICALE', 'CICHLID', 'TAO', 'TAD', 'TALA', 'TALE', 'TALC', 'TALCED', 'TALI', 'TACE', 'TACET', 'TACH', 'TACHE', 'TACO', 'TACT', 'TAT', 'TATE', 'TACE', 'TACET', 'TACH', 'TACHE', 'TACO', 'TAIL', 'TAILED', 'TAILCOAT', 'TAILCOATED', 'TED', 'TEL', 'TELA', 'TELE', 'TELECOM', 'TELECOM', 'TELOMIC', 'TELOI', 'TELCO', 'TELIA', 'TELIAL', 'TELIC', 'TECH', 'TECHED', 'TECHY', 'TECHIE', 'TECTA', 'TECTAL', 'TET', 'TETH', 'TETCHED', 'TETCHY', 'TECH', 'TECHED', 'TECHY', 'TECHIE', 'THAT', 'THATCH', 'THATCHED', 'THATCHY', 'THE', 'THEY', 'THECA', 'THECAL', 'THECATE', 'THETA', 'THECA', 'THECAL', 'THECATE', 'THY', 'THYMOL', 'THYMOCYTE', 'THYMY', 'THYMI', 'THYMIC', 'THIO', 'THIOL', 'THIOLIC', 'TOM', 'TOMCAT', 'TOMCAT', 'TOAD', 'TOADY', 'TOADIED', 'TOE', 'TOED', 'TOY', 'TOYED', 'TOYO', 'TOLA', 'TOLE', 'TOLED', 'TOLD', 'TOCCATA', 'TOCCATE', 'TOT', 'TOTAL', 'TOTALED', 'TOTE', 'TOTED', 'TOCCATA', 'TOCCATE', 'TOIL', 'TOILE', 'TOILED', 'TOILET', 'TOILETED', 'TYE', 'TYTHE', 'TYTHED', 'CAD', 'CADMIC', 'CADE', 'CADET', 'CADI', 'CAY', 'CALM', 'CALATHI', 'CALECHE', 'CALECHE', 'CALO', 'CALICHE', 'CALICO', 'CACA', 'CACAO', 'CACHALOT', 'CACHE', 'CACHED', 'CACHET', 'CACHETED', 'CACTOID', 'CAT', 'CATALO', 'CATE', 'CATHECT', 'CATHECTED', 'CATCH', 'CATCHY', 'CACA', 'CACAO', 'CACHALOT', 'CACHE', 'CACHED', 'CACHET', 'CACHETED', 'CAID', 'CEDE', 'CEDED', 'CEDI', 'CEL', 'CELOM', 'CELT', 'CELIAC', 'CELIAC', 'CECA', 'CECAL', 'CETE', 'CECA', 'CECAL', 'CEIL', 'CEILED', 'CEILI', 'CHAO', 'CHAD', 'CHAY', 'CHAYOTE', 'CHALAH', 'CHALEH', 'CHALET', 'CHALOT', 'CHALOTH', 'CHALICE', 'CHALICED', 'CHAT', 'CHAI', 'CHELA', 'CHELATE', 'CHELATED', 'CHELOID', 'CHETAH', 'CHETH', 'CHYMIC', 'CHI', 'CHIMLA', 'CHIMLEY', 'CHIA', 'CHIAO', 'CHIEL', 'CHIELD', 'CHID', 'CHIDE', 'CHIDED', 'CHILE', 'CHILD', 'CHILDE', 'CHILI', 'CHILIAD', 'CHILIADAL', 'CHILIADIC', 'CHIC', 'CHICA', 'CHICALOTE', 'CHICHI', 'CHICO', 'COMTE', 'COMIC', 'COMICAL', 'COAL', 'COALA', 'COALED', 'COACH', 'COACHED', 'COACT', 'COACTED', 'COAT', 'COATED', 'COACH', 'COACHED', 'COED', 'COELOM', 'COELOMIC', 'COELIAC', 'COELIAC', 'COY', 'COYED', 'COYOTE', 'COL', 'COLA', 'COLE', 'COLED', 'COLECTOMY', 'COLOCATE', 'COLOCATED', 'COLOTOMY', 'COLOCATE', 'COLOCATED', 'COLD', 'COLT', 'COLIC', 'COCA', 'COCO', 'COCOA', 'COCCAL', 'COCCOID', 'COCCOIDAL', 'COT', 'COTE', 'COTED', 'COCA', 'COCO', 'COCOA', 'COCCAL', 'COCCOID', 'COCCOIDAL', 'COCCI', 'COCCID', 'COCCIDIA', 'COCCIC', 'COIL', 'COILED', 'CYMOL', 'CYMOID', 'CYCAD', 'CYCADEOID', 'CYCLE', 'CYCLED', 'CYCLO', 'CYCLOTHYMIA', 'CYCLOTHYMIC', 'CYCLOTOMIC', 'CYCLOID', 'CYCLOIDAL', 'CYCLIC', 'CYCLICAL', 'CLAD', 'CLADE', 'CLAY', 'CLAYED', 'CLAYEY', 'CLACH', 'CLACH', 'CLAIM', 'CLOACA', 'CLOACAL', 'CLOACA', 'CLOACAL', 'CLOY', 'CLOYED', 'CLOCHE', 'CLOT', 'CLOTH', 'CLOTHE', 'CLOTHED', 'CLOCHE', 'CLICHE', 'CLICHED', 'IMID', 'IMIDE', 'IMIDIC', 'IOTA', 'IDLE', 'IDLED', 'IDIOM', 'IDIOLECT', 'IDIOLECTAL', 'IDIOT', 'IDIOCY', 'ILIA', 'ILIAD', 'ILIAL', 'ILIAC', 'ILIAC', 'ICE', 'ICED', 'ICH', 'ICHTHYOID', 'ICHTHYIC']
    print(possible_words)
    valid_combinations = find_valid_combinations_of_words_limited(possible_words, original_characters)
    print(valid_combinations)


