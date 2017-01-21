PRINT_S = 0
PRINT_R = 0

class Scenario():
    def __init__(self, name, buy_price, sell_price, growth_time, gold_amount, num_days, num_spots, regrowth_time=-1):
        
        self.name = name
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.growth_time = growth_time
        self.gold_amount = gold_amount
        self.num_days = num_days
        self.num_spots = num_spots
        self.regrowth_time = regrowth_time

scenarios_s = []
#scenarios_s.append(Scenario(1, 20, 40, 4, 120, 24, 36))
#scenarios_s.append(Scenario(2, 120, 240, 4, 120, 24, 36))
#scenarios_s.append(Scenario(3, 60, 80, 2, 120, 24, 36))
#scenarios_s.append(Scenario(4, 50, 75, 2, 120, 24, 36))

scenarios_s.append(Scenario("Pumpkin", 80, 250, 13, 200, 46, 46))
scenarios_s.append(Scenario("Wheat", 10, 25, 4, 200, 46, 46))
scenarios_s.append(Scenario("Parsnip", 20, 35, 4, 200, 46, 46))

scenarios_r = []
scenarios_r.append(Scenario("Strawberry", 100, 120, 8, 200, 46, 46, 4))
scenarios_r.append(Scenario("Green Bean", 60, 40, 10, 200, 46, 46, 3))
scenarios_r.append(Scenario("Blueberry", 80, 150, 13, 200, 46, 46, 4))

def gold_amount_s(scenarios):

    for sc in scenarios:
        num_cycles = sc.num_days // sc.growth_time
        gold = sc.gold_amount

        for i in range(num_cycles):
            buy_amount = gold // sc.buy_price

            if (buy_amount > sc.num_spots):
                buy_amount = sc.num_spots

            gold -= buy_amount * sc.buy_price
            if PRINT_S: print(sc.name, "- buy_amount:", buy_amount, "- gold_left:", gold)
            gold += buy_amount * sc.sell_price
            if PRINT_S: print(sc.name, "- gold_after_sell:", gold)

        print(sc.name, "-", gold)

def gold_amount_r(scenarios):

    for sc in scenarios:
        planner = [0] * sc.num_days
        gold = sc.gold_amount

        for i in range(sc.num_days):
            if PRINT_R: print(sc.name, "day:", i+1, "gold gain:", planner[i] * sc.sell_price)
            gold += planner[i] * sc.sell_price

            if i <= (sc.num_days - sc.growth_time):
                buy_amount = gold // sc.buy_price
                if PRINT_R and buy_amount: print(sc.name, "buy_amount:", buy_amount, "gold before:", gold)
                gold -= buy_amount * sc.buy_price
                if PRINT_R and buy_amount: print(sc.name, "gold after:", gold)

            for j in range(i + sc.growth_time-1, sc.num_days, sc.regrowth_time):
                planner[j] += buy_amount

        print(sc.name, "-", gold)


gold_amount_s(scenarios_s)
gold_amount_r(scenarios_r)