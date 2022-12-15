from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import resources
import random

# -----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------------------------------------------------------------
DB_NAME = 'EmployeeDB.db'

CURRENT_TABLE = ""  # the table which the program is currently connected to

CURRENT_QUERY = ""  # the last executed SQL query

CONSOLE = ""  # stores the text which was last entered into the input field

AWAITING_INPUT = False  # track whether a process is awaiting user input

STATE = 0  # for database navigation: 0 = init; 1 = connect; 2 = create; 3 = delete

COL_NAMES = [
    ["rowid", "Employee ID"],
    ["title", "Title"],
    ["firstname", "First Name"],
    ["surname", "Surname"],
    ["email", "Email"],
    ["salary", "Salary (£)"]
]

# toggles to determine whether to sort columns descending or ascending
SORT_TOGGLES = [True, False, False, False, False, False]

# to store the text from entry boxes, in case they need to be recovered
ENTRY_BOXES = []


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def clear_entryboxes():
    """ Removes any values currently present in the record entry boxes. """
    ID_entry.delete(0, END)
    title_entry.delete(0, END)
    firstname_entry.delete(0, END)
    surname_entry.delete(0, END)
    email_entry.delete(0, END)
    salary_entry.delete(0, END)


def record_entry_state(state):
    """ Toggles record entry boxes between enabled and disabled. """
    ID_entry.config(state=state)
    title_entry.config(state=state),
    firstname_entry.config(state=state),
    surname_entry.config(state=state),
    email_entry.config(state=state),
    salary_entry.config(state=state)


def save_entry_boxes():
    """ Saves the current contents of the record entry boxes to a global variable. """
    global ENTRY_BOXES
    ENTRY_BOXES = [
        ID_entry.get(),
        title_entry.get(),
        firstname_entry.get(),
        surname_entry.get(),
        email_entry.get(),
        salary_entry.get()]


def restore_entry_boxes():
    """ Restores the contents of the record entry boxes from a previous save. """
    global ENTRY_BOXES
    clear_entryboxes()
    ID_entry.insert(0, ENTRY_BOXES[0])
    title_entry.insert(0, ENTRY_BOXES[1])
    firstname_entry.insert(0, ENTRY_BOXES[2])
    surname_entry.insert(0, ENTRY_BOXES[3])
    email_entry.insert(0, ENTRY_BOXES[4])
    salary_entry.insert(0, ENTRY_BOXES[5])


# -----------------------------------------------------------------------------------------------
def print_to_log(text, append=False):
    """ Allows for instructions and status information to be displayed to the user. """
    output_log.config(state=NORMAL)
    if not append:
        output_log.delete('1.0', END)
    output_log.insert(END, text)
    output_log.config(state=DISABLED)


# -----------------------------------------------------------------------------------------------
def get_list_of_tables():
    """ Returns a string which lists each table in the database, on separate lines. """
    query = ("SELECT name FROM sqlite_schema WHERE type ='table' "
             "AND name NOT LIKE 'sqlite_%';")
    records = sql_query(query, return_records=True)
    log_string = ""
    for record in records:
        for index in record:
            log_string += "    -    " + index + "\n"
    return log_string


# -----------------------------------------------------------------------------------------------
def sql_query(query, return_records=False):
    """
    Runs a SQL query, with the option to return the results to the calling code as a list.
    """
    connection = sq.connect(DB_NAME)  # create/connect to db
    cursor = connection.cursor()  # create a cursor object
    cursor.execute(query)
    records = cursor.fetchall()
    connection.commit()  # commit to database
    connection.close()  # close connection to database
    if return_records:
        return records


# -----------------------------------------------------------------------------------------------
def query_and_update_tree(query):
    """
    Runs a SQL query and populates the tree view based on the results.
    Records should be cleared from the tree view before this function is called.
    """
    records = sql_query(query, return_records=True)
    # insert table data to the tree
    count = 0
    for record in records:
        if count % 2 == 0:
            db_treeview.insert(parent='',
                               index='end',
                               iid=record[0],
                               text='',
                               values=(record[0], record[1], record[2], record[3],
                                       record[4], record[5]),
                               tags=('evenrow',))
        else:
            db_treeview.insert(parent='',
                               index='end',
                               iid=record[0],
                               text='',
                               values=(record[0], record[1], record[2], record[3],
                                       record[4], record[5]),
                               tags=('oddrow',))
        count += 1


