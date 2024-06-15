# Name: Yeabsira Moges
# Email: yamoges@student.rtc.edu
# Date: 09/15/2024
# Class: CNE 370
# Project Description: This code queries a database from a max-scale container running on 172.20.10.12

import mysql.connector

conn = mysql.connector.connect(
    user='maxuser',
    password='maxpwd',
    host='172.20.10.12',
    port='4000'
)
cursor = conn.cursor()

#### Queries and print the largest zipcode
cursor.execute("SELECT MAX(zipcode) FROM zipcodes_one.zipcodes_one")
print("=================================================")
print(cursor.fetchone()[0], "is the largest zipcodes in zipcodes_one")
print("=================================================")


#### Queries zipcode where state is Kentucky
print("=================================================")
print("Zipcodes in Kentucky")
print("=================================================")
cursor.execute("SELECT zipcode FROM zipcodes_one.zipcodes_one WHERE state='KY'")
zipcodes_one = cursor.fetchall()
cursor.execute("SELECT zipcode FROM zipcodes_two.zipcodes_two WHERE state='KY'")
zipcodes_two = cursor.fetchall()
zipcodes = zipcodes_one + zipcodes_two
for zipcode in zipcodes:
    print(zipcode[0])



#### Query Zipcode between 40000 & 410000
print("=================================================")
print("Zipcodes between 40000 and 410000")
print("=================================================")
cursor.execute("SELECT zipcode FROM zipcodes_one.zipcodes_one WHERE zipcode BETWEEN 40000 AND 41000")
zipcode_one_4 = cursor.fetchall()
cursor.execute("SELECT zipcode FROM zipcodes_two.zipcodes_two WHERE zipcode BETWEEN 40000 AND 41000")
zipcode_two_4 = cursor.fetchall()
zipcodes_4 = zipcode_two_4 + zipcode_one_4
for zipcode in zipcodes_4:
        print(zipcode[0])



#### Query Total Wages in Pennyslvania state
print("=================================================")
print("Total Wages Column in Pennsylvania")
print("=================================================")
cursor.execute("SELECT TotalWages FROM zipcodes_one.zipcodes_one WHERE state='PA'")
wage_one = cursor.fetchall()
cursor.execute("SELECT TotalWages FROM zipcodes_two.zipcodes_two WHERE state='PA'")
wage_two = cursor.fetchall()
wage_all = wage_one + wage_two
for wage in wage_all:
        print(wage[0])




cursor.close()
conn.close()