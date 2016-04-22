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
"spring": ["Cauliflower", "Garlic", "Green Bean", "Kale", "Parsnip", 
"Potato", "Rhubarb", "Strawberry", "Blue Jazz", "Tulip"],

"summer": ["Blueberry", "Corn", "Hops", "Hot Pepper", "Melon", 
"Radish", "Red Cabbage", "Starfruit", "Tomato", "Wheat", "Poppy", 
"Summer Spangle"],

"fall": ["Amaranth", "Artichoke", "Beet", "Bok Choy", "Cranberries",
"Corn", "Eggplant", "Grape", "Pumpkin", "Yam", "Fairy Rose", "Sunflower"]
}

# A list containing all the names of multi-harvestable crops.
multiharvest_crops = ["Green Bean", "Strawberry", "Blueberry", "Corn", 
"Hops", "Hot Pepper", "Tomato", "Cranberries", "Eggplant", "Grape"]

# Creates a dictionary containing the buy and sell price of crops. Retrieves
# values from crops_store_values.csv
crops_store_values = {}
with open("crops_store_values.csv") as crop_values:
    for row in csv.DictReader(crop_values):
        if not row["crop_name"].startswith("#"):
            crops_store_values[row["crop_name"]] = {
                    "buy_price": float(row["buy_price"]), 
                    "sell_price": float(row["sell_price"])
                    }

# Creates a dictionary containing the grow_time, produce time (if applicable),
# harvests per crop, and yield of each crop. Retrieves the values from 
# crops_growth_values.csv
crops_growth_values = {}
with open("crops_growth_values.csv") as crop_growth:
    for row in csv.DictReader(crop_growth):
        # Ignore lines starting with # (to allow 
        # for commenting on the .csv file)
        if not row["crop_name"].startswith("#"):
            crops_growth_values[row["crop_name"]] = {
                    "grow_time": float(row["growth_time"]),
                    "produce_time": float(row["produce_time"]), 
                    "harvests_per_crop": float(row["harvests_per_crop"]),
                    "yield": float(row["yield"])
                    }

def clear_screen():
    """
    Clears the window
    """
    # More cross-platform http://stackoverflow.com/a/684344/780194
    os.system("cls" if os.name=="nt" else "clear")

def most_seeds_buy(budget, remaining_seeds, seed_name):
    max_to_buy = budget // crops_store_values[seed_name]['buy_price']
    if max_to_buy > remaining_seeds:
        max_to_buy = remaining_seeds
    budget -= max_to_buy * crops_store_values[seed_name]['buy_price']
    return (max_to_buy, budget)

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
            type_seeds   = set_type_seeds(season, date, budget, number_seeds)
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
        for option in range(len(array)):
            # if-else statement that prevents options from becoming vertically
            # disaligned due to option numbering reaching n digits in length.
            if direction == "vert":
                to_print.append("{0:{space}}. {1}".format(option + 1, 
                    array[option], space=len(str(len(array)))))
            else:
                to_print.append("{}. {}".format(option + 1, array[option]))
    else:
        for option in range(len(array)):
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
            print("Sorry I didn't understand. Please enter a number between 1 and 28.")
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
            print("Sorry I didn't understand. Please enter a number greater than 0.")
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
            print("Sorry I didn't understand. Please enter a number greater than 0.")
            error = False
        else:
            print("")

        p_input = input()
        if p_input.isdigit() and int(p_input) > 0:
            return int(p_input)
        else:
            error = True

