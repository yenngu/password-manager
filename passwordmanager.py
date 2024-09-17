from cryptography.fernet import Fernet

# This function is used to generate an encryption key once.
'''
def encryption():
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as keyFile:
        keyFile.write(key)
'''

# Loads encryption key from file
def get_encryption():
    file = open("encryption.key", "rb")
    encryption_key = file.read()
    file.close()
    return encryption_key

# Create a admin password
print("Welcome to the Password Manager")
adminVerify = input("Create a admin password. ")

# Grabs encryption key and admin password and encodes to bytes
# fernet is an object that has the combined encryption key and admin key
key = get_encryption() + adminVerify.encode()
fernet = Fernet(key) 

# Select option for view/add/delete files
userSelection = input("Would you like to add or view your accounts? (view/add/delete): ").lower()

# Function to view accounts in accountmanager.txt
def viewAccounts():
    with open('accountmanager.txt', 'r') as file:
        for line in file.readlines():
            database = line.rstrip()
            userdata, passdata = database.split("|")
            # Prints user and password in decrypted format
            print("User: ", userdata, ", Password: ", 
                  fernet.decrypt(passdata.encode()).decode())

# Function to add accounts and passwords in accountmanager.txt            
def addAccounts(): 
    accountInput = input("Enter Account Name: ")
    passwordInput = input("Enter Password: ")
    
    # Write accounts and passwords
    with open('accountmanager.txt', 'a') as file:
        file.write(accountInput + '|' + fernet.encrypt(passwordInput.encode()).decode() + "\n")

# Function to delete accounts if have access to admin password
def deleteAccount():
   
    admin_access = input("Enter admin password: ")
    if admin_access != adminVerify:
        print("Access Denied.")
        return

  
    account_to_delete = input("Enter the name of the account to delete: ")

    # read lines
    with open('accountmanager.txt', 'r') as file:
        lines = file.readlines()

    
    # Split '|' to read data per line
    account_found = False
    with open('accountmanager.txt', 'w') as file:
        for line in lines:
            account_name, encrypted_pass = line.strip().split("|")
            if account_name != account_to_delete:
                file.write(line)
            else:
                account_found = True

    
    if account_found:
        print(f"Account '{account_to_delete}' has been deleted.")
    else:
        print(f"Account '{account_to_delete}' not found.")

# If statements to add/view/delete/and exit
while True:
    if userSelection == 'add':
        addAccounts()
        
    elif userSelection == 'view':
        viewAccounts()

    elif userSelection == 'delete':
        deleteAccount()
    
    elif userSelection == '.':
        break
    
    # Prompts user question to repeat cycle or exit
    userSelection = input("Would you like to add or view your accounts?(view/add/delete) , press . to exit: ").lower()    



