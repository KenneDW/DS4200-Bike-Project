"""
This script when run creates and saves all the figures embedded in our project webpage
"""

import altair as alt
import pandas as pd
import geopandas as gpd
import os



def main():
    current_file = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(current_file, "../../"))
    stations = pd.read_csv(project_root + "/data/current_bluebikes_stations.csv")
    trips = pd.read_csv(project_root + "/data/trip_data.csv")

    box_category_selection = alt.binding_select(options=["rideable_type", "member_casual"], name="Group By: ")
    selection = alt.selection_point(fields = ['xvar'], bind = box_category_selection, value=[{"xvar": "rideable_type"}])

    # Create a box plot
    box_plot = alt.Chart(trips).mark_boxplot().encode(
        x=alt.X('xvar:N', title="Selected Category").scale(domain=list(trips.columns)),
        y=alt.Y('value:Q', title="Value"),
    ).add_params(selection).transform_calculate(
        xvar="datum[selection.xvar]"
    )

    # box_plot.save("box.html")


if __name__ == "__main__":
    main()