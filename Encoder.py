import os
from bitstring import BitArray
"""The encoder used for creating the huffman encoded file in the formate .bin"""
def gather_values(file_name) -> list:
    """Takes the text file and then finds each unique character within it
    and the frequency that they apper so that the Huffman tree can be created"""
    chars = []
    with open(file_name, 'r', encoding='utf-8') as file1:
        #takes each character in each line of the file
        for line in file1:
            for char in line:

                #first see if the character is already in the file
                pos = binary_search(chars, char, 0, len(chars)-1, "character")
                if pos >= 0:
                    #if it is increments its value by 1
                    chars[pos]['value'] += 1

                #finds the position to add the new chacter if it isnt already in the file
                else:
                    pos = add_new_item(chars, char, 0, len(chars)-1, "character")
                    if pos >= 0:
                        chars.insert(pos, {'character': char, 'value': 1})
                    else:
                        chars.append({'character': char, 'value': 1})

    return chars


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



def binary_search(search_list: list, search_value, first: int, last: int, dict_value: str) -> int:
    """A simple binary search algorithm for finding a specific value efficiently. This is used to 
    quickly find a value when it needs to be incrmented thank to the list being sorted using
    add_new_item() and quicksort()"""

    #if the item isnt in the search_list return the rouge value of -1
    try:
        if first > last:
            return -1
        #finds the midpoint of the remaining value
        middle_point = (first + last) // 2

        #finds the relative position of a point and then repeates the search
        if search_value == search_list[middle_point][dict_value]:
            return middle_point 
        elif search_value > search_list[middle_point][dict_value]:
            return binary_search(search_list, search_value, middle_point+1, last, dict_value)
        elif search_value < search_list[middle_point][dict_value]:
            return binary_search(search_list, search_value, first, middle_point-1, dict_value)

    except KeyError:
        return -1


def add_new_item(search_list: list, new_value, first: int, last: int, dict_value: str) -> int:
    """A simple binary search algorithm for finding where a new value should be added to a list
    Uses a binary search like system to find a position without a value which is where a new value
    should be inserted into the list."""
    try:
        #if the item isnt in the search_list return the position to insert the new item
        if first > last:
            return first
        #finds the midpoint of the remaining value
        middle_point = (first + last) // 2
        
        #finds the relative position of a point and then repeates the search
        if new_value == search_list[middle_point][dict_value]:
            return middle_point
        elif new_value > search_list[middle_point][dict_value]:
            return add_new_item(search_list, new_value, middle_point+1, last, dict_value)
        elif new_value < search_list[middle_point][dict_value]:
            return add_new_item(search_list, new_value, first, middle_point-1, dict_value)

    except KeyError:
        return -1


def binary_tree(queue: list) -> list:
    """The system used to generate a binary tree once all values have been collected
    This works through a queue system taking the two smallest values, assigning a
    binary value to it and then combining them into one item in the queue"""
    #first sends the queue to be sorted
    binary_tree = []
    queue = quicksort(queue, "value")
    while len(queue) > 1:
        #takes the two smallest values and combineds them into one value
        temp_store_character = queue[0]["character"] + queue[1]["character"]

        if len(queue[0]["character"]) == 1:
            binary_tree = new_tree_position(queue[0]["character"], 0, binary_tree)
        else:
            binary_tree = grow_tree(queue[0]["character"], 0, binary_tree)

        if len(queue[1]["character"]) == 1:
            binary_tree = new_tree_position(queue[1]["character"], 1, binary_tree)
        else:
            binary_tree = grow_tree(queue[1]["character"], 1, binary_tree)

        temp_store_value = queue[0]["value"] + queue[1]["value"]
        #removes the no longer needed values from the queue
        queue.pop(0)
        queue.pop(0)

        #finds the correct position for the new value and then adds it to the list
        new_position = add_new_item(queue, temp_store_value, 0, len(queue)-1, "value")
        queue.insert(new_position, {"character": temp_store_character, "value": temp_store_value})

    return binary_tree


def new_tree_position(character: str, binary_digit: int, binary_tree: list) -> list:
    """Adds a new character to the binary tree the first time it was called
    The items are positioned in order based on their character and therefor the new
    a search is used to find the correct alphabetic position of the character"""
    if binary_tree:
        position = add_new_item(binary_tree, character, 0, len(binary_tree)-1, "character")
        binary_tree.insert(position, {"character": character, "binary code": str(binary_digit)})
    else:
        binary_tree = [{"character": character, "binary code": str(binary_digit)}] 

    return binary_tree


def grow_tree(character: str, binary_digit: int, binary_tree: list) -> list:
    """Updates the values for all items in the search_list
    Finds each char in the updated position and add the binary character selected
    to each at the begining of its value"""
    for char in character:
        position = binary_search(binary_tree, char, 0, len(binary_tree)-1, "character")
        binary_tree[position]["binary code"] = str(binary_digit) + binary_tree[position]["binary code"]

    return binary_tree


def output(tree: list, file_name: str):
    """Takes the tree values and uses them to create the output.bin file"""
    file2=open(file_name[:-3]+"bin", "wb")
    codes = ""
    for item in tree:
        #stores char length, char length
        if len(item['character'].encode('utf8')) > 1:
            file2.write(bytes("?".encode('utf8')))
        else:
            file2.write(bytes(item['character'].encode('utf8')))


        length = len(item['binary code'])
        length = BitArray(bin=(format(length, '08b')))
        length.tofile(file2)

        #stores all the codes in one long line
        codes += item['binary code']

    #2 bytes of all 1's follwed by a new line to represent the end of the section
    clear = BitArray(bin='11111111')
    for i in range(2):
        clear.tofile(file2)
    file2.write(bytes("\n".encode('utf8')))

    #writes all the characters codes to the file in one long string
    codes = BitArray(bin=codes)
    codes.tofile(file2)

    #writes a newline character to begin the next section
    file2.write(bytes("\n".encode('utf8')))

    #writes the actual data in the huffman format
    file1=open(file_name, "r", encoding='utf-8')
    value=""
    for line in file1:
        for char in line:
            pos = binary_search(tree, char, 0, len(tree)-1, "character")
            value += tree[pos]['binary code']

            #only writes in lots of 8bits to reduces the amount of wasted bits
            if len(value) % 8 == 0:
                value = BitArray(bin=value)
                value.tofile(file2)
                value = ""


    value = BitArray(bin=value)
    value.tofile(file2)

    file1.close()
    file2.close()


#the main menu that the user interact with for encoding the file
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    #Enter the name of the file here, please make sure it is in the same file as this main.py
    print("               Huffman Encoder")
    print("___________________________________________________________\n\n")

    file_name = ""

    while file_name != "-1":
        print("Please enter one of the following:\n   your file name in the folder res")
        print("   -1 to exit\n\n")
        file_name = input("Enter your file name: ")
        os.system('cls' if os.name == 'nt' else 'clear')

        if file_name == "":
            file_name = "res/Christmas Carol English.txt"

        elif file_name  =="-1":
            break

        else:
            file_name = "res/"+file_name

        try:
            res = gather_values(file_name)

            tree = binary_tree(res)
            tree2 = quicksort(tree, 'binary code')

            output(tree, file_name)

            print("file successfully created.\n\n\n")

        except FileNotFoundError:
            print("Could not generate a binary tree for a file not in /res/your_file_name.txt")