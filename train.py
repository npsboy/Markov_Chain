import string

def read_text_file(file_path):
    """Read and return the contents of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def process_text(text):
    # Remove all punctuation
    no_punct = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    return no_punct.lower()


def parse_training_data(data):
    samples = []
    lines = data.splitlines()
    for line in lines:
        if line.strip():  # Skip empty lines
            words = line.strip().split()
            samples.append(words)
    return samples


markov_chain_gram_2 = {} 
markov_chain_gram_1 = {}
markov_chain_gram_3 = {}

def train_model_gram_2(samples):
    for sample in samples:
        for word in sample:
            word_index = sample.index(word)
            if word_index + 1 < len(sample):
                first_two_words = str(word) + " " + str(sample[word_index + 1])
            else:
                continue
            if word_index + 2 < len(sample):
                following_word = sample[word_index + 2]
            else:
                continue
            if first_two_words not in markov_chain_gram_2:
                markov_chain_gram_2[first_two_words] = [following_word]
            else:
                markov_chain_gram_2[first_two_words].append(following_word)

def train_model_gram_1(samples):
    for sample in samples:
        for word in sample:
            word_index = sample.index(word)
            if word_index + 1 < len(sample):
                following_word = sample[word_index + 1]
            else:
                continue
            if word not in markov_chain_gram_1:
                markov_chain_gram_1[word] = [following_word]
            else:
                markov_chain_gram_1[word].append(following_word)

def train_model_gram_3(samples):
    for sample in samples:
        for word in sample:
            word_index = sample.index(word)
            if word_index + 2 < len(sample):
                first_three_words = str(word) + " " + str(sample[word_index + 1]) + " " + str(sample[word_index + 2])
            else:
                continue
            if word_index + 3 < len(sample):
                following_word = sample[word_index + 3]
            else:
                continue
            if first_three_words not in markov_chain_gram_3:
                markov_chain_gram_3[first_three_words] = [following_word]
            else:
                markov_chain_gram_3[first_three_words].append(following_word)

def extract_keys_and_values(markov_chain):
    keys = list(markov_chain.keys())
    values = list(markov_chain.values())
    return keys, values


def save_to_text_file(data, file_path):
    """Save data to a text file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(data))
    except Exception as e:
        print(f"Error saving file: {e}")


def add_to_text_file(data, file_path):
    """Append data to a text file."""
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\n' + str(data))
    except Exception as e:
        print(f"Error appending to file: {e}")


def format_list_to_string(data_list):
    """Convert list to string, remove all commas."""
    lines = []
    for item in data_list:
        if isinstance(item, list):
            # Join sub-items with spaces, no commas
            line = ' '.join(str(x) for x in item)
            lines.append(line)
        else:
            lines.append(str(item))
    return '\n'.join(lines)


def main():
    training_data = read_text_file('training-data.txt')
    if training_data is None:
        print("Failed to load training data.")
        return

    training_data = process_text(training_data)
    print("Training data successfully loaded.")

    save_to_text_file(training_data, 'training-data.txt')  # Save cleaned data back to original file

    training_samples = parse_training_data(training_data)
    print(f"Parsed {len(training_samples)} training samples.")

    train_model_gram_2(training_samples)
    print("Gram 2 model training completed.")

    save_to_text_file(markov_chain_gram_2, './2gram/markov_chain_model_gram_2.txt')
    keys, values = extract_keys_and_values(markov_chain_gram_2)
    save_to_text_file(format_list_to_string(keys), './2gram/keys_gram_2.txt')
    save_to_text_file(format_list_to_string(values), './2gram/values_gram_2.txt')

    train_model_gram_1(training_samples)
    print("Gram 1 model training completed.")

    save_to_text_file(markov_chain_gram_1, './1gram/markov_chain_model_gram_1.txt')
    keys, values = extract_keys_and_values(markov_chain_gram_1)
    save_to_text_file(format_list_to_string(keys), './1gram/keys_gram_1.txt')
    save_to_text_file(format_list_to_string(values), './1gram/values_gram_1.txt')

    train_model_gram_3(training_samples)
    print("Gram 3 model training completed.")

    save_to_text_file(markov_chain_gram_3, './3gram/markov_chain_model_gram_3.txt')
    keys, values = extract_keys_and_values(markov_chain_gram_3)
    save_to_text_file(format_list_to_string(keys), './3gram/keys_gram_3.txt')
    save_to_text_file(format_list_to_string(values), './3gram/values_gram_3.txt')


if __name__ == '__main__':
    main()