class Person:
    def __init__(self, name, address,phone):
        self.name = name
        self.__address = address
        self.__phone =phone

    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self,new_address):
        self.__address = new_address


    @property
    def phone(self):
        return self.__phone
    @phone.setter
    def phone(self,new_phone):
        self.__phone = new_phone


    def __repr__(self):
        return f"Person(name={self.name}, address=***, phone=***)"


