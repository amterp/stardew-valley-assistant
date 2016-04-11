#------------------------------------------------------------------------------
# Original author:  Terpal47
# Contributors:     jjcf89
# Creation date:    09/04/2016
# Description:      As assistant application that allows the user to input the
#                   date, budget, and desired number and types of seeds in the
#                   video game Stardew Valley, and returns the optimal types
#                   and amounts of seeds to purchase.
#------------------------------------------------------------------------------
import os
import csv

# Define several dictionaries and lists to be used globally.
season_crops = {
"spring": ["Cauliflower", "Garlic", "Green Bean", "Kale", "Parsnip", \
"Potato", "Rhubarb", "Strawberry", "Blue Jazz", "Tulip"],

"summer": ["Blueberry", "Corn", "Hops", "Hot Pepper", "Melon", \
"Radish", "Red Cabbage", "Starfruit", "Tomato", "Wheat", "Poppy", \
"Summer Spangle"],

"fall": ["Amaranth", "Artichoke", "Beet", "Bok Choy", "Cranberries", \
"Corn", "Eggplant", "Grape", "Pumpkin", "Yam", "Fairy Rose", "Sunflower"]
}

# A list containing all the names of multi-harvestable crops.
multiharvest_crops = ["Green Bean", "Strawberry", "Blueberry", "Corn", \
"Hops", "Hot Pepper", "Tomato", "Cranberries", "Eggplant", "Grape"]

# Creates a dictionary containing the buy and sell price of crops. Retrieves
# values from crops_store_values.csv
crops_store_values = {}
with open('crops_store_values.csv') as crop_values:
    read_csv = csv.reader(crop_values, delimiter=',')

    for row in read_csv:
        if len(row) == 0 or row[0][0] == "#":
            continue
        else:
            crops_store_values[row[0]] = {"buy": float(row[1]), 'sell': \
                                                                float(row[2])}

# Creates a dictionary containing the grow_time, produce time (if applicable),
# harvests per crop, and yield of each crop. Retrieves the values from 
# crops_growth_values.csv
crops_growth_values = {}
with open('crops_growth_values.csv') as crop_growth:
    read_csv = csv.reader(crop_growth, delimiter=',')

    for row in read_csv:
        # Tells it to ignore empty lines and lines starting with # (to allow 
        # for commenting on the .csv file)
        if len(row) == 0 or row[0][0] == "#":
            continue
        elif row[0] in multiharvest_crops:
            crops_growth_values[row[0]] = {"grow_time": float(row[1]), \
            'produce_time': float(row[2]), "harvests/crop": float(row[3]), \
                                                        "yield": float(row[4])}
        else:
            crops_growth_values[row[0]] = {"grow_time": float(row[1]), \
                        "harvests/crop": float(row[2]), "yield": float(row[3])}

def clear_screen():
    """
    Clears the window
    """
    # More cross-platform http://stackoverflow.com/a/684344/780194
    os.system('cls' if os.name=='nt' else 'clear')


def main_menu():
    """
    Brings up the main menu and its choices.
    """
    error = False
    while True:
        clear_screen()

        options = ["Assist purchase", "Exit"]
        print("What can I do for you?")
        # Prints out the options array in a numbered fashion
        print_options(options)
        if error:
            print("Sorry I don't understand. Please enter either 1 or 2.")
        else:
            print("")

        p_input = input()
        if p_input == "1":
            season       = set_season()
            date         = set_date()
            budget       = set_budget()
            number_seeds = set_number_seeds()
            type_seeds   = set_type_seeds(season, date)
            determine_purchase(budget, number_seeds, type_seeds)
            break
        elif p_input == "2":
            print("Goodbye!")
            break
        else:
            error = True

def print_options(array, nummed=1, direction="horiz"):
    """
    Defines a function that takes in options in an array and prints them out
    # numbered if nummed = 1 or plainly if nummed = 2. dir determines if they 
    are printed out horizontally or vertically.
    """
    to_print = []
    if (nummed):
        for option in range(0 ,len(array)):
            # if-else statement that prevents options from becoming vertically
            # disaligned due to option numbering reaching 2 digits in length.
            if len(array) >= 9 and direction == "vert" and (option + 1) < 10:
                to_print.append("{}.  {}".format(option + 1, array[option]))
            else:
                to_print.append("{}. {}".format(option + 1, array[option]))
    else:
        for option in range(0 ,len(array)):
            to_print.append(array[option])

    if direction == "horiz":
        print('     '.join(to_print))
    elif direction == "vert":
        for option in to_print:
            print(option)

