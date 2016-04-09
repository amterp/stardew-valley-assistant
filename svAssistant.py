#---------------------------------------------------------------------------------------------------
# Written by:   Alexander Terp
# Date:         09/04/2016
# Description:  As assistant application that allows the user to input the date, budget, and desired
#               number and types of seeds in the video game Stardew Valley, and returns the optimal
#               types and amounts of seeds to purchase.
#---------------------------------------------------------------------------------------------------
from os import system

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

crops_store_values = {
# 'cost' is the price of buying a seed.
# 'sell' is the price at which each part of the yield can be sold at.
"Cauliflower": {"cost": 80, "sell": 175},
"Garlic": {"cost": 40, "sell": 60},
"Green Bean": {"cost": 60, "sell": 40},
"Kale": {"cost": 70, "sell": 110},
"Parsnip": {"cost": 20, "sell": 35},
"Potato": {"cost": 50, "sell": 80},
"Rhubarb": {"cost": 100, "sell": 220},
"Strawberry": {"cost": 100, "sell": 120},
"Blue Jazz": {"cost": 30, "sell": 50},
"Tulip": {"cost": 20, "sell": 30},
"Blueberry": {"cost": 80, "sell": 80},
"Corn": {"cost": 150, "sell": 50},
"Hops": {"cost": 60, "sell": 25},
"Hot Pepper": {"cost": 40, "sell": 40},
"Melon": {"cost": 80, "sell": 250},
"Radish": {"cost": 40, "sell": 90},
"Red Cabbage": {"cost": 100, "sell": 260},
"Starfruit": {"cost": 400, "sell": 800},
"Tomato": {"cost": 50, "sell": 60},
"Wheat": {"cost": 10, "sell": 25},
"Poppy": {"cost": 100, "sell": 140},
"Summer Spangle": {"cost": 50, "sell": 90},
"Amaranth": {"cost": 70, "sell": 150},
"Artichoke": {"cost": 30, "sell": 160},
"Beet": {"cost": 20, "sell": 100},
"Bok Choy": {"cost": 50, "sell": 80},
"Cranberries": {"cost": 240, "sell": 130},
"Eggplant": {"cost": 20, "sell": 60},
"Grape": {"cost": 60, "sell": 80},
"Pumpkin": {"cost": 100, "sell": 320},
"Yam": {"cost": 60, "sell": 160},
"Fairy Rose": {"cost": 200, "sell": 290},
"Sunflower": {"cost": 50, "sell": 80},
}

# A list containing all the names of multi-harvestable crops.
multiharvest_crops = ["Green Bean", "Strawberry", "Blueberry", "Corn", \
"Hops", "Hot Pepper", "Tomato", "Cranberries", "Eggplant", "Grape"]

