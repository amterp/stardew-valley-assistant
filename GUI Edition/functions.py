# Author:           Alexander M. Terp
# Date created:     January, 2016
# Description:      Contains code responsible for the functions used in the
#                   calculations for SVA.

import csv

# Define global macro values.
SINGLE_HARVEST_CROPS_CSV_FILE = "csv_files/single_harvest_crops.csv"
REGENERATIVE_CROPS_CSV_FILE = "csv_files/regenerative_crops.csv"

DAYS_IN_SEASON = 28

class Crop():
    """
    Defines a class for a general crop. Contains properties shared by all
    crops, whether they are a one-time harvest or multiple-time harvest However,
    contains all properties of a single-harvest crop.
    
    - name:             Name for the crop as referred to in-game.
    - buy_price:        The cheapest cost of an individual seed.
    - sell_price:       The regular sales price of one unit of produce.
    - growth_time:        The number of days it takes for the crop to 
                        become harvestable.
    - harvest_yield:    The average amount of produce per harvest.
    """
    def __init__(self, name, buy_price, sell_price, growth_time, harvest_yield):
        
        self.name = name
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.growth_time = growth_time
        self.sell_price = sell_price
        self.harvest_yield = harvest_yield

        # Regenerative crops are defined using the RegenerativeCrop class, 
        # which will set this property as True instead.
        self.regenerative = False

        # Initialize net gold income per day (ngid) property. Will be changed
        # with future functions.
        self.ngid = None

class RegenerativeCrop(Crop):
    """
    Defines a class for a regenerative crop, such as a strawberry crop.
    - regrowth_time:        The number of days it takes for a mature crop to 
                            regrow and become harvestable again after being 
                            harvested.
    - max_harvests:    The number of times a crop can be harvested in a
                            season.
    """
    def __init__(self, name, buy_price, sell_price, growth_time, 
        harvest_yield, regrowth_time, max_harvests):
        Crop.__init__(self, name, buy_price, sell_price, growth_time, 
            harvest_yield)

        self.regrowth_time = regrowth_time
        self.max_harvests = max_harvests
        self.regenerative = True

class data:
    """ Define an object to hold widely used information. Will allow for easy
    argument-passing for functions. """
    crops = {}

def import_crops(data):
    """ Reads in data from csv files and populates the data object with crop
    objects. """
    with open(SINGLE_HARVEST_CROPS_CSV_FILE) as crop_values:
        crop_values = csv.DictReader(crop_values)
        for row in crop_values:
            info = [row["name"], int(row["buy_price"]), int(row["sell_price"]), 
                    int(row["growth_time"]), float(row["harvest_yield"])]
            crop = Crop(*info)
            crop.seasons = ([row["season1"], row["season2"]] if 
                            row["season2"] else [row["season1"]])

            data.crops[row["name"]] = crop

    with open(REGENERATIVE_CROPS_CSV_FILE) as crop_values:
        crop_values = csv.DictReader(crop_values)
        for row in crop_values:
            info = [row["name"], int(row["buy_price"]), int(row["sell_price"]),
                    int(row["growth_time"]), float(row["harvest_yield"]),
                    int(row["regrowth_time"]), int(row["max_harvests"])]
            crop = RegenerativeCrop(*info)
            crop.seasons = ([row["season1"], row["season2"]] if 
                            row["season2"] else [row["season1"]])

            data.crops[row["name"]] = crop

def get_final_gold(season, date, budget, max_num_seeds, data, recursive=0):
    """ Given inputs taken from the GUI, returns all possible crops that can be
    bought and also calculates the amount of gold that the player would have at
    the end of the season if only that crop were harvested and returns that
    number too. """
    
    if not recursive:
        num_days = DAYS_IN_SEASON - date
        available_crops = [crop for crop in list(data.crops.values()) if 
                           season in crop.seasons and budget > crop.buy_price]
    else:
        num_days = DAYS_IN_SEASON * 2 - date
        available_crops = [crop for crop in list(data.crops.values()) if 
                           len(crop.seasons) == 2 and budget > crop.buy_price]

    possible_paths = []
    for crop in available_crops:
    #for crop in [data.crops["Eggplant"]]:

        if not crop.regenerative:
            # Crop is single-harvest.
            num_cycles = num_days // crop.growth_time
            gold = budget

            for i in range(num_cycles):
                buy_amount = gold // crop.buy_price

                if (buy_amount > max_num_seeds):
                    buy_amount = max_num_seeds

                gold -= buy_amount * crop.buy_price
                gold += buy_amount * crop.sell_price * crop.harvest_yield

            possible_paths.append( [crop.name, gold] )

        elif crop.regenerative:
            # Crop is regenerative.
            final_golds = []
            planner = [0] * num_days
            gold = budget

            for i in range(num_days):
                gold += planner[i] * crop.sell_price * crop.harvest_yield

                if i <= (num_days - crop.growth_time):
                    buy_amount = gold // crop.buy_price

                    if (buy_amount > max_num_seeds):
                        buy_amount = max_num_seeds

                    gold -= buy_amount * crop.buy_price

                num_harvests = 0
                for j in range(i + crop.growth_time-1, num_days, 
                               crop.regrowth_time):
                    planner[j] += buy_amount

                    num_harvests += 1
                    if (crop.max_harvests != -1 and num_harvests >= 
                        crop.max_harvests):
                        break

            possible_paths.append( [crop.name, gold] )

    if season == "summer" and not recursive:
        long_possible_paths = get_final_gold("summer", date, budget,
                                             max_num_seeds, data, 1)

        print('short', possible_paths)
        print('long', long_possible_paths)
        for path in long_possible_paths:
            path_names = [short_path[0] for short_path in possible_paths]
            index = path_names.index(path[0])

            possible_paths[index].append(path[1])


    return possible_paths
    

import_crops(data)
print(get_final_gold("summer", 6, 200, 36, data))