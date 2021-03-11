from bitstring import BitArray
import os
"""Huffman Decoder, takes .bin files created by the encoder and returns a text file with
the original contents of the file in it."""
def quicksort(sort_list: list, dict_value: str) -> list:
    """A simple quicksort function used to order a series of numbers based on there size
    Splits the list in too smaller and smaller lists of the values lower and higher than
    the first value of the currently list, allowing them to be sorted
    When the length of the list passed into the function is less than 5 an insertion sort
    is used instead"""

    #creats 3 lists to sort the values into
    lower_than_pivot = []
    equal_to_pivot = []
    higher_than_pivot = []

    #if there is still more than 5 items quicksort else insertion sort
    if len(sort_list) > 5:
        pivot = sort_list[0][dict_value]
        for item in sort_list:
            #for each value in the the search_list sorts them into less than, greater than and equal to
            if item[dict_value] > pivot:
                higher_than_pivot.append(item)
            elif item[dict_value] < pivot:
                lower_than_pivot.append(item)
            elif item[dict_value] == pivot:
                equal_to_pivot.append(item)

        #returns the combined groups into the quicksort loop above
        return quicksort(lower_than_pivot, dict_value) + equal_to_pivot + quicksort(higher_than_pivot, dict_value)
    else:
        return insertionsort(sort_list, dict_value)


def insertionsort(sort_list: list, dict_value: str) -> list:
    """When the list of values gets to 5 or less insertion sort is used becuase,
    despite its slower avarage time to sort it reduces the amount of recursions required
    in turn making the programme more efficent"""
    pos = len(sort_list) -1

    while pos > 0:
        indexNew = pos -1
        valueNew = sort_list[indexNew]

        while indexNew < len(sort_list) -1 and valueNew[dict_value] > sort_list[indexNew+1][dict_value]:
            sort_list[indexNew] = sort_list[indexNew+1]
            indexNew += 1

        sort_list[indexNew] = valueNew
        pos -= 1

    return sort_list

def search1(tree: list, first: int, last: int, digit_num) -> int:
    """Takes the tree and elimiantes all character that can no longer be correct once the new
    binary bit is added, since the digit at the position is one the first value is updated """
    found = False
    last_dig = ""

    first = (first + last)//2

    while found == False:
        #The edge is found when the bit changes
        if tree[first]["binary code"][digit_num] == "1" and last_dig != "0":
            last_dig = "1"
            first -= 1

        elif tree[first]["binary code"][digit_num] == "1" and last_dig == "0":
            return first
            found = True

        elif tree[first]["binary code"][digit_num] == "0" and last_dig != "1":
            last_dig = "0"
            first += 1

        elif tree[first]["binary code"][digit_num] == "0" and last_dig == "1":
            return first+1
            found = True


def search0(tree: list, first: int, last: int, digit_num) -> int:
    """Takes the tree and elimiantes all character that can no longer be correct once the new
    binary bit is added, since the digit at the position is zero the last value is updated"""
    found = False
    last_dig = ""
    last = (first + last)//2

    while found == False:
        #The edge is found when the bit changes
        if tree[last]["binary code"][digit_num] == "1" and last_dig != "0":
            last_dig = "1"
            last -= 1

        elif tree[last]["binary code"][digit_num] == "1" and last_dig == "0":
            return last-1
            found = True

        elif tree[last]["binary code"][digit_num] == "0" and last_dig != "1":
            last_dig = "0"
            last += 1

        elif tree[last]["binary code"][digit_num] == "0" and last_dig == "1":
            return last
            found = True





def gather_tree(file_name: str) -> list:
    """Takes the file and creates a new structure storing the
    character, length, code in the format
    [{'character': char, 'length': len, 'binary code': code},]"""
    tree = []

    break_out = 0
    binary=""

    char = ""
    length = 0

    last_char = False
    part = 1

    binary = ""
    first = 0
    last = 0
    digit_num = 0

    file1 =open(file_name, 'rb')
    file2=open(file_name[:-4]+" output.txt", "w")

    for line in file1:
        #defines the first stage of the decode process, gathing all characters and their length
        if part == 1:

            bits_line = BitArray(line)

            for bit in bits_line:
                if bit == True:
                    binary += "1"
                else:
                    binary += "0"

                if len(binary) == 8 and last_char == False:
                    if binary == "11111111":
                        break_out += 1

                    else:
                        break_out = 0

                    char = chr(int(binary, 2))
                    #resets binart and makes sure that it knows the next byte is a num
                    binary=""
                    last_char = True

                elif len(binary) == 8 and last_char == True:

                    if break_out == 1 and binary == "11111111":
                        binary = ""
                        break_out += 1

                    elif binary == "11111111":
                        break_out += 1

                        length = int(binary, 2)

                        binary = ""
                        tree.append({'character': char, 'length': length})

                        char=""
                        length = 0
                        last_char = False

                    else:
                        break_out = 0
                        length = int(binary, 2)

                        binary = ""
                        tree.append({'character': char, 'length': length})

                        char=""
                        length = 0
                        last_char = False
            
                if break_out == 2:
                    part = 2
                    break
        
        #Defines how to gather all the tree binary codes once the character and length are known
        elif part == 2:
            binary=""
            current_pos = 0
            bits_line = BitArray(line)

            for bit in bits_line:
                if bit == True:
                    binary += "1"
                else:
                    binary += "0"
                
                if len(binary) == tree[current_pos]['length']:
                    tree[current_pos]['binary code'] = binary
                    binary = ""
                    current_pos += 1

                    if current_pos == len(tree):
                        tree = quicksort(tree, 'binary code')
                        part = 3
                        last = len(tree)-1
                        break
        
        #part 3 uses the tree values to actually decode the file back to text
        elif part == 3:
            
            bits_line = BitArray(line)
            for bit in bits_line:

                if bit == True:
                    first = search1(tree, first, last, digit_num)

                else:
                    last = search0(tree, first, last, digit_num)
                
                digit_num += 1

                if first == last:
                    file2.write(tree[first]['character'])

                    first = 0
                    last = len(tree)-1
                    digit_num = 0

    file1.close()
    file2.close()


if __name__=="__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("               Huffman Decoder")
    print("___________________________________________________________\n\n")
    print("Only .bin files produced by the encoder can be decoded\n")

    file_name = ""

    while file_name != "-1":
        print("Please enter one of the following:\n   your file name in the folder res")
        print("   -1 to exit\n\n")
        file_name = input("Enter your file name: ")
        os.system('cls' if os.name == 'nt' else 'clear')

        if file_name  =="-1":
            break

        elif file_name[-4:] == ".bin":
            file_name = "res/"+file_name

            try:
                tree = gather_tree(file_name)

                print("File successfully decode it can be found at", file_name[:-4], "output.txt\n\n\n")

            except FileNotFoundError:
                print("Could not generate a binary tree for a file not in /res/your_file_name.bin\n\n\n")

            except:
                print("Error! Invalid file not created by Encoder.py\n\n\n")
        
        else:
            print("Error can only take files created by Encoder.py in the format of .bin\n\n\n")