def set_season():
    """
    Facilitates the user entering what season it is. Returns the appropriate
    string.
    """
    error = False
    while True:
        clear_screen()

        options = ["Spring", "Summer", "Fall"]
        print("What season is it?")
        # Prints out the options array in a numbered fashion
        print_options(options)
        if error:
            print("Sorry I didn't understand. Please enter either 1, 2, or 3")
            error = False
        else:
            print("")

        p_input = input()
        if p_input.isdigit() and 1 <= int(p_input) <= 3:
            return options[int(p_input) - 1].lower()
        else:
            error = True

def set_date():
    """
    Facilitates the user entering what date it is. Returns it as an int.
    """
    error = False
    while True:
        clear_screen()

        print("What date is it?")
        if error:
            print("Sorry I didn't understand. Please enter a number between "\
                "and 28.")
            error = False
        else:
            print("")

        # Prints out the options array in a numbered fashion
        p_input = input()
        if p_input.isdigit() and 1 <= int(p_input) <= 28:
            return int(p_input)
        else:
            error = True

def set_budget():
    """
    Facilitates the user entering the maximum amount of gold they're willing to
    use. Returns it as an int.
    """
    error = False
    while True:
        clear_screen()
        print("What's your budget?")

        if error:
            print("Sorry I didn't understand. Please enter a number greater "\
                "than 0.")
            error = False
        else:
            print("")

        p_input = input()
        if p_input.isdigit() and int(p_input) > 0:
            return int(p_input)
        else:
            error = True

def set_number_seeds():
    """
    Facilitates the user entering the maximum number of seeds they are willing
    and able to purchase. Returns it as an int.
    """
    error = False
    while True:
        clear_screen()

        print("How many seeds do you wish to buy?")
        if error:
            print("Sorry I didn't understand. Please enter a number greater "\
                "than 0.")
            error = False
        else:
            print("")

        p_input = input()
        if p_input.isdigit() and int(p_input) > 0:
            return int(p_input)
        else:
            error = True

def set_type_seeds(season, date):
    """
    Using the season and date, it faciliates the user making educated choices
    (due to having the net income/day visibly present) about what seeds they
    are willing and able to purchase. Returns a list containing the names of
    those seeds.
    """
    crop_incomes = []
    for crop in season_crops[season]:
        crop_incomes.append((per_day_income(crop, date), crop))
    crop_incomes = sorted(crop_incomes, reverse=True)

    # Iterates through each seed and its NGI/D and formats them in such a way
    # that the NGI/D is nicely aligned vertically.
    formatted_crop_incomes = []
    for i in range(len(crop_incomes)):
        formatted_crop_incomes.append("{}{}".format(crop_incomes[i][1] + \
            " " * (15 - len(crop_incomes[i][1])), crop_incomes[i][0]))

    desired_seeds = []
    error = False
    while len(formatted_crop_incomes) > 0:
        clear_screen()
        print("What seeds do you wish to buy? (Highest priority first) "\
            "(Write 'done' when you're finished choosing)")
        # Prints out the options array in a vertically, numbered fashion
        print_options(formatted_crop_incomes, 1, 'vert')
        if error:
            print("Sorry I didn't understand. Write the number corresponding "\
                "to what seeds you want.")
            error = False
        else:
            print("")
        print(desired_seeds)
        print("")

        p_input = input()
        if p_input == "done":
            break
        elif p_input.isdigit() and 1 <= int(p_input) <= len(crop_incomes):
            # Pops both crop_incomes and formatted_crop_incomes in order to
            # ensure they match up.
            desired_seeds.append(crop_incomes.pop(int(p_input) - 1)[1])
            formatted_crop_incomes.pop(int(p_input) - 1)
            i += 1
        else:
            error = True

    return desired_seeds

