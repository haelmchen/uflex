import pandas as pd
import matplotlib as plt
import plotly.express as px
import streamlit as st
import numpy as np
import seaborn as sns
from io import StringIO


# ---- Titel ----
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Yieldverteilung",
    page_icon=":bar_chart:",
    layout="wide"
)


# ---- Datei Abfrage ----
uploaded_file = st.file_uploader("Choose a file")


# ---- Datei Auslesen
# Abfrage per 'uploaded_file', feste Datei per io=
df = pd.read_excel(uploaded_file,
#    io='m5115.xlsx',
    engine="openpyxl"
    )

# ---- blanken Input darstellen
#st.dataframe(df)


# ---- SIDEBAR ----
# -----------------
# ---- Dateiname darstellen ----
if uploaded_file:
    st.write("Filename: ", uploaded_file.name)
# ---- Sidebar Titel ----
st.sidebar.header("Please Filter Here:")

# ---- Multiselect ----
equipment = st.sidebar.multiselect(
    "Select the Equipment:",
    options=df.sort_values(by="Equipment")["Equipment"].unique(),
    default=df.sort_values(by="Equipment")["Equipment"].unique()
)
pcid = st.sidebar.multiselect(
    "Select the PC:",
    options=df.sort_values(by="PCID")["PCID"].unique(),
    default=df.sort_values(by="PCID")["PCID"].unique()
)
testmode = st.sidebar.multiselect(
    "Select the testmode:",
    options=df.sort_values(by="Testmode")["Testmode"].unique(),
    default=df.sort_values(by="Testmode")["Testmode"].unique()
)
# ---- Input auf Selektion begrenzen ----
df_selection = df.query(
    "Equipment == @equipment & PCID ==@pcid & Testmode == @testmode"
)

# ---- Datenselektion darstellen ----
#st.dataframe(df_selection)


# ---- MAINPAGE ----
# ------------------
# ---- Titel ----
st.title(":bar_chart: Yieldverteilung")
st.markdown("##")

# ---- Übersicht ----
pcyield = round(df_selection["PC_YIELD_ALL"].median(),4)
anzahl = len(df_selection["PC_YIELD_ALL"]) + 1
cards = df_selection["PCID"].nunique()
tester = df_selection["Equipment"].nunique()

# ---- Spalten für Übersicht ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Yield:")
    st.subheader(f"{pcyield:,}")
with col2:
    st.subheader("Anzahl:")
    st.subheader(f"{anzahl:,}")
with col3:
    st.subheader("Karten:")
    st.subheader(f"{cards:,}")
with col4:
    st.subheader("Tester:")
    st.subheader(f"{tester:,}")

# ---- Abgrenzung ----
st.markdown("""---""")

#Heatmap 1

df_median = df_selection.groupby(['PCID','Equipment']).median().round(2).reset_index(drop=False)
df_anzahl = df_selection.groupby(['PCID','Equipment']).size().reset_index(drop=False,name='counts')
#df_median = df_median.reset_index(drop=False)
array = df_median.pivot_table(index='PCID',columns='Equipment',values='PC_YIELD_ALL')
array2 = df_anzahl.pivot_table(index='PCID',columns='Equipment',values='counts')
array3 = array * array2


#fig1 = plt.figure(figsize=(20,15))
#ax1 = plt.subplot2grid((20,20), (0,0), colspan=19, rowspan=19)
#ax4 = plt.subplot2grid((20,20), (19,0), colspan=19, rowspan=1)
#ax5 = plt.subplot2grid((20,20), (0,19), colspan=1, rowspan=19)
#
#sns.heatmap(array, ax=ax1, annot=True, cmap="YlGnBu", linecolor='b', cbar = False)
#ax1.xaxis.tick_top()
#ax1.set_xticklabels(array.columns,rotation=90)
#ax4.set_ylabel('')    
#ax4.set_xlabel('')
#ax5.set_ylabel('')    
#ax5.set_xlabel('')
#
#sns.heatmap((pd.DataFrame(array.mean(axis=0))).transpose(), ax=ax4, annot=True, cmap="YlGnBu", cbar=False, xticklabels=False, yticklabels=False)
#sns.heatmap(pd.DataFrame(array.mean(axis=1)), ax=ax5, annot=True, cmap="YlGnBu", cbar=False, xticklabels=False, yticklabels=False)


