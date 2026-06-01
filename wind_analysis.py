# Data Source: NASA POWER - https://power.larc.nasa.gov/data-access-viewer/
# Location: Windpark Holtriem, Lower Saxony, Germany
# Coordinates: 53.6103N, 7.4292E
# Note: Download monthly wind speed data and update the file path below
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
df=pd.read_csv("/content/3.POWER_Point_Monthly_19810101_20251231_053d61N_007d43E_UTC.csv",skiprows=9)
df=df.drop(columns=["PARAMETER"])

conn=sqlite3.connect("data.db")
df.to_sql("wind",conn,if_exists="replace",index=False)

average_wind_speed="""
SELECT AVG(ANN) AS Average_Wind_Speed
FROM wind
"""
result1=pd.read_sql(average_wind_speed,conn)
print(f"Average Wind Speed: {result1['Average_Wind_Speed'][0]:.2f} m/s")

Highest_Wind_speed_year="""
SELECT YEAR,ANN
FROM wind
ORDER BY ANN DESC
LIMIT 1
"""
result2=pd.read_sql(Highest_Wind_speed_year,conn)
print(f"Year with Highest Wind Speed:{result2['YEAR'][0]}")

Lowest_Wind_speed_years="""
SELECT YEAR,ANN
FROM wind
ORDER BY ANN ASC
LIMIT 1
"""
result3=pd.read_sql(Lowest_Wind_speed_years,conn)
print(f"Year with Lowest Wind speed is:{result3['YEAR'][0]}")

months=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
monthly_avg= df[months].mean(axis=0)
Hihghes_monthly_avg=monthly_avg.idxmax()
Lowest_monthly_avg=monthly_avg.idxmin()
print(f"Month with Highest Average Wind Speed: {Hihghes_monthly_avg}")
print(f"Month with Lowest Average Wind Speed: {Lowest_monthly_avg}")


plt.plot(df["YEAR"],df["ANN"],marker='o')
plt.xlabel("Year")
plt.ylabel("Wind Speed (m/s)")
plt.title("Wind Speed Over Time")
plt.show()

plt.plot(months,monthly_avg,marker='o')
plt.xlabel("Month")
plt.ylabel("Monthly average wind speed")
plt.title("Monthly average wind speed by month")
plt.show()

Turbine_data={
    "Turbine":["Enercon E66"],
    "Rotor_Area":[3848],
    "Cp":[0.42],
    "Cut_in":[2.5],
    "Cut_out":[34],
    "Rated_Power_MW":[1.8],
    "Turbine_Count":[33]
}
tdf=pd.DataFrame(Turbine_data)
print(tdf)
df=df[df["YEAR"]>=1998]
df["key"]=1
tdf["key"]=1
final_data=pd.merge(df,tdf,on="key")
final_data=final_data.drop(columns=["key"])
rho = 1.225
final_data["Power_w"]= final_data.apply(
    lambda row:
    0.5
    *rho
    *row["Rotor_Area"]
    *(row["ANN"]**3)
    *row["Cp"]
    if row["ANN"]>= row["Cut_in"] and row["ANN"]<= row["Cut_out"]
    else 0,
    axis=1
)
final_data["Power_MW"]=final_data["Power_w"]/1000000
final_data["Farm_Power_MW"] = (
    final_data["Power_MW"]
    * final_data["Turbine_Count"]
)
final_data["Farm_Energy_MWh"] = (
    final_data["Farm_Power_MW"]
    * 8760
)
print(
    final_data[
        ["YEAR","ANN","Power_MW","Farm_Power_MW","Farm_Energy_MWh"]
    ].head()
)
print(final_data["Power_MW"].max())
