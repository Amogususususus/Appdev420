class Appointment:
    def __init__(self, name_ment, age_ment, gender_ment, nric_ment, email_ment, address_ment, remarks_ment, past_condition_ment, doctor_ment, date_ment, time_ment, count):
        self.__count = count
        self.__count += 1
        self.__ment_id = self.__count
        self.__name_ment = name_ment
        self.__age_ment = age_ment
        self.__gender_ment = gender_ment
        self.__nric_ment = nric_ment
        self.__email_ment = email_ment
        self.__address_ment = address_ment
        self.__remarks_ment = remarks_ment
        self.__past_condition_ment = past_condition_ment
        self.__doctor_ment = doctor_ment
        self.__date_ment = date_ment
        self.__time_ment = time_ment

    def get_id(self):
        return self.__ment_id

    def get_name_ment(self):
        return self.__name_ment

    def get_age_ment(self):
        return self.__age_ment

    def get_gender_ment(self):
        return self.__gender_ment

    def get_nric_ment(self):
        return self.__nric_ment

    def get_email_ment(self):
        return self.__email_ment

    def get_address_ment(self):
        return self.__address_ment

    def get_remarks_ment(self):
        return self.__remarks_ment

    def get_past_condition_ment(self):
        return self.__past_condition_ment

    def get_doctor_ment(self):
        return self.__doctor_ment

    def get_date_ment(self):
        return self.__date_ment

    def get_time_ment(self):
        return self.__time_ment

    def set_count(self, count):
        self.__ment_id = count

    def set_name_ment(self, name_ment):
        self.__name_ment = name_ment

    def set_age_ment(self, age_ment):
        self.__age_ment = age_ment

    def set_gender_ment(self, gender_ment):
        self.__gender_ment = gender_ment

    def set_nric_ment(self, nric_ment):
        self.__nric_ment = nric_ment

    def set_email_ment(self, email_ment):
        self.__email_ment = email_ment

    def set_address_ment(self, address_ment):
        self.__address_ment = address_ment

    def set_remarks_ment(self, remarks_ment):
        self.__remarks_ment = remarks_ment

    def set_past_condition_ment(self, past_condition_ment):
        self.__past_condition_ment = past_condition_ment

    def set_doctor_ment(self, doctor_ment):
        self.__doctor_ment = doctor_ment

    def set_date_ment(self, date_ment):
        self.__date_ment = date_ment

    def set_time_ment(self, time_ment):
        self.__time_ment = time_ment
