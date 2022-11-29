"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import streamlit as st

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import re
import sys

st.set_page_config(page_title="4-Point Bending",page_icon="📈") # Set Page Title and Icon

m = st.markdown("""
<style>
div.stButton > button:first-child {
    font-size:16px;font-weight:bold;height:2em;width:7em;
}
</style>""", unsafe_allow_html=True)

st.image('logo_inegi_big.png')
st.title('4-Point Bending: Sandwich Panels')

laminate_option = st.selectbox(
    'Select Laminate',
    ('2 x ETXL400 + 2x UNIE300 in each skin', '2 x ETXL400 + 2x ETXL400-cross in each skin', '4x ETXL 400 cross in each skin')) #Select of the 3 available laminates

joint_option = st.select_slider(
    '',
    options=['Homogeneous Panel', 'With 0.3mm Adhesive Thickness', 'With 1mm Adhesive Thickness'], value='With 0.3mm Adhesive Thickness') #Select of the 3 types of connection

strain_option = st.radio(
    "Select Strain Direction",
    ['exx', 'eyy', 'exy']) #Select Strain Direction

full_option = st.select_slider(
    '',
    options=['Full Sample', 'Detail Between Top Supports']) #Select DIC Field of View

#Compose Sample ID Reference Matrix
Sample_Number = ['1','2','3','4','5','6','7','8']

Laminate = ['2 x ETXL400 + 2x ETXL400-cross in each skin',
'4x ETXL 400 cross in each skin',
'4x ETXL 400 cross in each skin',
'2 x ETXL400 + 2x ETXL400-cross in each skin',
'4x ETXL 400 cross in each skin',
'2 x ETXL400 + 2x UNIE300 in each skin',
'4x ETXL 400 cross in each skin',
'2 x ETXL400 + 2x UNIE300 in each skin']

Connection = ['With 0.3mm Adhesive Thickness',
'With 0.3mm Adhesive Thickness',
'With 0.3mm Adhesive Thickness',
'With 0.3mm Adhesive Thickness',
'With 1mm Adhesive Thickness',
'With 1mm Adhesive Thickness',
'With 1mm Adhesive Thickness',
'With 1mm Adhesive Thickness']

DIC_Area = ['Detail Between Top Supports',
'Detail Between Top Supports',
'Full Sample',
'Full Sample',
'Full Sample',
'Full Sample',
'Detail Between Top Supports',
'Detail Between Top Supports']

df1 = pd.DataFrame(list(zip(Sample_Number, Laminate, Connection,DIC_Area)))
df1.columns = ['Sample Number', 'Laminate', 'Connection','DIC Area']
#Compose Sample ID reference matrix

vid_select_number=3 #Initiate variable to existant video

for index, row in df1.iterrows(): #match current selection with reference matrix
    if row['Laminate']==laminate_option:
        if row['Connection']==joint_option:
            if row['DIC Area']==full_option:
                vid_select_number=row['Sample Number']

 
vid_select='./Videos/sample' + str(vid_select_number)+'_'+str(strain_option)+'.mp4' #compose video file directory

graph_select='./Plots/sample'+str(vid_select_number)+'.csv' #compose plot csv file directory

st.video(vid_select, format="video/mp4", start_time=0) #play video



if st.button('Plot'): #give option to plot csv file

    df1_instron = pd.read_csv(graph_select,sep=",",usecols= [1,2], names=["Displacement (mm)","Force (N)"],header=1) #read csv file


    fig = px.scatter(df1_instron, x='Displacement (mm)', y='Force (N)', template="seaborn") #plot csv file

    fig.update_layout(
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 500,
            tickformat = '.2f'
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
#st.write(vid_select)


