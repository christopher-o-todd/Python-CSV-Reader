import mysql.connector
from mysql.connector import errorcode
from csv import reader, writer


#Create MySQL Connection:

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="PasswordPlaceHolder",
      database="bitcoindb"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
        
print(mydb.is_connected())

cursor = mydb.cursor()
cursor.execute('DROP TABLE IF EXISTS all_data;')

TABLES = {} #create an empty dictionary

#Create table with name all_data

TABLES['all_data'] = (
 "CREATE TABLE `all_data` ("
 "`Date` varchar(20) NOT NULL,"
 "`txVolume` varchar(20) NOT NULL,"
 "`adjustedTxVolume` varchar(20) NOT NULL,"
 "`txCount` varchar(20) NOT NULL,"
 "`marketcap` varchar(20) NOT NULL,"
 "`price` varchar(20) NOT NULL,"
 "`exchangeVolume` varchar(20) NOT NULL,"
 "`generatedCoins` varchar(20) NOT NULL,"
 "`fees` varchar(20) NOT NULL,"
 "`activeAddresses` varchar(20) NOT NULL,"
 "`averageDifficulty` varchar(20) NOT NULL,"
 "`paymentCount` varchar(20) NOT NULL,"
 "`medianTxValue` varchar(20) NOT NULL,"
 "`medianFee` varchar(20) NOT NULL,"
 "`blockSize` varchar(20) NOT NULL,"
 "`blockCount` varchar(20) NOT NULL"
 ") ENGINE=InnoDB")

table_description = TABLES['all_data']
try:
    print("Creating table {}: ".format('all_data'), end='')
    cursor.execute(table_description)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("table already exists")
    else:
        print(err.msg)
else:
    print("OK")

#Read the CSV data and write to MySQL row by row:

file_bitcoin = open("bitcoin_csv.csv") #open the CSV file
csv_reader = reader(file_bitcoin) #read the open CSV file
next(csv_reader) #skip the first row (column names)

for row in csv_reader:
    
    if len(row[5]) > 0: #if there's data in the price column
        cursor.execute("INSERT INTO all_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", #values in the table %s going into the index values below
                      [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]])
        mydb.commit()

print("100% done!")

mydb.commit()
