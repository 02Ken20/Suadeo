import os
import csv


print("Create a new folder? y/n: ")
answer = input()
if (answer == "y"):
    print("Enter the name of a folder: ")
    folder_name_input = input()

    current_directory = os.getcwd()
    path = current_directory + f"\\{folder_name_input}"

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = "user_folder_data.csv"
    csv_path = path + f"\\{file_name}"

    if not os.path.exists(csv_path):
        # If the file doesn't exist, create a new one with a header row
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['item_name'])

    # Check if 'item_name' row exists
    item_name_exists = False
    with open(csv_path, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header:
            for column in header:
                if column == 'item_name':
                    item_name_exists = True
                    break

    print("Add an item? y/n: ")
    answer = input()
    if answer == "y":
        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not item_name_exists:
                writer.writerow(['item_name'])
            print("Enter the name of an item: ")
            user_input = input()
            writer.writerow([user_input])
