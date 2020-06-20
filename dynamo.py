#streamlit run dynamo.py


#______________________________________________________________________________
# NEEDED PACKAGES

import importlib, importlib.machinery
import sys
import io
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import streamlit as st
from PIL import Image
#import plotly.graph_objs as go
#import plotly.express as px
import requests


#_____________________________________________________________________________
# DEFINE PATHS
# Data faile name
csvFile = 'dynamo_USDate.csv' 
# Github path
sourcePath = 'https://raw.githubusercontent.com/joelguglietta/dynamo/master/'

#______________________________________________________________________________
# FUNCTIONS


@st.cache(allow_output_mutation=True)

def load_data(path,csvFile, indexInOut, convertDate):
    url = path+csvFile
    df = pd.read_csv(url, sep =',')
    if indexInOut == 1:
        df = df.reset_index()
    colNames = df.columns 
    colDateName = colNames[0]
    if colDateName !='date':
        df = df.rename(columns={colDateName:'date'})        
    if convertDate == 'object2datetime64':
        df['date'] = pd.to_datetime(df['date'])   
    return  df

def download_image(url):    
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)  
    im = Image.open(io.BytesIO(r.content))
    return im

#______________________________________________________________________________
# STREAMLIT SCRIPT


def main():
    
    # -- Data preparation ----------------------------------------------------
    # Load main data
    df           = load_data(sourcePath,csvFile, 0, 'object2datetime64')
    dynamoDf     = df.copy()
    benchDate_np = df['date'].to_numpy(dtype='datetime64')
    # Retrieve P&L
    dynamo   = dynamoDf['dynamo'].to_numpy()     
    maars    = dynamoDf['maars'].to_numpy() 
    taglom   = dynamoDf['taglom'].to_numpy() 
    # Differet Df for for plotting
    # Dynamo(Maars + Taglom)
    dynamo_web = pd.DataFrame({'date':benchDate_np, 'pl': dynamo})
    dynamo_web = dynamo_web.set_index('date', inplace=False)    
    # Maars, market neutral
    maars_web = pd.DataFrame({'date':benchDate_np, 'pl': maars})
    maars_web = maars_web.set_index('date', inplace=False)
    # Taglo, Macro directional
    taglom_web = pd.DataFrame({'date':benchDate_np, 'pl': taglom})
    taglom_web = taglom_web.set_index('date', inplace=False)
      
    
    # -- Organise web page ----------------------------------------------------
    # Page title     
    st.title("DYNAMO")
    st.write("""**Dynamic Allocation of Macro Operators**""")    
    
    # -- Top (intro) left-Hand Side Column -----------------------------------
    # imageName = "fig_Dynamo.png"
    # imageUrl = sourcePath + imageName
    # image = Image.open(imageUrl)
    # st.sidebar.image(image, caption='', use_column_width=True)
    
    
    imageName = "fig_Dynamo.png"
    urlImage = sourcePath + imageName
    myImage = download_image(urlImage)             
    st.sidebar.image(myImage, caption='', use_column_width=True) 
    
    
    # Short explanation
    st.sidebar.subheader("A global cross-asset quantitative macro portfolio with proven efficiency combining pure market-neutral and directional strategies.")
  
    # -- Model's perfromance at glance ----------------------------------------
    st.sidebar.subheader("Model's performance")
    status = st.sidebar.selectbox("Select a model:",["DYNAMO","Market neutral strategy","Directional strategy"])
    if status == "DYNAMO":
        st.subheader("DYNAMO (Market neutral plus Directional strategies - cumulated returns, %)")
        st.line_chart(dynamo_web.pl)  
    elif status == "Market neutral strategy":
        st.subheader("MAARS (Market neutral strategy - cumulated returns, %)")
        #st.plotly_chart(fig)
        st.line_chart(maars_web.pl)
    elif status == "Directional strategy":  
        st.subheader("TAGLOM (Macro-Directional strategy - cumulated returns, %)")
        #st.plotly_chart(fig)    
        st.line_chart(taglom_web.pl)  
    
    
    # -- Model's presentation ------------------------------------------------
    st.sidebar.subheader("Model's presentation")
    statusPres = st.sidebar.selectbox("Select a theme:",["What is Dynamo?","Describe Dynamo","Model's assumption","Portfolio solution","Mandate", "Tactical Algorithm Factory", "Strategy overview", "Performance analytics", "Relative performance"])  
    
    
    if statusPres == "What is Dynamo?":
        
        st.subheader("**What is Dynamo?** Explore it in navigating through the **Model'spresentation**.")
        
    elif statusPres == "Describe Dynamo": 
        
        textBox = """
        ### Describe Dynamo###
        - **Dynamo ** stands for **Dynamic Allocation of Macro Operators**. It is a global cross-asset (currencies, fixed income, commodity, equity) quantitative macro portfolio.
        - Dynamo combines two main programs: **Maars** (**Macro Arbitrages**, i.e. a market-neutral, long-short program) and **Taglom** (**Trend Agglomeration**, i.e. macro-directional).
        - Dynamo is made up with more than 100 kernels, i.e. sub-models (some using machine learning technologies). Market-neutral kernels are the components of Maars, directional kernels are those of Taglom.
        - A Bayesian robust portfolio optimizer allocates capital dynamically across the different kernels.
        - Dynamo invests in nearly 100 instruments across developed and emerging markets.
        ---------------------
    """      
        st.markdown(textBox) 
    

    elif statusPres == "Model's assumption":
        imageName = "fig_Assumption.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage) 
        st.subheader("Model's'assumption")   
        st.image(myImage, use_column_width=True)
        
    elif statusPres == "Portfolio solution":
        imageName = "fig_PtfSolution.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage)  
        st.subheader("Portfolio solution")               
        st.image(myImage, use_column_width=True) 
        
    elif statusPres == "Mandate":
        imageName = "fig_Mandate.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage)
        #myImage = Image.open(urlImage)      
        st.subheader("Mandate")        
        st.image(myImage, use_column_width=True)              
        
    elif statusPres == "Tactical Algorithm Factory":
        imageName = "fig_TAF.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage)   
        st.subheader("Tactical Algorithm Factory")             
        st.image(myImage, use_column_width=True)        
        
    elif statusPres == "Strategy overview":
        imageName = "fig_StratOV.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage)   
        st.subheader("Strategy overview")                       
        st.image(myImage, use_column_width=True)        
        
    elif statusPres == "Performance analytics":
        imageName = "fig_PerfSnap.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage)    
        st.subheader("Performance analytics")              
        st.image(myImage, use_column_width=True)        
        
    elif statusPres == "Relative performance":
        imageName = "fig_OutPerf.png"
        urlImage = sourcePath + imageName
        myImage = download_image(urlImage)  
        st.subheader("Relative performance")                               
        st.image(myImage, use_column_width=True)    
    
    # -- AuthoR ---------------------------------------------------------------   
    st.sidebar.subheader("About Author")
    text = """[**Linkedin**](https://www.linkedin.com/in/joel-guglietta-977a5337/)
      """
    st.sidebar.markdown(text)
    

if __name__ == "__main__":
    main()