fig, ax = plt.subplots(figsize=(20,15))
ax = sns.heatmap(
    array, 
    annot=True, 
    annot_kws={"size": 10}, 
    fmt=".2f",
    linewidth=.5, 
    cmap='RdYlGn', 
    vmin=0.8, 
    vmax=1)

fig2, ax2 = plt.subplots(figsize=(20,15))
ax2 = sns.heatmap(
    array2, 
    annot=True, 
    annot_kws={"size": 10}, 
    fmt=".0f",
    linewidth=.5, 
    cmap='RdYlGn', 
    vmin=1, 
    vmax=300)

fig3, ax3 = plt.subplots(figsize=(20,15))
ax3 = sns.heatmap(
    array3, 
    annot=True, 
    annot_kws={"size": 10}, 
    fmt=".0f",
    linewidth=.5, 
    cmap='RdYlGn', 
    vmin=1, 
    vmax=300)

# Anpassungen
#plt.title("Auswertung",fontsize=18)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax2.xaxis.tick_top()
ax2.xaxis.set_label_position('top')
ax3.xaxis.tick_top()
ax3.xaxis.set_label_position('top') 

# Top 5 

df_toptester = df_median.nlargest(5, ['PC_YIELD_ALL','Equipment'], keep='first')
df_toppc = df_median.nlargest(5, ['PC_YIELD_ALL','PCID'], keep='first')

#Display

col5, col6, col7 = st.columns([2,1,2])
with col5:
    st.subheader("Heatmap")
    tab1, tab2, tab3 = st.tabs(["Yield", "Anzahl","Yield*Anzahl"])
    with tab1:
        fig1 = plt.figure(figsize=(20,15))
        ax1 = plt.subplot2grid((20,20), (0,0), colspan=19, rowspan=19)
        ax2 = plt.subplot2grid((20,20), (19,0), colspan=19, rowspan=1)
        ax3 = plt.subplot2grid((20,20), (0,19), colspan=1, rowspan=19)
        
        ax1.xaxis.tick_top()
        ax1.set_xticklabels(array.columns,rotation=90)
        ax1.xaxis.set_label_position('top')
        ax2.xaxis.tick_top()
        ax3.xaxis.set_label_position('top')        
        sns.heatmap(array, ax=ax1, annot=True, cmap="RdYlGn", fmt=".2f", linecolor='b', cbar = False)
        sns.heatmap((pd.DataFrame(array.mean(axis=0))).transpose(), ax=ax2, annot=True, cmap="RdYlGn", cbar=False, xticklabels=False, yticklabels=False)
        sns.heatmap(pd.DataFrame(array.mean(axis=1)), ax=ax3, annot=True, cmap="RdYlGn", cbar=False, xticklabels=False, yticklabels=False)
        st.pyplot(fig1)
    with tab2:
        fig2 = plt.figure(figsize=(20,15))
        ax1 = plt.subplot2grid((20,20), (0,0), colspan=19, rowspan=19)
        ax2 = plt.subplot2grid((20,20), (19,0), colspan=19, rowspan=1)
        ax3 = plt.subplot2grid((20,20), (0,19), colspan=1, rowspan=19)

        ax1.xaxis.tick_top()
        ax1.set_xticklabels(array.columns,rotation=90)

        sns.heatmap(array2, ax=ax1, annot=True, cmap="RdYlGn", fmt=".2f", linecolor='b', cbar = False)
        sns.heatmap((pd.DataFrame(array2.sum(axis=0))).transpose(), ax=ax2, annot=True, cmap="RdYlGn", fmt=".0f", cbar=False, xticklabels=False, yticklabels=False)
        sns.heatmap(pd.DataFrame(array2.sum(axis=1)), ax=ax3, annot=True, cmap="RdYlGn", fmt=".0f", cbar=False, xticklabels=False, yticklabels=False)
        st.pyplot(fig2)
    with tab3:
        st.pyplot(fig3)

#col6 leer, damit etwas Platz zwischen den Anzeigen ist

with col7:
    st.subheader("TOP 5")
    st.subheader("Tester")
    st.dataframe(df_toptester)
    st.subheader("Probecard")
    st.dataframe(df_toppc)

st.markdown("""---""")

st.header("raw data")
st.dataframe(df)