def per_day_income(crop_name, date):
    """
    Given the name of the crop and the current date, this will return the
    amount of gold that the crop can produce if harvested until the end of its
    life span.
    """
    # If-block triggered if the crop is a multi-harvestable crop
    # (e.g. strawberries)
    if crop_name in multiharvest_crops:
        # Number of days left after the crop has fully grown.
        post_growth_days = 28 - date - crops_growth_values[crop_name]\
                                                            ["grow_time"]
        # Possible number of harvests that can be done before the crop dies.
        most_n_harvests = 1 + post_growth_days // \
                                crops_growth_values[crop_name]["produce_time"]
        # Changes 'most_n_harvests' if it conflicts with the max number of
        # times that it can physically be harvested.
        if most_n_harvests > crops_growth_values[crop_name]\
                                                    ["harvests/crop"]:
            most_n_harvests = crops_growth_values[crop_name]["harvests/crop"]
        # Total number of days from when it's planted until it's last day of
        # possible harvest.
        total_days = crops_growth_values[crop_name]["grow_time"] + \
        (most_n_harvests - 1) * crops_growth_values[crop_name]\
                                                        ["produce_time"]
        income_per_day = (most_n_harvests * crops_store_values[crop_name]\
            ["sell"] - crops_store_values[crop_name]["buy"]) / total_days
        return income_per_day
    # Else-block is triggered if the crop is NOT a multi-harvestable crop
    # (e.g. potatoes)
    else:
        # Number of days left in the month after the crop has fully grown.
        post_growth_days = 28 - date
        # If the plant is repeatadly planted and harvested until the end of the
        # month, most_n_harvests is the maximum amount of times you'd be able 
        # to harvest.
        most_n_harvests = post_growth_days // crops_growth_values[crop_name]\
                                                                ["grow_time"]
        # Prevents dividing by zero a few lines down. Instead ends function and
        # returns the amount of gold that'd be lost per day until the end of
        # the month if the seed was purchased.
        if most_n_harvests == 0:
            return -1 * crops_store_values[crop_name]["buy"] / \
                                                            post_growth_days
        # Total days of growing, including time over multiple harvests.
        total_days = most_n_harvests * crops_growth_values[crop_name]\
                                                                ["grow_time"]
        # For simplicity, the sell price, yield, and cost of the crops are
        # extracted here.
        sell_price = crops_store_values[crop_name]["sell"]
        crop_yield = crops_growth_values[crop_name]["yield"]
        seed_cost = crops_store_values[crop_name]["buy"]
        income_per_day = (most_n_harvests * sell_price * crop_yield - \
                                    (most_n_harvests * seed_cost)) / total_days
        return income_per_day

def determine_purchase(budget, number_seeds, type_seeds):
    """
    Takes an input budget of gold to be used, the number of seeds to be bought,
    and the types of seeds to be bought. Prints how much of each seed that
    should be purchased.
    """
    clear_screen()

    # List containing all the prices of each type of crop in the type_seeds
    # list. Used later to find the cheapest seed in the list.
    seed_prices = []
    for seed in type_seeds:
        seed_prices.append(crops_store_values[seed]["buy"])

    # List containing how many of each seed type that should be purchased. By
    # matching indexes, those numbers can be associated with the seed types.
    seeds_to_purchase = []
    # Money will be subtracted as the number of seeds to buy of one type
    # is determined.
    gold = budget
    i = 0
    # While there's more gold than the cheapest seed is worth (i.e. can still
    # purchase more seeds.) and there's still more room for seeds, do the
    # following...
    while gold >= min(seed_prices) and number_seeds > 0:
        # The max number of this type of seed that can be bought with the
        # current gold remaining.
        max_seeds = gold // crops_store_values[type_seeds[i]]["buy"]
        # Number of seeds left to buy is reduced as seeds are bought.
        number_seeds -= max_seeds
        # Ensures that more seeds than specified are not being bought.
        if number_seeds < 0:
            max_seeds += number_seeds
        # Calculates remaining gold after purchase of above number of seeds.
        gold -= max_seeds * crops_store_values[type_seeds[i]]["buy"]
        seeds_to_purchase.append(max_seeds)
        # If the specified number of seeds to buy is met, stop buying more.
        if number_seeds == 0:
            break
        i += 1

    error = False
    while True:
        clear_screen()
        # Prints out a sentence for every seed specifying how many you should 
        # buy and of which type.
        for i in range(len(seeds_to_purchase)):
            print("You should purchase {} {} seeds.".format(\
                                    int(seeds_to_purchase[i]), type_seeds[i]))
        print("")
        print("What would you like to do now?")
        options = ["Return to main menu", "Exit"]
        print_options(options)
        if error:
            print("Sorry I don't understand. Please enter either 1 or 2.")
            error = False
        else:
            print("")
        p_input = input()
        if p_input == "1":
            main_menu()
            break
        elif p_input == "2": 
            print("Goodbye!")
            break
        else:
            error = True

# Starts the program. 
main_menu()
