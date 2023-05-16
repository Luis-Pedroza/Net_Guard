# ***************************************************
# FILE: InsertPorts.py
#
# DESCRIPTION: 
# This code opens a CSV containing all register ports
# It reads the CSV file, retrieves the information, and inserts it into a database.
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

import csv
import sqlite3

# Declare a counter and a boolean
firstRow = True
count = 0

# Open and read file "service-names-port-numbers.csv"
# File must be in the same folder as the DB
file=open('Data/service-names-port-numbers.csv')
reader = csv.reader(file)

try:
    #Connection to ports.db
    db_name = 'Data/ports.db'
    connection = sqlite3.connect(db_name)
    pointer = connection.cursor()

    #Read each row on the file
    for row in reader:    
        #Exclude the first row because it´s the header of the table
        if firstRow:
            firstRow = False
            continue
        #If a service name is Null then assign "Unassigned"
        if row[0] == '':
            row[0] = 'Unassigned'

        #Initialize the query with 
        #row[1]=Port Number, row[0]=Service Name, row[2]=Transport Protocol, row[3]=Description, row[8]=Reference
        query = 'INSERT INTO Ports_Info (Port, Service, Protocol, Description, Reference) values (?, ?, ?, ?, ?)'
        params = (row[1],row[0],row[2],row[3], row[8])
        pointer.execute(query,params)

    #Commit query and close DB
    connection.commit()
    print('Data was inserted')
    connection.close()

#Exception control
except sqlite3.Error as e: print('Error executing SQL command: ', e)