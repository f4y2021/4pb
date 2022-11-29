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

st.set_page_config(page_title="4-Point Bending",page_icon="⏩")

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
    ('2 x ETXL400 + 2x UNIE300 in each skin', '2 x ETXL400 + 2x ETXL400-cross in each skin', '4x ETXL 400 cross in each skin'))

joint_option = st.select_slider(
    '',
    options=['Homogeneous Panel', 'With 0.3mm Adhesive Thickness', 'With 1mm Adhesive Thickness'], value='With 0.3mm Adhesive Thickness')


strain_option = st.radio(
    "Select Strain Direction",
    ['exx', 'eyy', 'exy'])

full_option = st.select_slider(
    '',
    options=['Full Sample', 'Detail Between Top Supports'])


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

vid_select_number=3

for index, row in df1.iterrows():
    if row['Laminate']==laminate_option:
        if row['Connection']==joint_option:
            if row['DIC Area']==full_option:
                vid_select_number=row['Sample Number']
                
              

vid_select='./Videos/sample' + str(vid_select_number)+'_'+str(strain_option)+'.mp4'

graph_select='./Plots/sample'+str(vid_select_number)

if st.button('Plot Force - Displacement Graph for this sample'):

    df1_instron = pd.read_csv(graph_select,sep=",",usecols= [1,2], names=["Displacement","Force"],header=1)
    
    
    fig = px.scatter(df1_instron, x='Displacement (mm)', y='Force (N)', marginal_y="box",
           marginal_x="box",template="ggplot2")
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

st.video(vid_select, format="video/mp4", start_time=0)