def set_type_seeds(season, date, budget, number_seeds):
    """
    Using the given arguments,  it faciliates the user making educated
    choices (due to having the net income/day visibly present) about what seeds 
    they are willing and able to purchase. Returns a list containing the names 
    of those seeds.
    """

    def update_choices(init=0, crop_names=[]):
        crop_incomes = []
        if init:
            for crop in season_crops[season]:
                crop_incomes.append((per_day_income(crop, date, budget, number_seeds), crop))
            crop_incomes = sorted(crop_incomes, reverse=True)
        else:
            for crop in crop_names:
                crop_incomes.append((per_day_income(crop, date, budget, number_seeds), crop))
            crop_incomes = sorted(crop_incomes, reverse=True)
        # Iterates through each seed and its NGI/D and formats them in such a way
        # that the NGI/D is nicely aligned vertically.
        formatted_crop_incomes = []
        for i in range(len(crop_incomes)):
            formatted_crop_incomes.append("{}{}".format(crop_incomes[i][1] +
                " " * (15 - len(crop_incomes[i][1])), crop_incomes[i][0]))
        return (crop_incomes, formatted_crop_incomes)

    crop_incomes = update_choices(1)[0]
    formatted_crop_incomes = update_choices(1)[1]
    desired_seeds = []
    error = False
    i = 0
    while len(formatted_crop_incomes) > 0:
        clear_screen()
        crop_incomes = update_choices(0, [tupl[1] for tupl in crop_incomes])[0]
        formatted_crop_incomes = update_choices(0, [tupl[1] for tupl in crop_incomes])[1]
        print("What seeds do you wish to buy? (Highest priority first) "
            "(Write 'done' when you're finished choosing)")
        # Prints out the options array in a vertically, numbered fashion
        print_options(formatted_crop_incomes, 1, 'vert')
        if error:
            print("Sorry I didn't understand. Write the number corresponding "
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
            tupl_choice = crop_incomes.pop(int(p_input) - 1)
            formatted_crop_incomes.pop(int(p_input) - 1)
            number_seeds -= most_seeds_buy(budget, number_seeds, tupl_choice[1])[0]
            desired_seeds.append(tupl_choice[1])
            i += 1
        else:
            error = True

    return desired_seeds

def per_day_income(crop_name, date, budget, number_seeds):
    """
    Given the name of the crop and the current date, this will return the
    amount of gold that the crop can produce if harvested until the end of its
    life span.
    """
    # Grab references to crop info
    crop_growth = crops_growth_values[crop_name]
    crop_values = crops_store_values[crop_name]

    # If-block triggered if the crop is a multi-harvestable crop
    # (e.g. strawberries)
    if crop_name in multiharvest_crops:
        # Number of days left after the crop has fully grown.
        post_growth_days = 28 - date - crop_growth["grow_time"]
        # Possible number of harvests that can be done before the crop dies.
        # Starts with +1 because of the initial harvest when growth_time is done.
        most_n_harvests = 1 + post_growth_days // crop_growth["produce_time"]
        # Changes 'most_n_harvests' if it conflicts with the max number of
        # times that it can physically be harvested. If it has a negative value,
        # change it to the more sensible value of 0.
        if most_n_harvests > crop_growth["harvests_per_crop"]:
            most_n_harvests = crop_growth["harvests_per_crop"]
        elif most_n_harvests < 0:
            most_n_harvests = 0
        # Total number of days from when it's planted until it's last day of
        # possible harvest.
        if most_n_harvests == 0:
            total_days = crop_growth["grow_time"]
        else:
            total_days = crop_growth["grow_time"] + (most_n_harvests - 1) * crop_growth["produce_time"]
        # To prevent ZeroDivisionErrors as well as false income_per_day values,
        # if total_days is 0 or less, just set income_per_day to 0.
        income_per_day = (most_n_harvests * crop_values["sell_price"] - 
                crop_values["buy_price"]) / total_days
        return income_per_day
    # Else-block is triggered if the crop is NOT a multi-harvestable crop
    # (e.g. potatoes)
    else:
        # For simplicity, the sell price, yield, and cost of the crops are
        # extracted here.
        sell_price = crop_values["sell_price"]
        crop_yield = crop_growth["yield"]
        seed_cost = crop_values["buy_price"]
        # Checks to see if there's enough time for the crop to grow and pay off.
        # If not, a negative value is stored in income_per_day.
        if crop_growth["grow_time"] < 28 - date:
            income_per_day = ((sell_price * crop_yield - seed_cost) / 
                crop_growth["grow_time"])
        else:
            income_per_day = seed_cost / crop_growth["grow_time"]

    max_seeds_buy = most_seeds_buy(budget, number_seeds, crop_name)[0]
    total_NGI_D = income_per_day * max_seeds_buy
    return total_NGI_D

def determine_purchase(budget, number_seeds, type_seeds):
    """
    Takes an input budget of gold to be used, the number of seeds to be bought,
    and the types of seeds to be bought. Prints how much of each seed that
    should be purchased.
    """
    # List containing all the prices of each type of crop in the type_seeds
    # list. Used later to find the cheapest seed in the list.
    seed_prices = []
    print(type_seeds)
    for seed in type_seeds:
        seed_prices.append(crops_store_values[seed]["buy_price"])
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
        seeds_to_purchase.append(most_seeds_buy(gold, number_seeds, type_seeds[i])[0])
        gold = most_seeds_buy(gold, number_seeds, type_seeds[i])[1]
        number_seeds -= seeds_to_purchase[-1]
        # If the specified number of seeds to buy is met, stop buying more.
        if number_seeds == 0:
            break
        i += 1

    error = False
    while True:
        clear_screen()
        # Prints out a sentence for every seed specifying how many you should 
        # buy and of which type. Skips any sentence that says to buy 0 seeds.
        for i in range(len(seeds_to_purchase)):
            if seeds_to_purchase[i] == 0:
                continue
            print("You should purchase {} {} seeds.".format(
                int(seeds_to_purchase[i]), type_seeds[i]))
        # If the sum of seeds_to_purchase equals, it must mean that the user
        # has not been told to buy any seeds in the for loop above. Thus, 
        # a sentence telling them not to buy any seeds is printed.
        if sum(seeds_to_purchase) == 0:
            print("You should not buy any seeds.")
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
