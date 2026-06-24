import matplotlib.pyplot as plt
import pandas as pd
qualifying=pd.read_csv("qualifying.csv")
races=pd.read_csv("races.csv")
drivers=pd.read_csv("drivers.csv")
circuits=pd.read_csv("circuits.csv")
circuits=circuits.drop(columns=["url"])
races=races.drop(columns=["url"])
drivers=drivers.drop(columns=["url"])

a=qualifying.merge(races,on="raceId")
merge=a.merge(drivers,on="driverId")
mg=merge.merge(circuits,on="circuitId")


ham=mg[mg["surname"]=="Hamilton"]
kov=mg[mg["surname"]=="Kovalainen"]

def convert(lap):
    if lap == 0 or not lap or lap == r"\N" or lap == "\\N":
        return 0.0
    if isinstance(lap, (int, float)):
        return float(lap)
    b=lap.split(":")
    if len(b)>1:
        min=float(b[0])*60
        second=float(b[1])
        return min+second
    else:
        return float(b[0])
            
ham["q1_sec"] = ham["q1"].apply(convert)
ham["q2_sec"] = ham["q2"].apply(convert)
ham["q3_sec"] = ham["q3"].apply(convert)
kov["q1_sec"] = kov["q1"].apply(convert)
kov["q2_sec"]=kov["q2"].apply(convert)
kov["q3_sec"]=kov["q3"].apply(convert)

ham_year=ham[ham["year"]==2008]
kov_year=kov[kov["year"]==  2008]

ham_q3=ham_year[["raceId","q3_sec","location"]]
kov_q3=kov_year[["raceId","q3_sec","location"]]
merge_q3=(ham_q3[ham_q3["q3_sec"]>0]).merge((kov_q3[kov["q3_sec"]>0]),on="raceId")

merge_q3["win_time"]=merge_q3["q3_sec_x"]-merge_q3["q3_sec_y"]
colors =['#FF8700'if x<0 else '#00A6FF' for x in merge_q3["win_time"]]
plt.figure(figsize=(12,6),facecolor="#1C1D21")
plt.barh(merge_q3["location_x"],merge_q3["win_time"],color=colors)
plt.xlabel("Qualifying Time Gap (Seconds) | ◄ Hamilton Faster | Kovalainen Faster ►",color="white")
plt.ylabel("Race Track",color="white")
plt.title("2008 McLaren F1 Teammate Qualifying Battle: Hamilton vs. Kovalainen",color="white")
ax=plt.gca()
ax.set_facecolor("#121316")
ax.tick_params(colors="white")
ax.spines["left"].set_color("white")
ax.spines["bottom"].set_color("white")

plt.show()