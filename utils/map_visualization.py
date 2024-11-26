DATA_PATH = "C:/Users/ellio/OneDrive - Queen's University/Queen's/4th year fall/493/map_data"

# Import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib.patches import Patch, Circle

import warnings
warnings.filterwarnings("ignore")
import random

def get_state_code(state_name):
    """
    Returns the code for a given state name.

    Parameters:
        state_name (str): The name of the state (case insensitive).

    Returns:
        str: The state code if found, otherwise 'State not found'.
    """
    state_codes = {
        "ALABAMA": "01",
        "ALASKA": "02",
        "ARIZONA": "04",
        "ARKANSAS": "05",
        "CALIFORNIA": "06",
        "COLORADO": "08",
        "CONNECTICUT": "09",
        "DELAWARE": "10",
        "DISTRICT OF COLUMBIA": "11",
        "FLORIDA": "12",
        "GEORGIA": "13",
        "HAWAII": "15",
        "IDAHO": "16",
        "ILLINOIS": "17",
        "INDIANA": "18",
        "IOWA": "19",
        "KANSAS": "20",
        "KENTUCKY": "21",
        "LOUISIANA": "22",
        "MAINE": "23",
        "MARYLAND": "24",
        "MASSACHUSETTS": "25",
        "MICHIGAN": "26",
        "MINNESOTA": "27",
        "MISSISSIPPI": "28",
        "MISSOURI": "29",
        "MONTANA": "30",
        "NEBRASKA": "31",
        "NEVADA": "32",
        "NEW HAMPSHIRE": "33",
        "NEW JERSEY": "34",
        "NEW MEXICO": "35",
        "NEW YORK": "36",
        "NORTH CAROLINA": "37",
        "NORTH DAKOTA": "38",
        "OHIO": "39",
        "OKLAHOMA": "40",
        "OREGON": "41",
        "PENNSYLVANIA": "42",
        "RHODE ISLAND": "44",
        "SOUTH CAROLINA": "45",
        "SOUTH DAKOTA": "46",
        "TENNESSEE": "47",
        "TEXAS": "48",
        "UTAH": "49",
        "VERMONT": "50",
        "VIRGINIA": "51",
        "WASHINGTON": "53",
        "WEST VIRGINIA": "54",
        "WISCONSIN": "55",
        "WYOMING": "56"
    }
    
    state_name = state_name.upper()
    return state_codes.get(state_name, "State not found")