crops_growth_values = {
# 'grow_time' is the number of days it takes for the crop to completely grow.
# 'produce_time' is the number of days it takes to reproduce yield post-growth.
# 'harvests/crop' is the number of times the crop can be harvested per season.
# '999' for 'harvests/crop' means infinite.
# 'yield' is the number of crops you recieve per harvest.
"Cauliflower": {"grow_time": 12, "harvests/crop": 1, "yield": 1},
"Garlic": {"grow_time": 4, "harvests/crop": 1, "yield": 1},
"Green Bean": {"grow_time": 10, "produce_time": 3, "harvests/crop": 999, "yield": 1},
"Kale": {"grow_time": 6, "harvests/crop": 1, "yield": 1},
"Parsnip": {"grow_time": 4, "harvests/crop": 1, "yield": 1},
"Potato": {"grow_time": 6, "harvests/crop": 1, "yield": 1.25},
"Rhubarb": {"grow_time": 13, "harvests/crop": 1, "yield": 1},
"Strawberry": {"grow_time": 8, "produce_time": 4, "harvests/crop": 999, "yield": 1},
"Blue Jazz": {"grow_time": 7, "harvests/crop": 1, "yield": 1},
"Tulip": {"grow_time": 6, "harvests/crop": 1, "yield": 1},
"Blueberry": {"grow_time": 13, "produce_time": 4, "harvests/crop": 999, "yield": 3},
"Corn": {"grow_time": 14, "produce_time": 4, "harvests/crop": 999, "yield": 1},
"Hops": {"grow_time": 11, "produce_time": 1, "harvests/crop": 999, "yield": 1},
"Hot Pepper": {"grow_time": 5, "produce_time": 3, "harvests/crop": 999, "yield": 1},
"Melon": {"grow_time": 12, "harvests/crop": 1, "yield": 1},
"Radish": {"grow_time": 6, "harvests/crop": 1, "yield": 1},
"Red Cabbage": {"grow_time": 9, "harvests/crop": 1, "yield": 1},
"Starfruit": {"grow_time": 13, "harvests/crop": 1, "yield": 1},
"Tomato": {"grow_time": 11, "produce_time": 4, "harvests/crop": 5, "yield": 1},
"Wheat": {"grow_time": 4, "harvests/crop": 1, "yield": 1},
"Poppy": {"grow_time": 7, "harvests/crop": 1, "yield": 1},
"Summer Spangle": {"grow_time": 8, "harvests/crop": 1, "yield": 1},
"Amaranth": {"grow_time": 7, "harvests/crop": 3, "yield": 1},
"Artichoke": {"grow_time": 8, "harvests/crop": 1, "yield": 1},
"Beet": {"grow_time": 6, "harvests/crop": 1, "yield": 1},
"Bok Choy": {"grow_time": 4, "harvests/crop": 1, "yield": 1},
"Cranberries": {"grow_time": 7, "produce_time": 5, "harvests/crop": 5, "yield": 2},
"Eggplant": {"grow_time": 5, "produce_time": 5, "harvests/crop": 999, "yield": 1},
"Grape": {"grow_time": 10, "produce_time": 3, "harvests/crop": 999, "yield": 1},
"Pumpkin": {"grow_time": 13, "harvests/crop": 1, "yield": 1},
"Yam": {"grow_time": 10, "harvests/crop": 1, "yield": 1},
"Fairy Rose": {"grow_time": 12, "harvests/crop": 1, "yield": 1},
"Sunflower": {"grow_time": 8, "harvests/crop": 1, "yield": 1}
}

def main_menu():
    """
    Defines a function that brings up the main menu and its choices.
    """
    while True:
        system('cls')   # Clears the window
        options = ["Assist purchase", "Exit"]
        print("What can I do for you?")
        # Prints out the options array in a numbered fashion
        print_options(options, 1)
        p_input = int(input())
        if p_input == 1:
            season = set_season()
            date = set_date()
            budget = set_budget()
            number_seeds = set_number_seeds()
            type_seeds = set_type_seeds(season, date)
            determine_purchase(budget, number_seeds, type_seeds)
            break
        elif p_input == 2:
            print("Goodbye!")
            break
        else:
            "Sorry I didn't understand. Write the number corresponding to " \
            "what you wish to do."

def print_options(array, nummed, direction="horiz"):
    """
    Defines a function that takes in options in an array and prints them out
    # numbered if nummed = 1 or plainly if nummed = 2. dir determines if they're 
    printed out horizontally or vertically.
    """
    to_print = []
    if (nummed):
        for option in range(0 ,len(array)):
            # if-else statement that prevents options from becoming vertically disaligned due to option numbering 
            # reaching 2 digits in length.
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
    while True:
        system('cls')   # Clears the window
        options = ["Spring", "Summer", "Fall"]
        print("What season is it?")
        # Prints out the options array in a numbered fashion
        print_options(options, 1)
        p_input = input()
        if p_input.isdigit() and 1 <= int(p_input) <= 3:
            return options[int(p_input) - 1].lower()
        else:
            "Sorry I didn't understand. Write the number corresponding to " \
            "what season it is."

def set_date():
    while True:
        system('cls')    # Clears the window
        print("What date is it?")
        # Prints out the options array in a numbered fashion
        p_input = input()
        if p_input.isdigit() and 1 <= int(p_input) <= 28:
            return int(p_input)
        else:
            print("Sorry I didn't understand. Please enter a number.")

