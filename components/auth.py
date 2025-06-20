def verification(username, password):
    filename = "data/users.txt"

    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    stored_username, stored_password, stored_role = line.strip().split(",")
                    if stored_username == username and stored_password == password:
                        return stored_role  # returns 'admin' or 'user'
                except ValueError:
                    continue
    except FileNotFoundError:
        return None

    return None  # If no match found


def main_verify():
    while True:
        try:
            choice = int(input("Are you an admin or a user?\n1) Admin\n2) User\n3) Exit\n "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            try:
                with open("data/admin.txt", "r") as file:
                    data = file.readlines()
            except FileNotFoundError:
                print("Admin data file not found.")
                continue
            role, userID = verification(data, "admin")
        elif choice == 2:
            try:
                with open("data/user.txt", "r") as file:
                    data = file.readlines()
            except FileNotFoundError:
                print("User data file not found.")
                continue
            role, userID = verification(data, "user")
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice")
            continue
