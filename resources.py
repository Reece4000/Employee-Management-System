init_msg = ("Welcome!"
            "\n--------\n"
            "To get started, please select an option from the dropdown File menu.")

adding = ("Adding Records:\n"
          "---------------\n"
          "To add a new record to the database, enter the relevant information in the entry "
          "boxes and press 'Add Record'.\n\n"
          "The ID of a record is assigned automatically; make sure that this field is empty "
          "before attempting to add any records.")

deleting = ("Deleting Records:\n"
            "-----------------\n"
            "Once connected to a table, to delete one (or many) records, select the rows you "
            "wish to delete from the list, and then select 'Delete Record(s).\n\n"
            "Note that several records can be selected at once by holding the Ctrl key down "
            "while clicking on records. Alternatively, a range can be selected by clicking the top "
            "record, holding the Shift key, and then clicking the bottom record in the range.")

filtering = ("Filtering Records:\n"
             "------------------\n"
             "The system supports filtering of records. If a specific value is entered in one "
             "of the fields and the 'Filter Records' button is pressed, the system will filter "
             "the results to show only records which match the entered value for a given field.\n\n"
             "The system also supports filtering based on wildcards and comparison operators, "
             "although the two cannot be combined.\n\n"
             "Please see the relevant sub-menus for more information.\n")

wildcards = ("Filtering Records with Wildcards:\n"
             "---------------------------------\n"
             "This system supports the use of the SQLite '%' and '_' wildcards. \n\n"
             "'%' represents any number of numbers/characters. For example, applying the filter: "
             "'Jo%n' would show any text starting with 'Jo' and ending in 'n'.\n\n"
             "'_' represents any single number/character. For example, applying the filter: 'J_n' "
             "would show all three letter records starting with 'J' and ending in 'n'.")

comparison = ("Filtering Records with Comparison Operators:\n"
              "--------------------------------------------\n"
              "This system supports the use of comparison operators on both TEXT and INTEGER fields.\n\n"
              "If used on text fields, comparison operators will filter records based on their "
              "alphabetical order. For example, '>Mr' will return all records which follow 'Mr' "
              "alphabetically, including 'Mrs'. \n\nOn number fields, comparison operators filter "
              "records based on their numerical value; i.e., >21 will filter on fields which "
              "are greater than 21.")

updating = ("Updating Records:\n"
            "-----------------\n"
            "The system allows administrators to update records. Select the record you wish to "
            "update in the list view and the entry boxes will be populated with the corresponding "
            "records. The entry boxes can then be changed, whereupon pressing 'Update Record'"
            "will write these changes to the database.\n\n"
            "Note that the 'Employee ID' field is set automatically and cannot be updated. If a user "
            "tries to update this field, they will be presented with an error message; any changes in "
            "other entry boxes will still be written to the database, however.")

mens_fnames = [
    "Liam",
    "Oliver",
    "Noah",
    "Elijah",
    "James",
    "Will",
    "Ben",
    "Lucas",
    "Henry",
    "Theodore",
    "Jack",
    "Levi",
    "Alexander",
    "Kyle",
    "Gary",
    "Rowan",
    "Joshua",
    "Andrew"
]
womens_fnames = [
    "Katie",
    "Sarah",
    "Everlyne",
    "Gertrude",
    "Alice",
    "Natalie",
    "Jacinda",
    "Emily",
    "Fiona",
    "Imogen",
    "Amber",
    "Sally",
    "Christina",
    "Rachel",
    "Leela",
    "Tess",
    "Julie",
    "Jane",
    "Sophie",
    "Liz",
    "Teresa",
    "Tina"
]
womens_titles = [
    "Miss",
    "Ms",
    "Mrs",
    "Lady",
    "Duchess",
    "Rev",
    "Hon"
]
mens_titles = [
    "Mr",
    "Sir",
    "Lord",
    "Duke",
    "Prof",
    "Rev",
    "Hon"

]
last_names = [
    "Haigh",
    "Grant",
    "Johnson",
    "Lewis",
    "Thompson",
    "Myers",
    "Jackson",
    "Withington",
    "Smith",
    "Williams",
    "Brown",
    "Miller",
    "Davis",
    "Jones",
    "Garcia",
    "Gutierrez",
    "Laurent",
    "Dubois",
    "Martin",
    "Moreau",
    "Mills",
    "Cockroft",
    "Fielden",
    "Holden",
    "Clough",
    "Roberts",
    "Wright",
    "Evans",
    "Harris",
    "Turner",
    "Hughes",
    "Green",
    "Walker",
    "Hall",
    "White",
    "Davy",
    "Wood",
    "Robinson",
    "Wilson",
]