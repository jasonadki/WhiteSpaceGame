import json
import re
import itertools
from PIL import ImageFont



if __name__ == "__main__":
    # Get the starter sentence as a parameter from the command line
    starter_sentence = input("Enter a starter sentence: ")

    # Read in replacement possibilities from json file
    fullCombinations = json.load(open("replacements.json"))

    # Create a font object Times New Roman, 10 pt
    font = ImageFont.truetype("times.ttf", 12)


    # Split the sentence into words and punctuation but keep the conjunctions 
    sentence_split = re.split(r"(\s+)", starter_sentence)

    # Split the '.' and ',' and ';' from the words
    sentence_split = [re.split(r"([.,;])", i) for i in sentence_split]

    # Flatten the list
    sentence_split = [item for sublist in sentence_split for item in sublist]

    # Remove empty strings
    sentence_split = [i for i in sentence_split if i != '']

    # Split '--' as its own element
    sentence_split = [re.split(r"(\-\-)", i) for i in sentence_split]

    # Flatten the list
    sentence_split = [item for sublist in sentence_split for item in sublist]



    replacements = []

    # Iterate through the sentence split
    for i in range(len(sentence_split)):
        # If the word is in any of the lists in the fullCombinations list, print the word and the list it is in
        for j in range(len(fullCombinations)):
            if sentence_split[i] in fullCombinations[j]:
                replacements.append(fullCombinations[j])

                # Repalce the element in the sentence split with %s
                sentence_split[i] = "%s"

    
    # Convert the sentence split list into a string
    sentence_with_placeholders = "".join(sentence_split)


    results = []
    # Try all the combinations of the replacements list and print the length of each combination
    for i in itertools.product(*replacements):
        temp_sentence = sentence_with_placeholders % i

        # Need to check if there are any 'a' or 'an' in the sentence
        # If there is, check if the next word starts with a vowel
        # If it does, replace 'a' with 'an' and vice versa
        # If it doesn't, replace 'an' with 'a' and vice versa
        t = temp_sentence.split()
        for j in range(len(t)):
            if t[j] == 'a' or t[j] == 'an':
                if t[j+1][0] in ['a', 'e', 'i', 'o', 'u']:
                    # And if the second letter isn't 'n' or the first two letters aren't 'un' or 'im' or 'in'
                    if t[j+1][1] != 'n' and t[j+1][:2] not in ['un', 'im', 'in']:
                        t[j] = 'an'
                    # t[j] = 'an'
                else:
                    t[j] = 'a'

        temp_sentence = " ".join(t)

        temp_sentence = '- ' + temp_sentence

        # Calculate the length of the sentence
        length = font.getsize(temp_sentence)[0]

        # Append the sentence and the length to the results list
        if length <= 600 and length >= 540:
            results.append((temp_sentence, length))
        # results.append((temp_sentence, length))

    # Sort the results list by the length of the sentence in descending order
    results.sort(key=lambda x: x[1], reverse=True)

    print(
        """\nOrdered by length in ascending order.
\nLengths are fickle so if one is too long work your way up the list
and keep trying until you get one you like that also fits.\n

Length 558 seems to be the sweet spot.

Results:\n
        """
    )

    for result in results:
        print(result[0], '\tLength:', result[1])

        