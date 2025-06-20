def verification(username, password, role):
    filename = "data/admin.txt" if role == "admin" else "data/user.txt"
    try:
        with open(filename, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    return True
    except FileNotFoundError:
        return False
    return False
