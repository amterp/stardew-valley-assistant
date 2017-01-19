# Author:           Alexander M. Terp
# Date created:     January, 2016
# Description:      Contains code responsible for the functions used in the
#                   calculations for SVA.

import csv

# Define global macro values.
SINGLE_HARVEST_CROPS_CSV_FILE = "csv_files/single_harvest_crops.csv"
REGENERATIVE_CROPS_CSV_FILE = "csv_files/regenerative_crops.csv"
CROP_SEASONS_CSV_FILE = "csv_files/crop_seasons.csv"

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

        self.seasons = []

class RegenerativeCrop(Crop):
    """
    Defines a class for a regenerative crop, such as a strawberry crop.
    - regrowth_time:        The number of days it takes for a mature crop to 
                            regrow and become harvestable again after being 
                            harvested.
    - harvests_per_crop:    The number of times a crop can be harvested in a
                            season.
    """
    def __init__(self, name, buy_price, sell_price, growth_time, 
        harvest_yield, regrowth_time, harvests_per_crop):
        Crop.__init__(self, name, buy_price, sell_price, growth_time, 
            harvest_yield)

        self.regrowth_time = regrowth_time
        self.harvests_per_crop = harvests_per_crop
        self.regenerative = True

        self.seasons = []

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
            info = [row["name"], row["buy_price"], row["sell_price"], 
                    row["growth_time"], row["harvest_yield"]]
            crop = Crop(*info)
            data.crops[row["name"]] = crop

    with open(REGENERATIVE_CROPS_CSV_FILE) as crop_values:
        crop_values = csv.DictReader(crop_values)
        for row in crop_values:
            info = [row["name"], row["buy_price"], row["sell_price"], 
                    row["growth_time"], row["harvest_yield"], 
                    row["regrowth_time"],row["max_harvests"]]
            crop = RegenerativeCrop(*info)
            data.crops[row["name"]] = crop

    with open(CROP_SEASONS_CSV_FILE) as crop_values:
        crop_values = csv.reader(crop_values)
        next(crop_values)   # Skip header
        for row in crop_values:
            data.crops[row[0]].seasons = [*[season for season in row[1:] if 
                                            season]]

def asd(season, date, budget, num_seeds_to_buy, data):
    available_crops = [crop.name for crop in list(data.crops.values()) 
                       if season in crop.seasons]
    return available_crops

import_crops(data)
print(data.crops["Corn"].seasons)
print(asd("fall", 6, 2, 1, data))