from Person.person import Person
class Admin(Person):
    def __init__(self, name, address, phone, pin):
        super().__init__(name, address, phone)
        self.pin = pin
        
    def Create_new_admin(self):
        if self.name == "":
            print("❌ Name cannot be empty.")
            return
            
        with open("data/users.txt", "a") as file:
            file.write(f"{self.name},{self.pin},{"admin"}\n")
        print(f"Admin {self.name} created successfully.")

    
