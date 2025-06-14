def updating_pin(file_path, userID, oldPin, newPin):
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    found = False
    new_lines = []

    for line in lines:
        parts = line.strip().split(',')
        if parts[0] == userID and parts[-1] == oldPin:
            parts[-1] = newPin
            found = True
        new_lines.append(','.join(parts) + '\n')

    with open(file_path, "w") as f:
        f.writelines(new_lines)

    return found
