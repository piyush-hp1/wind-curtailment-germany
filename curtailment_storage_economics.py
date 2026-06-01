# Note: Sample data used for model testing. 
# To be replaced with real SMARD.de curtailment data.

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
data = {

"Farm":["F1","F2","F3","F4"],

"Curtailed_Energy_MWh":[
1200,
1800,
2500,
1400
],

"Avg_Market_Price":[
85,
78,
92,
80
],

"Storage_Hours":[
4,
6,
5,
3
]
}

Storage_efficiency={
    "F1":0.88,
    "F2":0.84,
    "F3":0.91,
    "F4":0.82
}
Battery_cost={
    "F1":400000,
    "F2":550000,
    "F3":750000,
    "F4":350000
}
df=pd.DataFrame(data)
df["Storage_recovery_efficiency"]=df["Farm"].map(Storage_efficiency)
df["Battery_installation_cost"]=df["Farm"].map(Battery_cost)
df["Recoverable_enrgy MWh"]=df["Curtailed_Energy_MWh"]*df["Storage_recovery_efficiency"]
df["Revenue"]=df["Recoverable_enrgy MWh"]*df["Avg_Market_Price"]
df["Profit"]=df["Revenue"]-df["Battery_installation_cost"]
df["ROI"]=(df["Profit"]/df["Battery_installation_cost"])*100
df["Payback_Years"] = df.apply(
    lambda row: row["Battery_installation_cost"] / row["Profit"]
    if row["Profit"] > 0
    else "No Payback",
    axis=1
)

print(df)

conn=sqlite3.connect("farms.db")
df.to_sql("wdata",conn,if_exists="replace",index=False)

querry1="""
SELECT Farm, ROI
FROM wdata
ORDER BY ROI DESC
LIMIT 1
"""
result1=pd.read_sql(querry1,conn)
print(result1)

querry2="""
SELECT Farm, ROI
FROM wdata
ORDER BY ROI  ASC
LIMIT 1
"""
result2=pd.read_sql(querry2,conn)
print(result2)

querry3="""
SELECT Farm, ROI
FROM wdata
ORDER BY ROI  DESC
"""
result3=pd.read_sql(querry3,conn)
print(result3)

query4="""
SELECT Farm,ROI
FROM wdata
WHERE ROI>40
"""
result4=pd.read_sql(query4,conn)

querry5="""
SELECT Farm, Profit
FROM wdata
ORDER BY Profit  DESC
"""
result5=pd.read_sql(querry5,conn)
print(result5)

plt.plot(df["Farm"],df["ROI"])
plt.xlabel("Farm")
plt.ylabel("ROI")
plt.title("ROI by Farm")
plt.show()
