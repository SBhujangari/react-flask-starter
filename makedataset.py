import os
from imutils import paths
import shutil
import pandas as pd

"""please see createdataset.md before running this."""

# This assumes your datsets were cloned into the same directory as this makedataset.py file. Change this to the directory of your datasets if this is not the case
workingDirectory = os.path.dirname(os.path.realpath(__file__))
print('working directory:', workingDirectory)
covidPath = os.path.sep.join([f"{workingDirectory}", "COVID-19 Radiography Database", "COVID-19"])
normalPath = os.path.sep.join([f"{workingDirectory}", "COVID-19 Radiography Database", "NORMAL"])


# Combines all COVID images into one singular dataset to make it easier to process
def makeDataset(workingDirectory=workingDirectory):
    print("starting, please be patient. This can take a few minutes. ")
    global covidPath
    global normalPath
    imagePath = os.path.sep.join([f"{workingDirectory}", "covid-chestxray-dataset", "images"])
    fig1ImagePath = os.path.sep.join([f"{workingDirectory}", "Figure1-COVID-chestxray-dataset", "images"])
    actualmedImagePath = os.path.sep.join([f"{workingDirectory}", "Actualmed-COVID-chestxray-dataset", "images"])

    for (index, row) in pd.read_csv(os.path.sep.join([f"{workingDirectory}", "covid-chestxray-dataset", "metadata.csv"])).iterrows():
        if len(row['finding']) < 8:
            continue
        if (row["finding"][-8:] != "COVID-19"):  # Skip everything except if the case is COVID-19
            continue
        singleImagePath = os.path.sep.join([imagePath, row["filename"]])
        if not os.path.exists(singleImagePath):
            print('image not found', singleImagePath)
            continue
        filename = row["filename"].split(os.path.sep)[-1]
        outputPath = os.path.sep.join([f"{covidPath}", filename])
        shutil.copy2(singleImagePath, outputPath)

    for (index, row) in pd.read_csv(os.path.sep.join([f"{workingDirectory}", "covid-chestxray-dataset", "metadata.csv"])).iterrows():
        if len(row['finding']) < 8:
            continue
        if (row["finding"][-8:] != "COVID-19"):  # Skip everything except if the case is COVID-19
            continue
        singleImagePath = os.path.sep.join([imagePath, row["filename"]])
        if not os.path.exists(singleImagePath):
            print('image not found', singleImagePath)
            continue
        filename = row["filename"].split(os.path.sep)[-1]
        outputPath = os.path.sep.join([f"{covidPath}", filename])
        shutil.copy2(singleImagePath, outputPath)

    for (index, row) in pd.read_csv(os.path.sep.join([f"{workingDirectory}", "Figure1-COVID-chestxray-dataset", "metadata.csv"]),encoding="ISO-8859-1").iterrows():
        if row["finding"] != "COVID-19":
            continue
        if os.path.exists(os.path.join(f"{fig1ImagePath}", row["patientid"] + ".jpg")):
            singleImagePath = os.path.sep.join([f"{fig1ImagePath}", row["patientid"] + ".jpg"])
        elif os.path.exists(os.path.join(f"{fig1ImagePath}", row["patientid"] + ".png")):
            singleImagePath = os.path.sep.join([f"{fig1ImagePath}", row["patientid"] + ".png"])
        else:
            print("Some files from the figure1 dataset are missing.")
            continue
        filename = singleImagePath.split(os.path.sep)[-1]
        outputPath = os.path.sep.join([f"{covidPath}", filename])
        shutil.copy2(singleImagePath, outputPath)

    for (index, row) in pd.read_csv(os.path.sep.join([f"{workingDirectory}", "Actualmed-COVID-chestxray-dataset", "metadata.csv"]),encoding="unicode_escape",).iterrows():
        if row["finding"] != "No finding":
            continue
        singleImagePath = os.path.sep.join([actualmedImagePath, row["imagename"]])
        if not os.path.exists(singleImagePath):
            print('image not found')
            continue
        filename = row["imagename"].split(os.path.sep)[-1]
        outputPath = os.path.sep.join([f"{normalPath}", filename])
        shutil.copy2(singleImagePath, outputPath)
    for (index, row) in pd.read_csv(os.path.sep.join([f"{workingDirectory}", "Actualmed-COVID-chestxray-dataset", "metadata.csv"]),encoding="unicode_escape",).iterrows():
        if row["finding"] != "COVID-19":
            continue
        singleImagePath = os.path.sep.join([actualmedImagePath, row["imagename"]])
        if not os.path.exists(singleImagePath):
            continue
        filename = row["imagename"].split(os.path.sep)[-1]
        outputPath = os.path.sep.join([f"{covidPath}", filename])
        shutil.copy2(singleImagePath, outputPath)
    print("finished copying.")
    normalImages = list(paths.list_images(f"{normalPath}"))
    covidImages = list(paths.list_images(f"{covidPath}"))

    print("dataset completed. you may now close this script and begin to train.")
    print("Number of COVID train files:", str(len(covidImages)))
    print("Number of normal train files", str(len(normalImages)))

makeDataset()
