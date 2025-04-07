"""
This script generates out visualizations
"""

import altair as alt
import pandas as pd
import geopandas as gpd
import os
import seaborn as sns
import matplotlib.pyplot as plt

current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../"))
stations = pd.read_csv(project_root + "/data/current_bluebikes_stations.csv")
trips = pd.read_csv(project_root + "/data/trip_data.csv")


def category_hist(x):
    fig = plt.figure(figsize = (7, 4))
    sns.boxplot(x = trips[x], y = trips["duration"], showfliers = False)
    plt.xlabel(x)
    plt.ylabel("Duration")
    plt.title(f"Box and Whisker plot of ride duration by {x}")
    plt.tight_layout()
    return fig

def main():
    print("Your ran the visualizations file")
    current_file = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(current_file, "../../"))
    stations = pd.read_csv(project_root + "/data/current_bluebikes_stations.csv")
    trips = pd.read_csv(project_root + "/data/trip_data.csv")

if __name__ == "__main__":
    main()