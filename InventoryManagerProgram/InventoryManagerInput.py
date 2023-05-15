import csv
from datetime import datetime, date


class InventoryItem:  # creating InventoryItem class and defining it
    # creating constructor that initialize the variables for InventoryItem object
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged=False):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

    # defining class to represent as a string
    def __str__(self):
        # returning objects with items in the objects
        return f"{self.item_id},{self.manufacturer},{self.item_type},{self.price},{self.service_date},{self.damaged}"


# defining read_manufacturer_list that will take in the file name as a parameter
def read_manufacturer_list(file_name):
    # creating empty dictionary for storing manufacturer names and their ID numbers
    manufacturer_list = {}
    # opening csv file and reading it
    with open(file_name, 'r') as file:
        # csv reader object
        reader = csv.reader(file)
        # skip header row
        next(reader)
        # looping through each row in the file
        for row in reader:
            # mapping the manufacturer names to ID numbers
            manufacturer_list[row[0]] = row[1:]
    # returning manufacturer names and their ID numbers
    return manufacturer_list


# defining read_price_list that will take in the file name as parameter
def read_price_list(file_name):
    # creating empty dictionary for storing the price listings
    price_list = {}
    # opening csv file and reading it
    with open(file_name, 'r') as file:
        # csv reader object
        reader = csv.reader(file)
        # skip header row
        next(reader)
        # looping through each row in the file
        for row in reader:
            # adding key-value pair to the price list dictionary, where the key is the item name
            price_list[row[0]] = float(row[1])
    # returning price list dictionary
    return price_list


# defining read_service_dates_list that will take the file name as parameter
def read_service_dates_list(file_name):
    # creating empty dictionary service_dates_list to store the service_dates
    service_dates_list = {}
    # opening csv file and reading it
    with open(file_name, 'r') as file:
        # skip header row
        reader = csv.reader(file)
        # skipping header row of the file
        next(reader)
        # looping through each row in the csv file
        for row in reader:
            # converting service date from the csv file to datetime object
            service_dates_list[row[0]] = datetime.strptime(
                # parsing and converting to date object
                row[1], '%m/%d/%Y').date()
    # returning completed service dates list dictionary
    return service_dates_list


# defining merge_data that will take the three dictionaries as parameters
# manufacturer_list, price_list, service_dates_list
def merge_data(manufacturer_list, price_list, service_dates_list):
    # creating an empty list to store the inventory items
    inventory_list = []
    # looping through each item_id in manufacturer_list
    for item_id in manufacturer_list:
        # verifying whether the item_id is present in all the provided lists
        if item_id in price_list and item_id in service_dates_list:
            # extracting manufacturer, item_type, and damaged status from the manufacturer_list dictionary
            manufacturer, item_type, damaged = manufacturer_list[item_id]
            # extracting the price from the price_list dictionary
            price = price_list[item_id]
            # extracting the service date from the service_dates_list dictionary
            service_date = service_dates_list[item_id]
            # converting the 'damaged' string to boolean value
            damaged = damaged.strip() == "damaged"
            # creating new InventoryItem object with the extracted data, and adding it to inventory_list
            inventory_item = InventoryItem(
                item_id, manufacturer, item_type, price, service_date, damaged)
            inventory_list.append(inventory_item)
    # returning completed inventory list
    return inventory_list


# defining get_manufacturer function that will take InventoryItem object as input and returning manufacturer
def get_manufacturer(item):
    return item.manufacturer


# defining function create_full_inventory that will take the two parameters inventory_list and file_name
def create_full_inventory(inventory_list, file_name):
    # sorting inventory_list in ascending order by manufacturer name using get_manufacturer as key
    inventory_list = sorted(inventory_list, key=get_manufacturer)
    # opening file
    with open(file_name, 'w', newline='') as file:
        # creating csv writer
        writer = csv.writer(file)
        # for loop to iterate over items in inventory_list and writing item's attributes to a new row in csv file
        for item in inventory_list:
            # converting boolean damaged status to string
            damaged_status = 'True' if item.damaged else 'False'
            # writing attributes to new row in csv file
            writer.writerow([item.item_id, item.manufacturer, item.item_type,
                             item.price, item.service_date, damaged_status])
    # outputting that the file has been created
    print(f'Created FullInventory.csv: {file_name}')


# defining get_item_id function that will take InventoryItem object as input and returning item_id
def get_item_id(item):
    return item.item_id


# defining create_item_type_inventory that will take inventory_list as input and create files for each item type
def create_item_type_inventory(inventory_list):
    # getting item types from inventory list
    item_types = set(item.item_type for item in inventory_list)
    # for each item type, create csv file with the item type
    for item_type in item_types:
        # creating file name
        file_name = f"{item_type}Inventory.csv"
        # sorting inventory_list by item id
        inventory_list = sorted(inventory_list, key=get_item_id)
        # opening file and writing to it
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for item in inventory_list:
                # writing items with the current item type
                if item.item_type == item_type:
                    writer.writerow(
                        [item.item_id, item.manufacturer, item.price, item.service_date, item.damaged])


# defining get_date_id function that will take the InventoryItem object as input and returning the service date
def get_date_id(item):
    return item.service_date


