import os
import regex
import argparse

def get_file_content(path_to_file):
    content = None
    with open(path_to_file, encoding='utf8') as text_file:
        content = text_file.read()
    return content

def write_file_content(new_file_name, content, typography):
    with open (new_file_name, "w", encoding="utf-8") as new_file:
        for line in content:
            new_file.write(line + typography)

def extract_hashtags(path_to_file):
    text_content = get_file_content(path_to_file)
    pattern = r"\#\w+"
    hashtags = regex.findall(pattern, text_content)
    write_file_content("extracted_hashtags.txt", hashtags, "\n")

def arrange_headlines(path_to_file):
    text_content = get_file_content(path_to_file)
    pattern = r"(\d{1,2})\. (\w+)  (\d{4}) \n\n(\d+\:\d{2}) \n\n(.*\n)"
    rearranged = regex.sub(pattern, r"\3\t\2\t\1\t\4\t\5", text_content)
    write_file_content("arranged_headlines.txt", rearranged.splitlines(), "\n")

def extract_from_vertical(path_to_file):
    text_content = get_file_content(path_to_file)
    pattern = r"(\n*(\w+)\t(\w+.*)\t(\w{1})(.*))|(\n.*)"
    extracted_info = regex.sub(pattern, r"\2_\4 ", text_content)
    cleanup_pattern = r" \_"
    clean_info = regex.sub(cleanup_pattern, "", extracted_info)
    write_file_content("info_from_vertical.txt", str(clean_info), "")

def extract_from_joanna(path_to_file):
    text_content = get_file_content(path_to_file)
    pattern = r"^(?!\p{L}{2},).*$"
    only_two_syllable = regex.sub(pattern, "", text_content, flags=regex.MULTILINE)
    pattern2 = r"(^[\\s]*$\n)|(^\p{L}{2})(.*?)(\d)(.*?)(\d)(.*?)(\d{8}-)(\w)(.*?)\n"
    extracted_info = regex.sub(pattern2, r"\2\t\4\t\6\t\9\n", only_two_syllable, flags=regex.MULTILINE)
    cleanup_pattern = r"^[\\s\t\r]*$\n"
    clean_info = regex.sub(cleanup_pattern, "", extracted_info, flags=regex.MULTILINE)
    write_file_content("info_from_joanna.txt", str(clean_info), "")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to extract hashtags, arrange headlines from a file, extract info from vertical or extract info from cantonese analysis.")
    parser.add_argument("function", choices=["extract_hashtags", "arrange_headlines", "extract_from_vertical", "extract_from_joanna"], help="Function to run")
    parser.add_argument("path_to_file", help="Path to the file")
    args = parser.parse_args()

    while not os.path.exists(args.path_to_file):
        print("The file path provided is not valid.")
        args.path_to_file = input("Please enter a valid file path: ")

    if args.function == "extract_hashtags":
        extract_hashtags(args.path_to_file)
        print("Your twitter hashtags have been successfully extracted!")
    elif args.function == "arrange_headlines":
        arrange_headlines(args.path_to_file)
        print("Your have been rearranged!")
    elif args.function == "extract_from_vertical":
        extract_from_vertical(args.path_to_file)
        print("Information has been extracted from vertical!")
    elif args.function == "extract_from_joanna":
        extract_from_joanna(args.path_to_file)
        print("Information has been extracted from joanna!")
