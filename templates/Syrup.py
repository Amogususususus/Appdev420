
class Syrup:
    def __init__(self, name_Medication, price_Medication, stock, Volume, Description, Picture, count):
        self.__count = count
        self.__count += 1
        self.__syrup_id = self.__count
        self.__Volume = Volume
        self.__Description = Description
        self.__name_Medication = name_Medication
        self.__price_Medication = price_Medication
        self.__stock = stock
        self.__Picture = Picture

    def set_count(self, count):
        self.__syrup_id=count

    def get_id(self):
        return self.__syrup_id

    def set_Volume(self,Volume):
        self.__Volume=Volume

    def set_Description(self,Description):
        self.__Description=Description

    def get_Volume(self):
        return self.__Volume

    def get_Description(self):
        return self.__Description

    def set_name(self, name_Medication):
        self.__name_Medication=str(name_Medication)

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

    def set_Picture(self, Picture):
        self.__Picture=Picture

    def get_Picture(self):
        return self.__Picture