# -----------------------------------------------------------------------------------------------
def filter_records():
    """
    Filters records based on whatever values are currently in the attribute entry boxes.
    Supports some more advanced features, including comparison operators and wildcards.
    Please see the help messages for more information.
    """
    global CURRENT_TABLE, CURRENT_QUERY

    def convert_to_query(col_name, filter_criteria):
        parsed_filter_criteria = ""
        wildcards = ["%", "_"]
        comparison_ops = ["<", ">", "!", "="]
        if filter_criteria == "":
            return ""
        if not filter_criteria.isnumeric():
            if "'" not in filter_criteria:
                temp = ""
                for character in filter_criteria:
                    if character not in comparison_ops:
                        if temp[-1:] == "'":
                            temp = temp.rstrip(temp[-1])
                            temp += character + "'"
                        else:
                            temp += "'" + character + "'"
                    else:
                        temp += character
                filter_criteria = temp

        if any(wildcard in filter_criteria for wildcard in wildcards):
            parsed_filter_criteria += col_name + " LIKE " + filter_criteria + " AND "
        else:
            if any(comparison_op in filter_criteria for comparison_op in comparison_ops):
                parsed_filter_criteria += col_name + filter_criteria + " AND "
            else:
                parsed_filter_criteria += col_name + " = " + filter_criteria + " AND "
        return parsed_filter_criteria

    filter_string = "\nWHERE "
    filter_string += convert_to_query("rowid", ID_entry.get())
    filter_string += convert_to_query("title", title_entry.get())
    filter_string += convert_to_query("firstname", firstname_entry.get())
    filter_string += convert_to_query("surname", surname_entry.get())
    filter_string += convert_to_query("email", email_entry.get())
    filter_string += convert_to_query("salary", salary_entry.get())

    if "AND" in filter_string[-4:]:
        filter_string = filter_string[:len(filter_string) - 4]
    elif filter_string == "\nWHERE ":
        filter_string = ""

    if filter_string != "":
        save_entry_boxes()
        filter_string = "SELECT rowid, * FROM " + CURRENT_TABLE + filter_string + ";"
        print_to_log("Filtering results on the below query: \n\n" + filter_string)
        db_treeview.delete(*db_treeview.get_children())  # clear view
        try:
            query_and_update_tree(filter_string)
            CURRENT_QUERY = filter_string
        except sq.OperationalError:
            print_to_log("An error occurred - please review the filter criteria!")
            query_and_update_tree(CURRENT_QUERY)
    else:
        print_to_log("No filter criteria specified!")


# -----------------------------------------------------------------------------------------------
def clear_filters():
    """ Clears any filters which are currently applied to the table view. """
    global CURRENT_TABLE, CURRENT_QUERY
    db_treeview.delete(*db_treeview.get_children())  # clear view
    CURRENT_QUERY = "SELECT rowid, * FROM " + CURRENT_TABLE + ";"
    query_and_update_tree(CURRENT_QUERY)
    clear_entryboxes()
    print_to_log("Filters cleared.")


# -----------------------------------------------------------------------------------------------
def add_record():
    """
    Allows for new records to be added to the database from the values currently inputted in
    the record entry boxes. Requires at least one entry box to be populated; any blank boxes
    will be imported to the table as NULL values.
    """
    global STATE, CURRENT_TABLE, CURRENT_QUERY
    if STATE == 0:
        print_to_log("You are not connected to a table!")
    else:
        if ID_entry.get() != "":
            print_to_log("Employee ID is assigned automatically! \n\n"
                         "Please ensure that this field is empty before adding any records.\n")
        else:
            try:
                query_and_update_tree("INSERT INTO " + CURRENT_TABLE +
                                      "(title, firstname, surname, email, salary)" +
                                      "VALUES(" +
                                      "'" + title_entry.get() + "', " +
                                      "'" + firstname_entry.get() + "', " +
                                      "'" + surname_entry.get() + "', " +
                                      "'" + email_entry.get() + "', " +
                                      salary_entry.get() + ");")
                print_to_log("Record added successfully!")
            except sq.OperationalError:
                print_to_log("An error occurred - the record was not added to the table.\n\n" +
                             "Please ensure that the cells are not blank, and that the salary\n"
                             "field does not contain any non-numeric characters.")

            # refresh current tree view
            db_treeview.delete(*db_treeview.get_children())
            query_and_update_tree(CURRENT_QUERY)
            clear_entryboxes()


