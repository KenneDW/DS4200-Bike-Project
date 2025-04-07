import os
import pandas as pd

def main():

    current_file = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(current_file, "../../"))

    april = pd.read_csv(project_root + "/data/202404-bluebikes-tripdata.csv")
    september = pd.read_csv(project_root + "/data/202409-bluebikes-tripdata.csv")
    december = pd.read_csv(project_root + "/data/202412-bluebikes-tripdata.csv")

    start_april = april[april["start_station_name"] == "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"]
    end_april = april[april["end_station_name"] == "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"]
    start_september = september[september["start_station_name"] == "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"]
    end_september = september[september["end_station_name"] == "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"]
    start_december = december[december["start_station_name"] == "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"]
    end_december = december[december["end_station_name"] == "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"]

    df_final = pd.concat([start_april, start_september, start_december, end_april, end_september, end_december],
                         ignore_index = True)

    df_final = df_final.dropna()



    df_final["started_at"] = pd.to_datetime(df_final["started_at"], format = "ISO8601")
    df_final["ended_at"] = pd.to_datetime(df_final["ended_at"], format = "ISO8601")
    print(df_final.dtypes)


    df_final["duration"] = (df_final["ended_at"] - df_final["started_at"]).dt.total_seconds() / 60


    df_final.to_csv(project_root + "/data/trip_data.csv", index = False)

if __name__ == "__main__":
    main()

