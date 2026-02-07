import string
import re

def clean_subtitles(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip subtitle numbers (digits only)
        if re.match(r'^\d+$', line):
            continue
        # Skip timestamps (contain -->)
        if '-->' in line:
            continue
        # Skip HTML tags like <i> or </i>
        line = re.sub(r'<[^>]+>', '', line)
        # Collect dialogue text
        current_text.append(line)
    
    # Since subtitles are block-separated by empty lines or numbers, but in this file, each block is separated by number and timestamp.
    # Actually, the text is after timestamp until next number.
    # To simplify, since the file has numbers, timestamps, then text, we can process sequentially.
    # But in the loop above, we skipped numbers and timestamps, so current_text accumulates all text lines.
    # But we need to group per subtitle.
    # Better way: iterate and when we hit a number, start new block, but since we skip numbers, perhaps reset on empty or something.
    # The file has no empty lines between blocks, but after text, next number.
    # So, perhaps collect until we hit a number, but since we skip numbers, it's tricky.
    # Actually, since we skip numbers and timestamps, the remaining are text lines, and each subtitle's text is consecutive.
    # But in the file, each subtitle has its text on one or more lines, then next number.
    # To group, we can use a flag.
    
    # Revised approach:
    cleaned_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'^\d+$', line):  # Subtitle number
            i += 1
            if i < len(lines) and '-->' in lines[i]:  # Timestamp
                i += 1
                # Now collect text until next number or end
                text_parts = []
                while i < len(lines) and not re.match(r'^\d+$', lines[i].strip()) and lines[i].strip():
                    text = lines[i].strip()
                    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
                    if text:
                        text_parts.append(text)
                    i += 1
                if text_parts:
                    full_text = ' '.join(text_parts)
                    # Clean: lowercase, remove punctuation
                    full_text = full_text.lower()
                    full_text = full_text.translate(str.maketrans('', '', string.punctuation))
                    cleaned_lines.append(full_text)
            else:
                i += 1
        else:
            i += 1
    
    # Write to output file, one per line
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line.strip() + '\n')

if __name__ == '__main__':
    clean_subtitles('training-data.txt', 'training-data.txt')
    print("Subtitles cleaned and saved to 'training-data.txt'.")