# -----------------------------------------------------------------------------------------------
def select_record(event):
    """ Pulls the data for a selected record through to the entry boxes. """
    global ENTRY_BOXES
    save_entry_boxes()
    clear_entryboxes()
    values = db_treeview.item(db_treeview.focus(), 'values')
    try:
        ID_entry.insert(0, values[0])
        title_entry.insert(0, values[1])
        firstname_entry.insert(0, values[2])
        surname_entry.insert(0, values[3])
        email_entry.insert(0, values[4])
        salary_entry.insert(0, values[5])
        salary_formatted = "£" + values[5]
        if not "." in salary_formatted:
            salary_formatted = "£" + values[5][:len(values[5]) - 3] + "," + values[5][-3:]
        print_to_log("%s. %s %s\n\n%s's email address is: %s\n\n"
                     "%s's current salary is: %s" %
                     (values[1], values[2], values[3], values[2],
                      values[4], values[2], salary_formatted))
    except IndexError:
        pass
    if ID_entry.get() == "":
        restore_entry_boxes()


# -----------------------------------------------------------------------------------------------
def treeview_sql_sort(col):
    """
    Sorts the tree view records for a particular column, toggles between ascending and descending,
    tracked by the SORT_TOGGLES variable.
    """
    global SORT_TOGGLES, CURRENT_QUERY, COL_NAMES
    col_names = COL_NAMES[col]
    db_treeview.delete(*db_treeview.get_children())  # clear view

    if SORT_TOGGLES[col]:
        sorting_query = " ORDER BY " + col_names[0] + " DESC;"
        SORT_TOGGLES[col] = False
        print_to_log("Records sorted by " + col_names[1] + " (descending)")
    else:
        sorting_query = " ORDER BY " + col_names[0] + ";"
        SORT_TOGGLES[col] = True
        print_to_log("Records sorted by " + col_names[1] + " (ascending)")

    current_filter = CURRENT_QUERY
    current_filter = current_filter.replace(";", " ")
    current_filter += sorting_query
    print_to_log("\n\nSQL query:\n\n" + current_filter, append=True)
    try:
        query_and_update_tree(current_filter)
    except sq.OperationalError:
        print_to_log("An error occurred - the records were not sorted.\n\n"
                     "Please make sure that you are connected to a table "
                     "before sorting columns.")


# -----------------------------------------------------------------------------------------------
def update_record():
    """
    Allows for data for a record to be updated according to the entry box inputs.
    Uses the Employee ID of the selected record to determine which record to update.
    """
    global COL_NAMES, STATE, CURRENT_TABLE
    if STATE == 0:
        print_to_log("You are not connected to a table!")
    else:
        log_string = ""
        changed_fields = 0
        original_values = db_treeview.item(db_treeview.focus(), 'values')
        if not len(original_values) == 0:
            entered_values = [
                ID_entry.get(),
                title_entry.get(),
                firstname_entry.get(),
                surname_entry.get(),
                email_entry.get(),
                salary_entry.get()
            ]
            for i in range(0, len(entered_values)):
                if entered_values[i] != original_values[i]:
                    if i == 0:
                        log_string += ("    -    Employee ID is set automatically - this"
                                       " field cannot be updated.\n")
                    else:
                        log_string += ("    -    " + COL_NAMES[i][1] +
                                       " updated from " + original_values[i] +
                                       " to " + entered_values[i] + "\n")
                        changed_fields += 1

            try:
                query_and_update_tree("UPDATE " + CURRENT_TABLE + " SET "
                                      "title = '" + entered_values[1] + "', " +
                                      "firstname = '" + entered_values[2] + "', " +
                                      "surname = '" + entered_values[3] + "', " +
                                      "email = '" + entered_values[4] + "', " +
                                      "salary = " + entered_values[5] + " " +
                                      "WHERE rowid = " + original_values[0] + ";")
                db_treeview.item(db_treeview.focus(), text="",
                                 values=(original_values[0],
                                         entered_values[1],
                                         entered_values[2],
                                         entered_values[3],
                                         entered_values[4],
                                         entered_values[5]))
                clear_entryboxes()
                print_to_log(str(changed_fields) + " field(s) updated for Employee " +
                             original_values[0] + ":\n\n" + log_string)

            except sq.OperationalError:
                print_to_log("An error occurred - the record was not updated.\n\n" +
                             "Please make sure there aren't any illegal characters "
                             "in the entry boxes.")

        else:
            print_to_log("No record selected!")


