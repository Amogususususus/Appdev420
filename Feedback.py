class Feedback:
    count_id = 0


    def __init__(self, date, name, email, typeqn, qn1, qn2):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__date = date
        self.__name = name
        self.__email = email
        self.__typeqn = typeqn
        self.__qn1 = qn1
        self.__qn2 = qn2


    def get_feedback_id(self):
        return self.__feedback_id

    def get_date(self):
        return self.__date

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_typeqn(self):
        return self.__typeqn

    def get_qn1(self):
        return self.__qn1

    def get_qn2(self):
        return self.__qn2


    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_date(self, date):
        self.__date = date

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_typeqn(self, typeqn):
        self.__typeqn = typeqn

    def set_qn1(self, qn1):
        self.__qn1 = qn1

    def set_qn2(self, qn2):
        self.__qn2 = qn2

