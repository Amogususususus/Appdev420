class Medications():
    def __init__(self, name_Medication, price_Medication, stock):
        self.__name_Medication = name_Medication
        self.__price_Medication = price_Medication
        self.__stock = stock

    def set_name(self, name_Medication):
        self.__name_Medication=name_Medication

    def set_price(self, price_Medication):
        self.__price_Medication=price_Medication

    def set_stock(self, stock):
        self.__stock=int(stock)

    def get_name(self):
        return self.__name_Medication

    def get_price(self):
        return self.__price_Medication

    def get_stock(self):
        return self.__stock