def visualize_state_opinions(graph,state_names=None,image_size=18,title_size=32,legend_size=20,annotation_size=15):

    edge_color = "#30011E"
    background_color = "#fafafa"

    data_breaks = [
        (0.90, "#E20E0E", "90-100% Republican"),   # Dark red
        (0.70, "#E45757", "70-90% Republican"),              # Medium red
        (0.55, "#E7A0A0", "55-70% Republican"),              # Light red
        (0.45, "#E9E9E9", "Even Split +- 5%"),              # Grey (middle range)
        (0.30, "#A3A1E6", "55-70% Democratic"),              # Light blue
        (0.10, "#5E59E4", "70-90% Democratic"),              # Medium blue
        (0.0,  "#1811E1", "90-100% Democratic")   # Dark blue
    ]

    #Function to set the value for each county
    def create_color(county_df, data_breaks):
        colors = []

        for i, row in county_df.iterrows():
            if row['STATEFP']+row['COUNTYFP'] in graph.nodes.keys():
                for p, c, _ in data_breaks:
                    node = graph.nodes[row['STATEFP']+row['COUNTYFP']]
                    if node.red+node.blue <= 0:
                        print(f"{row['STATEFP']+row['COUNTYFP']} has zero red and blue balls")
                        colors.append("#27d618")
                        break
                    # if sum(node.red)/(sum(node.red)+sum(node.blue)) >= p:
                    #     colors.append(c)
                    #     break
                    if node.red/(node.red+node.blue) >= p:
                        colors.append(c)
                        break
            
            else:
                print(f"{row['STATEFP']+row['COUNTYFP']} not in graph, but in map data")
                colors.append("#EBCC34")

        return colors

    def add_title(state_names):
        if state_names is None:
            plt.annotate(
                text="Political Opinions by County for",
                xy=(0.5, 1.1), xycoords="axes fraction", fontsize=annotation_size, ha="center"
            )

            plt.annotate(
                text=f"The United States of America", 
                xy=(0.5, 1.03), xycoords="axes fraction", fontsize=title_size, ha="center",
                fontweight="bold"
            )
        elif len(state_names) == 1:
            plt.annotate(
                text="Political Opinions by County for the state of",
                xy=(0.5, 1.1), xycoords="axes fraction", fontsize=annotation_size, ha="center"
            )

            plt.annotate(
                text=f"{state_names[0]}", 
                xy=(0.5, 1.03), xycoords="axes fraction", fontsize=title_size, ha="center",
                fontweight="bold"
            )

        elif len(state_names) > 1:
            plt.annotate(
                text="Political Opinions by County for the states of",
                xy=(0.5, 1.1), xycoords="axes fraction", fontsize=annotation_size, ha="center"
            )
            text = ""
            for i in range(len(state_names)-1):
                text = text + state_names[i] + ", "
            text = text + state_names[len(state_names)-1]
            plt.annotate(
                text=text,
                xy=(0.5, 1.03), xycoords="axes fraction", fontsize=title_size, ha="center",
                fontweight="bold"
            )

    def add_legend(data_breaks):
        patches = [Patch(facecolor=c, edgecolor=edge_color, label=t) for _, c, t in data_breaks]

        leg = plt.legend(
            handles=patches,
            bbox_to_anchor=(0.5, -0.03), loc='center',
            ncol=4, fontsize=legend_size, columnspacing=1,
            handlelength=1, handleheight=1,
            edgecolor=background_color,
            handletextpad=0.4
        )

    def add_information():
        plt.annotate(
            "The Polya Network Process Involves removing a ball from an urn's super urn and\n replacing a set number of balls back into its urn of that color (...)",
            xy=(0.5, -0.08), xycoords="axes fraction", ha="center", va="top", fontsize=annotation_size, linespacing=1.8
        )

        # plt.annotate(
        #     "Source: https://dataforgood.facebook.com/", 
        #     xy=(0.5, -0.22), xycoords="axes fraction", fontsize=16, ha="center",
        #     fontweight="bold"
        # )

    def translate_geometries(df, x, y, scale, rotate):
        df.loc[:, "geometry"] = df.geometry.translate(yoff=y, xoff=x)
        center = df.dissolve().centroid.iloc[0]
        df.loc[:, "geometry"] = df.geometry.scale(xfact=scale, yfact=scale, origin=center)
        df.loc[:, "geometry"] = df.geometry.rotate(rotate, origin=center)
        return df

    def adjust_maps(df):
        df_main_land = df[~df.STATEFP.isin(["02", "15"])]
        df_alaska = df[df.STATEFP == "02"]
        df_hawaii = df[df.STATEFP == "15"]

        df_alaska = translate_geometries(df_alaska, 1300000, -4900000, 0.5, 32)
        df_hawaii = translate_geometries(df_hawaii, 5400000, -1500000, 1, 24)

        return pd.concat([df_main_land, df_alaska, df_hawaii])

    sns.set_style({
        "font.family": "serif",
        "figure.facecolor": background_color,
        "axes.facecolor": background_color,
    })

    if state_names is not None:
        state_codes = [get_state_code(s) for s in state_names]

    # Load and prepare geo-data, remove states we don't care about
    counties = gpd.read_file(DATA_PATH + "/tl_2020_us_county/")
    if state_names is not None:
        counties = counties[counties.STATEFP.isin(state_codes)]
    else:
        counties = counties[~counties.STATEFP.isin(["72", "69", "60", "66", "78"])]
    counties = counties.set_index("GEOID")

    states = gpd.read_file(DATA_PATH + "/tl_2020_us_state/")
    if state_names is not None:
        states = states[states.STATEFP.isin(state_codes)]
    else:
        states = states[~states.STATEFP.isin(["72", "69", "60", "66", "78"])]

    counties = counties.to_crs("ESRI:102003")
    states = states.to_crs("ESRI:102003")

    if state_names is None:
        counties = adjust_maps(counties)
        states = adjust_maps(states)    

    counties.loc[:, "color"] = create_color(counties, data_breaks)
    ax = counties.plot(edgecolor=edge_color + "55", color=counties.color, figsize=(image_size, image_size))
    states.plot(ax=ax, edgecolor=edge_color, color="None", linewidth=1)

    add_title(state_names)
    add_legend(data_breaks)
    add_information()

    plt.axis("off")
    #plt.show()