# -----------------------------------------------------------------------------------------------
def delete_record():
    """
    Allows for deletion of records from a table based on the current tree view selection
    """
    global CURRENT_QUERY, CURRENT_TABLE
    records = db_treeview.selection()
    failed_to_delete = []
    num_deleted = 0
    for record in records:
        try:
            query_and_update_tree("DELETE FROM " + CURRENT_TABLE +
                                  " WHERE rowid = " + record + ";")
            num_deleted += 1
        except sq.OperationalError:
            failed_to_delete.append(record)

    if len(failed_to_delete) > 0:
        print_to_log("An error occurred - employee(s) " + str(failed_to_delete) +
                     " could not be deleted.")
    else:
        if not len(records) == 0:
            print_to_log(str(num_deleted) + " record(s) deleted from " +
                         CURRENT_TABLE + "!")
        else:
            print_to_log("No records selected!")

    # refresh view and clear input boxes
    db_treeview.delete(*db_treeview.get_children())
    query_and_update_tree(CURRENT_QUERY)
    clear_entryboxes()


# -----------------------------------------------------------------------------------------------
def add_test_data():
    """Adds some dummy data to the current table."""
    if CURRENT_TABLE == "":
        print_to_log("Please connect to a table before trying to add data.")
    else:
        for i in range(10):
            if i % 2 == 0:
                title_entry.insert(0, random.choice(resources.mens_titles))
                firstname_entry.insert(0, random.choice(resources.mens_fnames))
            else:
                title_entry.insert(0, random.choice(resources.womens_titles))
                firstname_entry.insert(0, random.choice(resources.womens_fnames))
            surname_entry.insert(0, random.choice(resources.last_names))
            email_entry.insert(0, firstname_entry.get()[:1] + "." +
                               surname_entry.get() + "@test.co.uk")
            salary_entry.insert(0, random.randint(20000, 60000))
            add_record()


