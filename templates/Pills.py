from Medications import *

class Pills(Medications):
    def __init__(self, name_Medication, price_Medication, stock):
        super().__init__(name_Medication, price_Medication, stock)
        self.__Grams=0
        self.__Description=None

    def set_Grams(self,Grams):
        self.__Grams=Grams

    def set_Description(self,Description):
        self.__Description=Description

    def get_Grams(self):
        return self.__Grams

    def get_Description(self):
        return self.__Description
