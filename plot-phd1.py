"""
Visualize phd.1 files from Sanger sequencing
color code to show low quality bases
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

def parse_phd1(file):
    """Parse phd.1 file into data frame with 3 columns
    Input:
    file: phd.1 file
    Output:

    """

    read_line = False
    rows = []

    with open(file) as f:
        for line in f:
            line = line.strip()

            if line == "BEGIN_DNA":
                read_line = True
                continue
            elif line == "END_DNA":
                break
            
            if read_line:
                base, v1, v2 = line.split()
                d = {"base":base, "v1":int(v1), "v2":int(v2)}
                rows.append(d)

    df = pd.DataFrame(rows)
    return df

def plot_phd1(df, name, markersize=2):
    """Plot phd.1 quality scores
    Input:
    df: dataframe from parse_phd1()
    name: file name
    markersize: size of dots in plot
    """
    # color the points based on the y-value
    # I used this conditions/choices method from this youtube talk
    # at 12:30 into talk
    # https://www.youtube.com/watch?v=nxWginnBklU
    # note that if multiple conditions are met - the first one is used, so
    # if > 50 that will be used and not the others
    conditions = [
        df.v1 > 50, 
        df.v1 > 40,
        df.v1 > 30,
        df.v1 > 20,
        df.v1 > 10, 
    ]
    choices = ["black", "purple", "blue", "green", "orange"]

    df["colors"] = np.select(conditions, choices, default="red")
    fig, ax = plt.subplots()
    yvals = df.v1.values
    xvals = range(len(yvals))
    colors = df.colors
    ax.scatter(xvals, yvals, s=markersize, color=colors)
    ax.set_title(name)
    ax.set_ylim(0,65)

p = Path(".")

for file in p.glob("*.phd.1"):
    df = parse_phd1(file)
    plot_phd1(df, file)

    
