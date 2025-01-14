import itertools
import time
import os
import zipfile
from tqdm import tqdm

# Predefined character sets
CHAR_SETS = {
    "Chat": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Num": "0123456789",
    "SYM": "!@#$%^&*()-_=+[]{}|;:',.<>?/`~",
    "All": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:',.<>?/`~"
}

def clear_screen():
    """Clears the terminal screen."""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"\033[31mError clearing screen: {e}\033[0m")

def display_intro():
    """Displays the starting screen and information about the tool."""
    try:
        clear_screen()
        print("\033[31m" + "█████████████████████████████████████████████████████████████████" + "\033[0m")
        print("\033[32m" + "   Enhanced Wordlist Generator" + "\033[0m")
        print("\033[34m" + "-----------------------------------------------------------------" + "\033[0m")
        print("\033[36m" + "     Generate your own wordlists with advanced options" + "\033[0m")
        print("\033[34m" + "-----------------------------------------------------------------" + "\033[0m")
        print("\033[33m" + "[*] Version 2.1 | By Sagar Budha" + "\033[0m")
        print("\033[36m" + "[*] Use responsibly and for authorized purposes only!" + "\033[0m")
        print("\n")
        time.sleep(2)
    except Exception as e:
        print(f"\033[31mError displaying intro: {e}\033[0m")

def generate_wordlist(charset, min_length, max_length, output_file, prefix="", compress=False, max_words=None):
    """
    Generates a wordlist based on the parameters provided by the user.

    Args:
        charset (str): The characters to include in the wordlist.
        min_length (int): The minimum length of words to generate.
        max_length (int): The maximum length of words to generate.
        output_file (str): The file where the generated wordlist will be saved.
        prefix (str): A prefix to add before each word (optional).
        compress (bool): Whether to compress the output file into a .zip (optional).
        max_words (int): The maximum number of words to generate (optional).
    """
    try:
        total_words = sum(len(charset) ** length for length in range(min_length, max_length + 1))
        if max_words and total_words > max_words:
            total_words = max_words
            print(f"\033[33m[WARNING] Total words truncated to {max_words:,}.\033[0m")

        estimated_size = total_words * (len(prefix) + (min_length + max_length) // 2 + 1)
        print(f"\033[36m[INFO] Total Words: {total_words:,}\033[0m")
        print(f"\033[36m[INFO] Estimated File Size: {estimated_size / (1024 ** 2):.2f} MB\033[0m")

        words_generated = 0
        try:
            with open(output_file, "w") as file:
                with tqdm(total=total_words, desc="Generating Wordlist") as pbar:
                    for length in range(min_length, max_length + 1):
                        for word in itertools.product(charset, repeat=length):
                            if max_words and words_generated >= max_words:
                                break
                            file.write(prefix + "".join(word) + "\n")
                            pbar.update(1)
                            words_generated += 1
        except OSError as e:
            print(f"\033[31mError opening or writing to file: {e}\033[0m")
            return

        print(f"\033[32mWordlist successfully saved to '{output_file}'.\033[0m")

        if compress:
            zip_file = output_file + ".zip"
            try:
                with zipfile.ZipFile(zip_file, "w") as zipf:
                    zipf.write(output_file)
                print(f"\033[32mWordlist compressed to '{zip_file}'.\033[0m")
            except zipfile.BadZipFile as e:
                print(f"\033[31mError compressing file: {e}\033[0m")
            except Exception as e:
                print(f"\033[31mUnexpected error while compressing: {e}\033[0m")
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m")

def get_input(prompt, valid_values=None, default=None, allow_empty=False):
    """
    Handles user input with validation.

    Args:
        prompt (str): The input prompt.
        valid_values (list, optional): Valid input values (case-sensitive).
        default (any, optional): Default value if input is empty.
        allow_empty (bool, optional): Whether to allow empty input.

    Returns:
        str: The user input or default value.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and allow_empty:
                return default
            if valid_values and user_input not in valid_values:
                print(f"Invalid input. Choose from {', '.join(valid_values)}.")
                continue
            return user_input or default
        except Exception as e:
            print(f"\033[31mError processing input: {e}\033[0m")

if __name__ == "__main__":
    # Display the starting screen
    try:
        display_intro()

        print("Available character sets:")
        for key, value in CHAR_SETS.items():
            print(f"  {key}: {value}")

        # Collect user input
        char_set_choice = get_input("Choose a character set (Chat, Num, SYM, All) or enter custom characters: ", allow_empty=True)
        charset = CHAR_SETS.get(char_set_choice, char_set_choice)

        exclude_chars = get_input("Enter characters to exclude (leave empty for none): ", allow_empty=True)
        exclude_chars = exclude_chars or ""  # Avoid None
        charset = "".join(char for char in charset if char not in exclude_chars)

        min_length = int(get_input("Enter the minimum word length: "))
        max_length = int(get_input("Enter the maximum word length: "))
        output_file = get_input("Enter the output file name (default: wordlist.txt): ", default="wordlist.txt", allow_empty=True)
        prefix = get_input("Enter a prefix for each word (leave empty for none): ", allow_empty=True, default="")
        max_words = int(get_input("Enter the maximum number of words to generate (leave empty for unlimited): ", allow_empty=True, default="0")) or None
        compress = get_input("Compress output to ZIP? (yes/no): ", valid_values=["yes", "no"], default="no") == "yes"

        # Generate the wordlist
        generate_wordlist(charset, min_length, max_length, output_file, prefix, compress, max_words)
    except Exception as e:
        print(f"\033[31mError in main process: {e}\033[0m")
                    
