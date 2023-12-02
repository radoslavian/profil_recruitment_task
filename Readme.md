## Installation
The scripts were written for Python version 3.11.3.  
Once downloaded, within a script directory a virtual environment
needs to be created - according to the
[documentation](https://docs.python.org/3/library/venv.html):
```
$ python -m venv ./venv
```  
Then install the required additional libraries
(SQLAlchemy and LXML) listed in requirements.txt:
```
$ pip3 -r ./requirements.txt
```
## Data import
For the script to work properly, the directory with the data to be 
imported (`data`) must be a subdirectory of the script
(i.e. located in where I put it in the repository).  
You can optionally import data from another location. To do so,
change the value of the `DATA_DIR` constant in the `script.py` file - 
it points to the directory with the files to be imported.  
Before first use, you must create the database and import the data
into it:
```
$ python script.py create_database
```
the command imports data from data files into a SQLite database
in `./database` directory.

## Example usage
Printing the oldest account:  
```
$ python script.py print-oldest-account --login briancollins@example.net --password 'R9AjA5nb$!'
name: Justin
email_address: opoole@example.org
created_at: 2022-11-25 02:19:37
```

Group Children by Age
```
$ python script.py group-by-age --login briancollins@example.net --password 'R9AjA5nb$!'
age: 5, count: 4
age: 10, count: 4
age: 14, count: 4
age: 6, count: 5
...
```
Printing the children of the logged-in user:
```
$ python script.py print-children --login briancollins@example.net --password 'R9AjA5nb$!'
Andrew, 3
Nicholas, 13
```
Printing out children of a similar age to the children of a 
logged-in user (together with their parents):
```
$ python script.py find-similar-children-by-age --login briancollins@example.net --password 'R9AjA5nb$!'
Joseph, 018820162: Wendy, 3
Danny, 342559287: David, 3
Sarah, 318506164: Bradley, 13
...
```

## WARNING
Bash (and probably other Linux shells) interprets some
characters as special (e.g. !, #, $) - if login fails
using the correct password, enter this password in
single quotes - __' '__ (like _literal string_
in Perl).