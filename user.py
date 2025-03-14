import csv
import sqlite3

#open git bash
#git config --global user.name "Ankita Gharti Magar"
#git config --global user.email "ankitagmgr@gmail.com"

#git init ==> first time only==> to initialize the git repository 
#git add .
#git commit -m "Your commit message"

#after each code change
#git add .==> track the files 
#git commit -m "Your commit message"

#git status ==> to check the status of the files
#git diff ==> to check the changes in files
#copy paste from github from code 
#git hub 

INPUT_STRING="""
Enter the option:
    1.CREATE TABLE
    2.DUMP user from csv INTO users TABLE
    3.ADD new user INTO users TABLE
    4.QUERY all users form TABLE
    5.QUERY user by id from TABLE
    6.QUERY specified no. of records from TABLE
    7.DELETE all users
    8.DELETE users by id
    9.UPDATE user
    10.Press any key to EXIT
"""

def create_connection():
    try:
        con=sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print("Error:",e)

def create_table(con):
    CREATE_USER_TABLE_QUERY="""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255) NOT NULL,
            email CHAR(255) NOT NULL,
            web text
        );

    """
    cur=con.cursor()
    cur.execute(CREATE_USER_TABLE_QUERY)
    print("User table was created successfully.")



def read_csv():
    users=[]
    with open("sample.csv","r") as f:
        data=csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]

def insert_users(con,users):
    user_add_query="""
        INSERT INTO users
        (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)

    """
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)} users were imported successfully.")
 
def select_users(con):
    cur=con.cursor()
    users=cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def select_users_by_id(con,user_id):
    cur=con.cursor()
    users=cur.execute("SELECT * FROM users where id =?;",(user_id,))
    for user in users:
        print(user)

def select_specified_records(con,num_records):
    cur=con.cursor()
    users=cur.execute("SELECT * FROM users LIMIT ?;",(int(num_records),))
    for user in users:
        print(user)

def delete_users(con):
    cur=con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("All users were deleted successfully.")

def delete_user_by_id(con,user_id):
    cur=con.cursor()
    cur.execute("DELETE FROM users where id=?;",(user_id,))
    con.commit()
    print(f"User with id [{user_id}] were deleted successfully.")

COLUMNS=(

    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",

)

def get_current_user_data(con,user_id):
    cur=con.cursor()
    cur.execute("SELECT * FROM users WHERE id =?;",(user_id,))
    return cur.fetchone()

def updated_user(con,user_id,user_data):
    current_data=get_current_user_data(con,user_id)
    updated_data=[
        new_value if new_value is not None else current_value
        for new_value ,current_value in zip(user_data,current_data[1:])
    ]

    update_query="""
        UPDATE users
        SET first_name=?,
            last_name=?,
            company_name=?,
            address=?,
            city=?,
            county=?,
            state=?,
            zip=?,
            phone1=?,
            phone2=?,
            email=?,
            web=?
        WHERE id=?;
    """
    cur=con.cursor()
    cur.execute(update_query,(*updated_data,user_id))
    con.commit()
    print(f"User with id [{user_id}] was successfully updated.")


def main():
    con=create_connection()
    user_input=input(INPUT_STRING)
    if user_input=="1":
        create_table(con)

    elif user_input=="2":
        users=read_csv()
        insert_users(con,users)

    elif user_input=="3":
        user_data=[]
        for column in COLUMNS:
            column_value=input(f"Enter the value of {column}:")
            user_data.append(column_value)
        insert_users(con,[tuple(user_data)])

    elif user_input=="4":
        select_users(con)

    elif user_input=="5":
        user_id=input("Enter the user id:")
        select_users_by_id(con,user_id)

    elif user_input=="6":
        num_records=input("Enter number of record to display:")
        if num_records.isdigit():
            select_specified_records(con,num_records)

    elif user_input=="7":
        delete_users(con)

    elif user_input=="8":
        user_id=input("enter the user id you want to delete:")
        if user_id.isdigit():
            delete_user_by_id(con,user_id)

    elif user_input=="9":
        user_id=input("Enter the user id to update:")
        if user_id.isdigit():
            current_data=get_current_user_data(con,user_id)
            if not current_data:
                print(f"No user found with id [{user_id}].")
                return
            user_data=[]
            for column in COLUMNS:
                column_value=input(
                    f"Enter the new value for {column} (leave blank to keep current):"
                )
                user_data.append(column_value if column_value else None)
            updated_user(con,user_id,user_data)
        else:
            print("Invalid user id . Please enter a numeric value.")

    else:
        exit()


main()