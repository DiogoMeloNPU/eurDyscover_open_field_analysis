import streamlit as stl #be mindful of using st for streamlit and scipy.stats
import pandas as pd

stl.title('TEST')

dystoniaFilesDFpath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.csv"

df=pd.read_csv(dystoniaFilesDFpath)

stl.table(df)