# defining create_past_service_date_inventory that will take inventory_list and file_name as input
def create_past_service_date_inventory(inventory_list, file_name):
    # creating csv file containing all items that have service_date earlier than current date
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # getting current date and sorting inventory list by service date from oldest to most recent
        past_date = date.today()
        inventory_list = sorted(inventory_list, key=get_date_id, reverse=False)
        # for loop to iterate through the sorted inventory list the items with service date earlier than date in csv
        for item in inventory_list:
            if item.service_date < past_date:
                writer.writerow([item.item_id, item.manufacturer, item.item_type,
                                 item.price, item.service_date, item.damaged])
    # outputting to confirm that the past service inventory file has been created
    print(f"Created past service inventory file: {file_name}")


# defining get_damage_id function that will take InventoryItem object as input and returning price
def get_damage_id(item):
    return item.price


# creating create_damaged_inventory that will take inventory_list and file_name as input
def create_damaged_inventory(inventory_list, file_name):
    # sorting inventory list based on the price of each item and sorting from most expensive to the least expensive
    inventory_list = sorted(inventory_list, key=get_damage_id, reverse=True)
    # creating csv file that contains all damaged items
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in inventory_list:
            if item.damaged:
                # writing details of each damaged items to csv file
                writer.writerow([item.item_id, item.manufacturer,
                                 item.item_type, item.price, item.service_date])
    # outputting to confirm the creation of the damaged inventory file
    print(f"Created damaged inventory file: {file_name}")


# defining sort_by_price function that will take item as argument and return price
def sort_by_price(item):
    return item[3]


# defining the interactive_inventory_query based on user input
def interactive_inventory_query(inventory_list):
    while True:
        # prompting user to input a manufacturer and an item type or press 'q' to quit
        input_str = input("\nPlease enter an item manufacturer and item type (or 'q' to quit): ")
        # breaking out of loop if user enters 'q'
        if input_str.lower() == 'q':
            break
        # splitting input into individual words
        words = input_str.split()
        # extracting the last two words from the input, and converting them to lowercase
        manufacturer, item_type = [word.lower() for word in words[-2:]]
        # initializing empty list to store items that match the user's query
        items = []
        # for loop through all items in inventory_list
        for item in inventory_list:
            # if the item's manufacturer and the item type match the user's input
            if item.manufacturer.lower() == manufacturer and item.item_type.lower() == item_type:
                # skipping item if it is past service date or damaged
                if item.service_date and datetime.now().date() >= item.service_date:
                    continue
                if item.damaged:
                    continue
                # adding item's ID, manufacturer, item type, and price as a tuple to the list of items
                items.append((item.item_id, item.manufacturer, item.item_type, item.price))
        # printing error message if no items were found
        if not items:
            print("No such item in inventory.")
            # continuing through next iteration
            continue
        # sorting list of items by price in descending order
        items_sorted = sorted(items, key=sort_by_price, reverse=True)
        # extracting the ID, manufacturer, item type, and price of the most expensive item
        item_id, manufacturer, item_type, price = items_sorted[0]
        # printing to user most expensive item's credentials
        print(f"Your item is: {item_id} {manufacturer} {item_type} {price}")
        # initializing empty list to store similar items that match the item type but different manufacturer
        similar_items = []
        # for looping through all items in inventory_list
        for item in inventory_list:
            # if the item's manufacturer does not match the user's query but the item type does
            if item.manufacturer.lower() != manufacturer and item.item_type.lower() == item_type:
                # if the item is past its service date or damaged, skipping item
                if item.service_date and datetime.now().date() >= item.service_date:
                    continue
                if item.damaged:
                    continue
                # adding item information as a tuple to list of similar items
                similar_items.append((int(item.item_id), item.manufacturer, item.item_type, item.price))
        # sorting item price in ascending order if there are similar items
        if similar_items:
            # printing item with the lowest price
            similar_items_sorted = sorted(similar_items, key=sort_by_price)
            similar_item_id, similar_manufacturer, similar_item_type, similar_price = similar_items_sorted[0]
            print(
                f"You may also consider: {similar_item_id} {similar_manufacturer} {similar_item_type} {similar_price}")


# defining main function
def main():
    # reading manufacturer list from file
    manufacturer_list = read_manufacturer_list("ManufacturerList.csv")
    # reading price list from file
    price_list = read_price_list("PriceList.csv")
    # reading service dates list from file
    service_dates_list = read_service_dates_list("ServiceDatesList.csv")
    # merging all data to create inventory list
    inventory_list = merge_data(
        manufacturer_list, price_list, service_dates_list)
    # creating full inventory
    create_full_inventory(inventory_list, 'FullInventory.csv')
    # creating item type inventory list
    create_item_type_inventory(inventory_list)
    # creating past service date inventory
    create_past_service_date_inventory(
        inventory_list, "PastServiceDateInventory.csv")
    # creating damaged inventory
    create_damaged_inventory(inventory_list, "DamagedInventory.csv")
    # defining interactive inventory query function to allow user to search for items based on various criteria
    interactive_inventory_query(inventory_list)


# calling main function
if __name__ == "__main__":
    main()
