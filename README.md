# Employee-Management-System
An employee management system designed as part of my Computer Science MSc course at the University of Bath. 
The system was built with Tkinter and utilises an SQLite database for the storage of customer records.


The system allows users to create or delete tables, and connect to existing tables, by specifying 
the relevant option from the File menu.

![image](https://user-images.githubusercontent.com/83663539/207992016-a6554451-1032-4b26-8754-b22de079ed6f.png)


Adding Records:
---------------
To add a new record to the database, enter the relevant information in the entry 
boxes and press 'Add Record'.
The ID of a record is assigned automatically; make sure that this field is empty 
before attempting to add any records.
          
Deleting Records:
-----------------
Once connected to a table, to delete one (or many) records, select the rows you 
wish to delete from the list, and then select 'Delete Record(s).
Note that several records can be selected at once by holding the Ctrl key down 
while clicking on records. Alternatively, a range can be selected by clicking the top 
record, holding the Shift key, and then clicking the bottom record in the range.
            
Filtering Records:
------------------
The system supports filtering of records. If a specific value is entered in one 
of the fields and the 'Filter Records' button is pressed, the system will filter 
the results to show only records which match the entered value for a given field.
The system also supports filtering based on wildcards and comparison operators, 
although the two cannot be combined.
Please see the relevant sub-menus for more information.
             
Filtering Records with Wildcards:
---------------------------------
This system supports the use of the SQLite '%' and ' _ ' wildcards. 
'%' represents any number of numbers/characters. For example, applying the filter: 
'Jo%n' would show any text starting with 'Jo' and ending in 'n'.
' _ ' represents any single number/character. For example, applying the filter: 'J_n' 
would show all three letter records starting with 'J' and ending in 'n'.
             
Filtering Records with Comparison Operators:
--------------------------------------------
This system supports the use of comparison operators on both TEXT and INTEGER fields.
If used on text fields, comparison operators will filter records based on their 
alphabetical order. For example, '>Mr' will return all records which follow 'Mr' 
alphabetically, including 'Mrs'. \n\nOn number fields, comparison operators filter 
records based on their numerical value; i.e., >21 will filter on fields which 
are greater than 21.
              
Updating Records:
-----------------
The system allows administrators to update records. Select the record you wish to 
update in the list view and the entry boxes will be populated with the corresponding 
records. The entry boxes can then be changed, whereupon pressing 'Update Record
will write these changes to the database.
Note that the 'Employee ID' field is set automatically and cannot be updated. If a user 
tries to update this field, they will be presented with an error message; any changes in 
other entry boxes will still be written to the database, however.
