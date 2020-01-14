# Function to print username and date of opening document
def print_introduction(first_name, last_name):
    
    from datetime import date
    today = date.today()
    print(f"Hello! My name is {first_name} {last_name}.")
    print(f"You are reading at my software project on {today}.")
    print("Enjoy!")
    
