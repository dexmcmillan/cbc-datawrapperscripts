import datawrappergraphics
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as ax3d
import pandas as pd

raw = pd.read_html("https://www.canada.ca/en/public-health/services/diseases/monkeypox.html")[0]


df = pd.DataFrame({"province": []})

for i, row in raw.iterrows():
    print(i)
    for case in range(0, row["Confirmed cases"]):
        if len(df)>0:
            df.loc[len(df)] = row["Province or Territory"]
        else:
            df.loc[0] = row["Province or Territory"]
        
def fibonacci_disc(numpts: int):

    ga = np.pi * (3 - np.sqrt(5)) # golden angle
    theta = np.arange(numpts) * ga

    radius = np.sqrt(np.arange(numpts) / float(numpts))
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    # Display points in a scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, [0] * numpts)

    return (x, y)
    
disc = fibonacci_disc(len(df))
df2 = pd.DataFrame({"x": disc[0], "y": disc[1]})
df2["province"] = df["province"]
df2 = df2.set_index("province").join(raw.set_index("Province or Territory"))

most_cases = raw.sort_values("Confirmed cases", ascending=False).head(1).reset_index().loc[0, "Province or Territory"]

(datawrappergraphics.Chart(chart_id="aMiZb")
 .data(df2)
 .deck(f"Canada has reported <b>{len(df2)} confirmed cases</b>, with the majority of cases (<b>{round(len(df2[df2.index == most_cases])/len(df2)*100, 1)}%</b>) in <b>{most_cases}</b>.<br><br>Hover over or tap each dot to see confirmed cases in that province or territory.")
 .publish()
 )