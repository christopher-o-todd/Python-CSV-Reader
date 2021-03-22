import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
%matplotlib notebook


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
        print("somehing is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
        
print(mydb.is_connected())

#Select the data from MySQL:
cursor = mydb.cursor()

sql_select = "SELECT Date, price FROM all_data"
cursor.execute(sql_select)

columns = [column[0] for column in cursor.description] 

data = cursor.fetchall()

mydb.close()

#Create the dataframe:

data = pd.DataFrame(data, columns=columns)
data['price'] = pd.to_numeric(data['price']) #convert all price values to float64 data type
data['Date'] = pd.to_datetime(data['Date']) #convert data values to dates

data.set_index('Date', inplace=True)

#Plot the data:

fig = plt.figure()

plt.xticks(rotation=45, ha="right", rotation_mode="anchor") 
plt.subplots_adjust(bottom = 0.2, top = 0.9)
plt.ylabel('Bitcoin Price (USD)')
plt.xlabel('Date')
plt.grid(b=True, which='major', color='#666666', linestyle='-') 
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

def plot_maker_2000(i):
    plot = plt.plot(data[:i].index, data[:i].values) 

animation = FuncAnimation(fig, plot_maker_2000, interval = 1000)

plt.show()

#Clear the plot:
#plt.clf()
#plt.cla()
#plt.close()