# -----------------------------------------------------------------------------------------------
def administration():
    """
    Comprises the logic for database administration tasks, (i.e. creating tables)
    """
    global CURRENT_QUERY, CURRENT_TABLE, CONSOLE, AWAITING_INPUT, STATE
    if STATE is None:
        print_to_log("Unrecognised input: " + CONSOLE + "\n\n" +
                     "To interact with the system, please select an option "
                     "from one of the dropdown menus at \nthe top left of the window, "
                     "then follow the instructions as shown in the Output field.")
    if STATE == 0:
        record_entry_state(DISABLED)
        print_to_log(resources.init_msg)
        STATE = None
    elif STATE == 1:  # CONNECT TO TABLE
        if AWAITING_INPUT:
            db_treeview.delete(*db_treeview.get_children())  # clear tree view
            CURRENT_TABLE = CONSOLE
            CURRENT_QUERY = "SELECT rowid, * FROM " + CURRENT_TABLE + ";"
            try:
                query_and_update_tree(CURRENT_QUERY)
                record_entry_state(NORMAL)
                clear_entryboxes()
                print_to_log("Successfully connected to the " + CONSOLE + " table!")
            except sq.OperationalError:
                print_to_log("No table named '" + CONSOLE + "' was found!\n\n"
                             "Please try again - note that table names are case sensitive!")
            AWAITING_INPUT = False
            CONSOLE = ""
            STATE = None
        else:
            print_to_log("Please specify the table you want to connect to by typing its "
                         "name in the Input field... \n\n"
                         "Tables:\n" + get_list_of_tables())
            AWAITING_INPUT = True

    elif STATE == 2:  # CREATE TABLE
        if not AWAITING_INPUT:
            print_to_log("Please enter a name for the new table in the Input field...")
            AWAITING_INPUT = True
        else:
            if CONSOLE in get_list_of_tables():
                print_to_log("The " + CONSOLE + " table already exists!")
            else:
                try:
                    sql_query("CREATE TABLE IF NOT EXISTS " + CONSOLE +
                              "(title TEXT, "
                              "firstname TEXT, "
                              "surname TEXT, "
                              "email TEXT, "
                              "salary INTEGER)")
                    print_to_log("The " + CONSOLE + " table has now been created!")
                    if CURRENT_TABLE == "":
                        CURRENT_TABLE = CONSOLE
                        CURRENT_QUERY = "SELECT rowid, * FROM " + CURRENT_TABLE + ";"
                        query_and_update_tree(CURRENT_QUERY)
                        record_entry_state(NORMAL)
                        print_to_log("\n\nYou are now connected to the " + CONSOLE + " table... \n\n"
                                     "Try adding some records with File > Add Dummy Data so that it "
                                     "doesn't look so empty!", append=True)

                except sq.OperationalError:
                    print_to_log("The table could not be created!\n\n"
                                 "Please make sure that the table name is not a "
                                 "reserved SQL keyword.")
                AWAITING_INPUT = False
                CONSOLE = ""
                STATE = None

    elif STATE == 3:  # DELETE TABLE
        if not AWAITING_INPUT:
            print_to_log("Please enter the name of the table to delete in the Input field..."
                         "\n\nTables:\n\n" + get_list_of_tables())
            AWAITING_INPUT = True
        else:
            if CONSOLE in get_list_of_tables():
                sql_query("DROP TABLE IF EXISTS " + CONSOLE + " ;")
                if CONSOLE == CURRENT_TABLE:
                    CURRENT_TABLE = ""
                    db_treeview.delete(*db_treeview.get_children())  # clear tree view
                print_to_log("The " + CONSOLE + " table has been deleted.")
                if CURRENT_TABLE == "":
                    print_to_log("\n\nPlease select an option from the File menu.", append=True)
                AWAITING_INPUT = False
                CONSOLE = ""
                STATE = None
            else:
                print_to_log("No table named '" + CONSOLE + "' was found!\n\n"
                             "Please try again - note that table names are case sensitive!")


# -----------------------------------------------------------------------------------------------
def get_admin_input(e):
    """Called when enter is pressed on the input entry - gets input and clears the entry box"""
    global CONSOLE
    CONSOLE = admin_input.get()
    administration()
    admin_input.delete(0, END)


def admin_connect_to_table():
    """Called when File > Connect to a Table is selected."""
    global AWAITING_INPUT, STATE
    if STATE != 1:
        AWAITING_INPUT = False
        STATE = 1  # state 1 = connecting
    administration()


def admin_create_table():
    """Called when File > Create a Table is selected."""
    global AWAITING_INPUT, STATE
    if STATE != 2:
        AWAITING_INPUT = False
        STATE = 2  # state 2 = creating
    administration()


def admin_delete_table():
    """Called when File > Delete a Table is selected."""
    global AWAITING_INPUT, STATE
    if STATE != 3:
        AWAITING_INPUT = False
        STATE = 3  # state 3 = deleting
    administration()


# -----------------------------------------------------------------------------------------------
# UI Setup - Codemy's 'Python GUIs with Tkinter' series was used as a guide
# (Codemy.com, 2021)
# -----------------------------------------------------------------------------------------------
mainbg = "#CED6D9"
highlight = "#DFE4E6"
disabled_bg = "#B6C2C5"
button = "#E4E3DD"
button_fg = "#5e5a4b"

db_window = Tk()
db_window.title('Employee Database')
db_window.geometry("670x680")
db_window.iconbitmap("database.ico")
db_window.config(bg=mainbg)
style = ttk.Style()  # add styling
style.theme_use('clam')  # add theme

# add console input entry box
input_frame = LabelFrame(db_window, text="INPUT (Enter to Submit)",
                         bg=mainbg, font=('consolas', 8, 'bold'), labelanchor='n')
input_frame.pack(fill="x", padx=180)
admin_input = Entry(input_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8, 'bold'))
admin_input.pack(fill="x", padx=20, pady=10)
admin_input.bind("<Return>", get_admin_input)  # read user input when Enter is pressed

# configure colours for treeview
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=20,
                fieldbackground="#D3D3D3",
                font=('consolas', 8))
