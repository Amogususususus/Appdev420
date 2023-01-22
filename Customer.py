import User

class Customer(User.User):
    count_id = 0

    def __init__(self, name, gender, membership, condition, email, age, address, password,nric):
        super().__init__(name, gender, membership, condition)
        Customer.count_id += 1
        self.__name = name
        self.__gender = gender
        self.__membership = membership
        self.__condition = condition
        self.__customer_id = Customer.count_id
        self.__email = email
        self.__age = age
        self.__address = address
        self.__password = password
        self.__nric = nric

    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_email(self):
        return self.__email

    def get_age(self):
        return self.__age

    def get_address(self):
        return self.__address

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_condition(self):
        return self.__condition

    def get_nric(self):
        return self.__nric

    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_age(self, age):
        self.__age = age

    def set_password(self,password):
        self.__password = password

    def set__name(self, name):
        self.__name = name

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_condition(self, condition):
        self.__condition= condition

    def set_nric(self,nric):
        self.__nric = nric
