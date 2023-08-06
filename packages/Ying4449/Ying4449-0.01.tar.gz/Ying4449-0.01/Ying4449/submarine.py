class Submarine:
    """
        ----------------
        Test document
        This Program เรือดำน้ำ

    """

    def __init__(self, price, budget):
        self.captain = 'Sinyapong'
        self.sub_name = 'Sukito'
        self.price = price
        self.kilo = 0
        self.budget = budget
        self.totalcost = 0

    def Missile(self):
        print('We are Department of Missile')

    def Calcommission(self):
        ''' ใช้สำหรับคำนวณค่าคอมมิสชั่น'''
        pc = 10
        percent = self.price * (pc/100)
        print('Loong You Got : {:,.2f} Million Baht'.format(percent))

    def Goto(self, enemypoint, distance):
        print(f"Let's go to  {enemypoint} : {distance} KM. ")
        self.kilo += distance
        self.Fuel()

    def Fuel(self):
        deisel = 20
        Cal_fuel_cost = self.kilo * deisel
        print('Current Fuel Cost: {:,d} Baht'.format(Cal_fuel_cost))
        self.totalcost += Cal_fuel_cost

    @property
    def BudgetRemaining(self):
        remaining = self.budget - self.totalcost
        print('Budget Remaining: {:,.2f} Baht'.format(remaining))
        return remaining

class ElectricSubmarine(Submarine):
    def __init__(self, price, budget):
        self.sub_name = 'PuPea'
        self.Battery_distance = 100000
        super().__init__(price,budget)

    def Battery(self):
        allbattery = 100
        print('Kilo = ',self.kilo)
        calculate = (self.kilo /  self.Battery_distance) * 100
        print('Cal: ',calculate)
        print('We have Battery Remaining: {}%'.format(allbattery - calculate))

    def Fuel(self):
        kilowat = 5
        Cal_fuel_cost = self.kilo * kilowat
        print('Current Power Cost: {:,d} Baht'.format(Cal_fuel_cost))
        self.totalcost += Cal_fuel_cost

if __name__ == "__main__":
    tesla = ElectricSubmarine(40000, 2000000)
    print(tesla.captain)
    print(tesla.budget)
    tesla.Goto('Japan', 10000)
    tesla.BudgetRemaining
    print(tesla.BudgetRemaining)
    tesla.Battery()
    print('---------------------------------')

    kongtabbok = Submarine(40000, 2000000)
    print(tesla.captain)
    print(tesla.budget)
    kongtabbok.Goto('Japan', 10000)
    print(kongtabbok.BudgetRemaining)



'''
kongtabreuw = Submarine(10000)
print(kongtabreuw.captain)
print(kongtabreuw.sub_name)
kongtabreuw.Goto('Chainat', 500)
print(kongtabreuw.kilo)
kongtabreuw.Fuel()
current_budget = kongtabreuw.BudgetRemaining
print(current_budget * 0.2)
print('-------------------------------')

kongtabreuw.Calcommission()

print('--------------2----------------')
kongtabbok = Submarine(70000)
kongtabbok.captain = 'Pupea'

print(kongtabbok.captain)
kongtabbok.Calcommission()
kongtabbok.Goto('Chanthaburi', 1000)
kongtabbok.Fuel()
'''