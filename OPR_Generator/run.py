import json
import re
import itertools
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


if __name__ == "__main__":
    # Get the starter sentence as a parameter from the command line
    starter_sentence = input("Enter a starter sentence: ")

    # Read in replacement possibilities from json file
    fullCombinations = json.load(open("replacements.json"))

    # Create a font object Times New Roman, 10 pt
    font = ImageFont.truetype("times.ttf", 12)
    # font = ImageFont.truetype("TimesNewRomanPSMT.ttf", 12)


    # Split the sentence into words and punctuation but keep the conjunctions 
    sentence_split = re.split(r"(\s+)", starter_sentence)
    # print(f'1. {sentence_split}')

    # Split the '.' and ',' and ';' from the words
    sentence_split = [re.split(r"([.,;])", i) for i in sentence_split]
    # print(f'2. {sentence_split}')

    # Flatten the list
    sentence_split = [item for sublist in sentence_split for item in sublist]
    # print(f'3. {sentence_split}')

    # Remove empty strings
    sentence_split = [i for i in sentence_split if i != '']
    # print(f'4. {sentence_split}')

    # Split '--' as its own element
    sentence_split = [re.split(r"(\-\-)", i) for i in sentence_split]
    # print(f'5. {sentence_split}')

    # Flatten the list
    sentence_split = [item for sublist in sentence_split for item in sublist]
    # print(f'6. {sentence_split}')



    replacements = []

    # Iterate through the sentence split
    for i in range(len(sentence_split)):
        # If the word is in any of the lists in the fullCombinations list
        for j in range(len(fullCombinations)):
            # Check if the word is in the replacement list
            if sentence_split[i] in fullCombinations[j]:
                replacements.append(fullCombinations[j])

                # Repalce the element in the sentence split with %s
                sentence_split[i] = "%s"
            # Check if only making the first letter of the word lowercase will make it in the replacement list
            elif sentence_split[i][0].lower() + sentence_split[i][1:] in fullCombinations[j]:
                # for k in fullCombinations[j]:
                #     print(k[0].upper() + k[1:])
                replacements.append([k[0].upper() + k[1:] for k in fullCombinations[j]])

                # Replace the element in the sentence split with %s
                sentence_split[i] = "%s"
            # Check if making all the letters lowercase will make it in the replacement list
            elif sentence_split[i].lower() in fullCombinations[j]:
                replacements.append([k.upper() for k in fullCombinations[j]])

                # Replace the element in the sentence split with %s
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
        # print(t)
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
        # print(temp_sentence, list(temp_sentence))

        # Calculate the length of the sentence
        length = font.getlength(temp_sentence)


        # calculate the length of the sentence in inches
        length_in_inches = length / 72

        # Append the sentence and the length to the results list
        # if length <= 600 and length >= 540:
        #     results.append((temp_sentence, length))
        results.append((temp_sentence, length))

    # Sort the results list by the length of the sentence in descending order
    results.sort(key=lambda x: x[1], reverse=True)

#     print(
#         """\nOrdered by length in ascending order.
# \nLengths are fickle so if one is too long work your way up the list
# and keep trying until you get one you like that also fits.\n

# Length 558 seems to be the sweet spot.

# Results:\n
#         """
#     )

    for result in results:
        print(result[0], '\tLength:', result[1], font.getbbox(result[0])[2])
        # image = Image.new('RGB', font.getsize(result[0]))
        # draw = ImageDraw.Draw(image)
        # draw.text((0,0), result[0], font=font)
        # # Show the image
        # image.show()

        