style.map('Treeview', background=[('selected', "#4C6E83")])
style.configure("Treeview.Heading", foreground='#5e5a4b', font='consolas 9 bold')

# -----------------------------------------------------------------------------------------------
# create the treeview
tree_frame = Frame(db_window)
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
db_treeview = ttk.Treeview(tree_frame,
                           yscrollcommand=tree_scroll.set,
                           selectmode="extended")
db_treeview.pack()
tree_scroll.config(command=db_treeview.yview)

db_treeview['columns'] = (COL_NAMES[0][1], COL_NAMES[1][1], COL_NAMES[2][1],
                          COL_NAMES[3][1], COL_NAMES[4][1], COL_NAMES[5][1])

# format columns
DEFAULT_COL_WIDTH = 92
db_treeview.column("#0", width=0, stretch=NO)
db_treeview.column(COL_NAMES[0][1], anchor=CENTER, width=DEFAULT_COL_WIDTH)
db_treeview.column(COL_NAMES[1][1], anchor=CENTER, width=DEFAULT_COL_WIDTH)
db_treeview.column(COL_NAMES[2][1], anchor=CENTER, width=DEFAULT_COL_WIDTH)
db_treeview.column(COL_NAMES[3][1], anchor=CENTER, width=DEFAULT_COL_WIDTH)
db_treeview.column(COL_NAMES[4][1], anchor=CENTER, width=DEFAULT_COL_WIDTH * 2)
db_treeview.column(COL_NAMES[5][1], anchor=CENTER, width=DEFAULT_COL_WIDTH)

# create striped row tags (for alternating rows)
db_treeview.tag_configure('oddrow', background="white")
db_treeview.tag_configure('evenrow', background="#D3E4EE")

# create headings
db_treeview.heading("#0", text="", anchor=W)
db_treeview.heading(COL_NAMES[0][1], text=COL_NAMES[0][1], anchor=CENTER,
                    command=lambda: treeview_sql_sort(0))
db_treeview.heading(COL_NAMES[1][1], text=COL_NAMES[1][1], anchor=CENTER,
                    command=lambda: treeview_sql_sort(1))
db_treeview.heading(COL_NAMES[2][1], text=COL_NAMES[2][1], anchor=CENTER,
                    command=lambda: treeview_sql_sort(2))
db_treeview.heading(COL_NAMES[3][1], text=COL_NAMES[3][1], anchor=CENTER,
                    command=lambda: treeview_sql_sort(3))
db_treeview.heading(COL_NAMES[4][1], text=COL_NAMES[4][1], anchor=CENTER,
                    command=lambda: treeview_sql_sort(4))
db_treeview.heading(COL_NAMES[5][1], text=COL_NAMES[5][1], anchor=CENTER,
                    command=lambda: treeview_sql_sort(5))

# add attribute data to entry boxes if record selected
db_treeview.bind("<ButtonRelease-1>", select_record)

# -----------------------------------------------------------------------------------------------
# add buttons for interacting with table data
button_frame = LabelFrame(db_window, text="", bg=mainbg)
button_frame.pack(padx=20, pady=0)

buttonpad = 6
add_button = Button(button_frame, text="Add Record", command=add_record,
                    font=('consolas', 8, 'bold'), bg=button, fg=button_fg)
add_button.grid(row=0, column=0, padx=buttonpad, pady=10)

update_button = Button(button_frame, text="Update Record", command=update_record,
                       font=('consolas', 8, 'bold'), bg=button, fg=button_fg)
update_button.grid(row=0, column=1, padx=buttonpad, pady=10)

delete_button = Button(button_frame, text="Delete Record(s)", command=delete_record,
                       font=('consolas', 8, 'bold'), bg=button, fg=button_fg)
delete_button.grid(row=0, column=2, padx=buttonpad, pady=10)

filter_button = Button(button_frame, text="Filter Records", command=filter_records,
                       font=('consolas', 8, 'bold'), bg=button, fg=button_fg)
filter_button.grid(row=0, column=3, padx=buttonpad, pady=10)

clear_filter_button = Button(button_frame, text="Clear Filters", command=clear_filters,
                             font=('consolas', 8, 'bold'), bg=button, fg=button_fg)
clear_filter_button.grid(row=0, column=4, padx=buttonpad, pady=10)

