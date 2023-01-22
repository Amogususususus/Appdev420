# User class
class User:
    count_id = 0

    # initializer method
    def __init__(self, name, gender, membership, condition):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__name = name
        self.__gender = gender
        self.__membership = membership
        self.__condition = condition

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name



    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_condition(self):
        return self.__condition

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name



    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_remarks(self, condition):
        self.__condition = condition
