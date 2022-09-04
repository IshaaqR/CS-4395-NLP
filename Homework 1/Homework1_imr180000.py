import sys
import os
import re
import pickle as pkl

# Define a Person class
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display (self):
        print('Employee id: ', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone)
        print()

# Create a function to process the input file
def process_input(path):
    persons_dict = dict()

    with open(os.path.join(os.getcwd(), path), 'r') as f:
        lines = f.read().splitlines()

    # Get rid of the first line which is just the heading line
    lines = lines[1:]

    for line in lines:  
        # Split on comma to get the fields as text variables
        attr = line.split(',')
        last, first, mi, id, phone = attr[0], attr[1], attr[2], attr[3], attr[4]

        # Modify last name and first name to bein Capital Case
        last = last.upper()
        first = first.upper()

        # Modify middle initial to be a single upper case letter
        if mi:
            mi = mi[0].upper()
        # Use ‘X’ as a middle initial if one is missing
        else:
            mi = 'X'

        # Modify id if necessary, using regex. The id should be 2 letters followed by 4 digits.
        if not re.search('[a-zA-Z]{2}\d{4}', id):
            print('ID invalid:', id)
            print('ID is two letters followed by 4 digits')
            id = input('Please enter a valid id: ')

        # Modify phone number, if necessary, to be in form 999-999-9999
        if not re.search('^[1-9]\d{2}-\d{3}-\d{4}', phone):
            print('Phone', phone, 'is invalid')
            print('Enter phone number in form 123-456-7890')
            phone = input('Enter phone number: ')

            # Create a Person object
        person = Person(last, first, mi, id, phone)

        # Save the object to a dict of persons, where id is the key
        # Check for duplicate id and print an error message if an ID is repeated in the input file
        if id in persons_dict.keys():
            print('ERROR: id', id, 'is repeated in the input file')
        else:
            persons_dict[id] = person

    # Return the dict of persons to the main function
    return persons_dict

# If the user does not specify a sysarg
if len(sys.argv) < 2:
    print('ERROR: path not specified')
    exit(0)

# The user specifies the relative path in a sysarg
path = sys.argv[1]

# Save the dictionary as a pickle file
persons_dict = process_input(path)
with open('persons.pkl', 'wb') as pkl_wb:
    pkl.dump(persons_dict, pkl_wb)

# Open the pickle file for read
with open('persons.pkl', 'rb') as pkl_rb:
    persons_unpickled = pkl.load(pkl_rb)

# Print each person using the Person display() method
print('\n\nEmployee list:\n')
for id in persons_unpickled.keys():
    persons_unpickled[id].display()