clear_entries_button = Button(button_frame, text="Clear Inputs", command=clear_entryboxes,
                              font=('consolas', 8, 'bold'), bg=button, fg=button_fg)
clear_entries_button.grid(row=0, column=5, padx=buttonpad, pady=10)

# -----------------------------------------------------------------------------------------------
# add record entry boxes
data_frame = LabelFrame(db_window, text="", bg=mainbg)
data_frame.pack(padx=0, pady=5)

labelpad = 0
entrypad = 3

ID_label = Label(data_frame, text=COL_NAMES[0][1], bg=mainbg, font=('consolas', 8, 'bold'))
ID_label.grid(row=1, column=0, padx=labelpad, pady=5)
ID_entry = Entry(data_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8))
ID_entry.grid(row=1, column=1, padx=entrypad, pady=5)

title_label = Label(data_frame, text=COL_NAMES[1][1], bg=mainbg, font=('consolas', 8, 'bold'))
title_label.grid(row=0, column=0, padx=labelpad, pady=5)
title_entry = Entry(data_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8))
title_entry.grid(row=0, column=1, padx=entrypad, pady=5)

firstname_label = Label(data_frame, text=COL_NAMES[2][1], bg=mainbg, font=('consolas', 8, 'bold'))
firstname_label.grid(row=0, column=2, padx=labelpad, pady=5)
firstname_entry = Entry(data_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8))
firstname_entry.grid(row=0, column=3, padx=entrypad, pady=5)

surname_label = Label(data_frame, text=COL_NAMES[3][1], bg=mainbg, font=('consolas', 8, 'bold'))
surname_label.grid(row=0, column=4, padx=labelpad, pady=5)
surname_entry = Entry(data_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8))
surname_entry.grid(row=0, column=5, padx=entrypad, pady=5)

email_label = Label(data_frame, text=COL_NAMES[4][1], bg=mainbg, font=('consolas', 8, 'bold'))
email_label.grid(row=1, column=2, padx=labelpad, pady=5)
email_entry = Entry(data_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8))
email_entry.grid(row=1, column=3, padx=entrypad, pady=5)

salary_label = Label(data_frame, text=COL_NAMES[5][1], bg=mainbg, font=('consolas', 8, 'bold'))
salary_label.grid(row=1, column=4, padx=labelpad, pady=5)
salary_entry = Entry(data_frame, bg=highlight, disabledbackground=disabled_bg, font=('consolas', 8))
salary_entry.grid(row=1, column=5, padx=entrypad, pady=5)

# -----------------------------------------------------------------------------------------------
# add output console
log_frame = LabelFrame(db_window, text="OUTPUT", bg=mainbg, font=('consolas', 10, 'bold'), labelanchor='n')
log_frame.pack(padx=0, pady=0, expand=1, fill="both")
output_log = Text(log_frame, bg=highlight, wrap=WORD)
output_log.pack(padx=5, pady=5, fill="both")
output_log.config(font=('consolas', 11))


# -----------------------------------------------------------------------------------------------
# add dropdown menus
menu_bar = Menu(db_window)
db_window.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=False)
file_menu.add_command(label='Connect to a Table', command=admin_connect_to_table)
file_menu.add_command(label='Create a Table', command=admin_create_table)
file_menu.add_command(label='Delete a Table', command=admin_delete_table)
file_menu.add_command(label='Add Dummy Data', command=add_test_data)

help_menu = Menu(menu_bar, tearoff=False)
help_menu.add_command(label='Adding Records',
                      command=lambda: print_to_log(resources.adding))
help_menu.add_command(label='Deleting Records',
                      command=lambda: print_to_log(resources.deleting))

filter_menu = Menu(help_menu, tearoff=0)
filter_menu.add_command(label='Using Filters',
                        command=lambda: print_to_log(resources.filtering))
filter_menu.add_command(label='Comparison Operators',
                        command=lambda: print_to_log(resources.comparison))
filter_menu.add_command(label='Wildcards',
                        command=lambda: print_to_log(resources.wildcards))

help_menu.add_cascade(label='Filtering Records', menu=filter_menu)
help_menu.add_command(label='Updating Records',
                      command=lambda: print_to_log(resources.updating))

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)

# -----------------------------------------------------------------------------------------------
administration()
db_window.mainloop()