def set_budget():
    while True:
        system('cls') # Clears the window
        print("What's your budget?")
        p_input = input()
        if p_input.isdigit():
            return int(p_input)
        else:
            "Sorry I didn't understand. Please enter a number."

def set_number_seeds():
    while True:
        system('cls') # Clears the window
        print("How many seeds do you wish to buy?")
        p_input = input()
        if p_input.isdigit():
            return int(p_input)
        else:
            "Sorry I didn't understand. Please enter a number."

def set_type_seeds(season, date):
    crop_incomes = []
    for crop in season_crops[season]:
        crop_incomes.append((per_day_income(crop, date), crop))
    crop_incomes = sorted(crop_incomes, reverse=True)
    formatted_crop_incomes = []
    for i in range(len(crop_incomes)):
        formatted_crop_incomes.append("{}{}".format(crop_incomes[i][1] + " " * (12 - len(crop_incomes[i][1])), crop_incomes[i][0]))
    error = False
    desired_seeds = []
    i = 0
    while i < 2:
        system('cls')   # Clears the window
        print("What seeds do you wish to buy? (Highest priority first) (Write 'done' when you're finished choosing)")
        # Prints out the options array in a vertically, numbered fashion
        print_options(formatted_crop_incomes, 1, 'vert')
        if error:
            print("Sorry I didn't understand. Write the number corresponding to what season it is.")
            error = False
        else:
            print("")
        print(desired_seeds)
        print("")
        p_input = input()
        if p_input == "done":
            break
        elif p_input.isdigit() and 1 <= int(p_input) <= (len(crop_incomes) - 1):
            # Pops both crop_incomes and formatted_crop_incomes in order to ensure they match up.
            desired_seeds.append(crop_incomes.pop(int(p_input) - 1)[1])
            formatted_crop_incomes.pop(int(p_input) - 1)
            i += 1
        else:
            error = True
    return desired_seeds

def per_day_income(crop_name, date):
    """
    Given the name of the crop and the current date, this will return the amount
    of gold that the crop can produce if harvested until the end of its life
    span.
    """
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
        income_per_day = (most_n_harvests * crops_store_values[crop_name]["sell"] - crops_store_values[crop_name]["cost"]) / total_days
        return income_per_day
    else:
        post_growth_days = 28 - date
        most_n_harvests = post_growth_days // crops_growth_values[crop_name]["grow_time"]
        if most_n_harvests == 0:
            return 0
        total_days = most_n_harvests * crops_growth_values[crop_name]["grow_time"]
        sell_price = crops_store_values[crop_name]["sell"]
        crop_yield = crops_growth_values[crop_name]["yield"]
        seed_cost = crops_store_values[crop_name]["cost"]
        income_per_day = (most_n_harvests * sell_price * crop_yield - seed_cost) / total_days
        return income_per_day

def determine_purchase(budget, number_seeds, type_seeds):
    """
    Takes an input budget of gold to be used, the number of seeds to be bought, and the types of seeds to be bought.
    Prints how much of each seed that should be purchased.
    """
    system('cls')
    cost_seed_1 = crops_store_values[type_seeds[0]]["cost"]
    cost_seed_2 = crops_store_values[type_seeds[1]]["cost"]
    seeds_to_buy = cramer(cost_seed_1, cost_seed_2, 1, 1, budget, number_seeds)
    print("You should buy {} {} seeds.".format(int(seeds_to_buy[0]), type_seeds[0]))
    print("You should buy {} {} seeds.".format(int(seeds_to_buy[1]), type_seeds[1]))
    print("")

def cramer(a1, a2, b1, b2, c1, c2):
    """
    Solves a 2x2 system of equations in the form of
    a1x + a2y = c1
    b1x + b2y = c2
    """
    D = (a1 * b2) - (a2 * b1)
    Dx = (c1 * b2) - (a2 * c2)
    Dy = (a1 * c2) - (c1 * b1)
    x = Dx/D
    y = Dy/D
    return (x, y)

main_menu()