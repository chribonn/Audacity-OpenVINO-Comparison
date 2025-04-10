import sys
import difflib
import string
import os

def print_and_log(text, filename="output.md"):
    """
    Prints the given text to the screen and simultaneously logs it to a text file.

    Args:
        text (str): The text to be printed and logged.
        filename (str, optional): The name of the text file to log to.
                                   Defaults to "output.txt".
    """
    # Print to the screen (standard output)
    print(text)

    # Open the file in append mode ('a') so new output is added
    with open(filename, "a") as f:
        # Write the text to the file, ensuring a newline character
        f.write(text + "\n")


def ignore_timings(file_content):
    # translator = str.maketrans('', '', '.,')
    
    result = []
    for line in file_content.splitlines():
        # Split the line by tabs
        parts = line.split('\t', 2)
        # Check if there are at least 3 parts (to ensure a second tab exists)
        if len(parts) > 2:
            result.append(parts[2].strip())  # Append the part after the second tab
    return ' '.join(result).lower()  # Concatenate all parts into a single string

     
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python score.py <path to directory where Audacity transcription files are stored>")
        sys.exit(1)

    audacity_path = sys.argv[1]
    source_path = os.path.join(audacity_path, "Source.txt")
    # Create the file that will store the result output
    mf_file_path = os.path.join(audacity_path, "output.md")
    try:
        os.remove(mf_file_path)
    except FileNotFoundError: 
        pass
    
    
    # Load the source file
    try:
        with open(source_path, 'r') as file1:
            source_content = file1.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    translator = str.maketrans('', '', '.,')
    source_text_only = ignore_timings(source_content)
    
    cnt = 1
    print_and_log(f"| {"#".center(4)} | Source text: Unprocessed |", mf_file_path)
    print_and_log(f"| {'-'*4} | ------- |", mf_file_path)
    for line in source_content.splitlines():
        print_and_log(f"| {cnt:4} |{line} |", mf_file_path)
        cnt += 1
    print_and_log("", mf_file_path)
          
    
    cnt = 1
    print_and_log(f"| {"#".center(4)} | Source text: No Timings/Lower Case/No NL |", mf_file_path)
    print_and_log(f"| {'-'*4} | ------- |", mf_file_path)
    for line in source_text_only.splitlines():
        print_and_log(f"| {cnt:4} |{line} |", mf_file_path)
        cnt += 1
    print_and_log("", mf_file_path)
          
    
    cnt = 1
    print_and_log(f"| {"#".center(4)} | Source text: No Timings/Lower Case/No NL/No Punctuation |", mf_file_path)
    print_and_log(f"| {'-'*4} | ------- |", mf_file_path)
    for line in source_text_only.splitlines():
        print_and_log(f"| {cnt:4} |{line.translate(translator)} |", mf_file_path)
        cnt += 1
    print_and_log("", mf_file_path)
    
    scores = dict()
    
    # Iterate through the models - output the text and compute the scores
    for model in  ["base", "small", "medium", "large-v3"]:

        file_path = os.path.join(audacity_path, f"Transcription({model}).txt")

        # Load the compare file
        try:
            with open(file_path, 'r') as file1:
                compare_content = file1.read()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

        compare_text_only = ignore_timings(compare_content)

        cnt = 1  
        print_and_log(f"| {"#".center(4)} | {model} text: Unprocessed |", mf_file_path)
        print_and_log(f"| {'-'*4} | ------- |", mf_file_path)
        for line in compare_content.splitlines():
            print_and_log(f"| {cnt:4} |{line} |", mf_file_path)
            cnt += 1
        print_and_log("", mf_file_path)
          
    
        cnt = 1
        print_and_log(f"| {"#".center(4)} | {model} text: No Timings/Lower Case/No NL |", mf_file_path)
        print_and_log(f"| {'-'*4} | ------- |", mf_file_path)
        for line in compare_text_only.splitlines():
            print_and_log(f"| {cnt:4} |{line} |", mf_file_path)
            cnt += 1
        print_and_log("", mf_file_path)
          
    
        cnt = 1
        print_and_log(f"| {"#".center(4)} | {model} text: No Timings/Lower Case/No NL/No Punctuation |", mf_file_path)
        print_and_log(f"| {'-'*4} | ------- |", mf_file_path)
        for line in compare_text_only.splitlines():
            print_and_log(f"| {cnt:4} |{line.translate(translator)} |", mf_file_path)
            cnt += 1
        print_and_log("", mf_file_path)


        # Calculate similarity score for unaltered text
        score = difflib.SequenceMatcher(None, source_content, compare_content).ratio()*100
        
        # Calculate similarity score for text ignoring case and punctuation
        score_notimings_ignore_case = \
            difflib.SequenceMatcher(None, source_text_only, compare_text_only).ratio()*100
       
        # Calculate similarity score for text ignoring case and punctuation
        score_notimings_ignore_case_nopunctuation = \
            difflib.SequenceMatcher(None, source_text_only.translate(translator), compare_text_only.translate(translator)).ratio()*100

        scores[model] = [score, score_notimings_ignore_case, score_notimings_ignore_case_nopunctuation]
        

    # Print the scores in a table format
    print_and_log(f"| {"".ljust(10)} | {"Unprocessed".rjust(30)} | {"No Timings/LCase/no NL".rjust(30)} | {"No Timings/LCase/no NL Punct".rjust(30)} |", mf_file_path)
    print_and_log(f"| {'-'*10} | {'-'*30} | {'-'*30} | {'-'*30} |", mf_file_path)
    
    # Iterate through the models - output the text and compute the scores
    for model in  ["base", "small", "medium", "large-v3"]:
        score = scores[model][0]
        score_notimings_ignore_case = scores[model][1]
        score_notimings_ignore_case_nopunctuation = scores[model][2]
        print_and_log(f"| {model.ljust(10)} | {score:30.2f} | {score_notimings_ignore_case:30.2f} | {score_notimings_ignore_case_nopunctuation:30.2f} |", mf_file_path)
    print_and_log("", mf_file_path)

    