import streamlit as st
import time
import pandas as pd
import numpy as np

st.title("Gmail Analysis")

st.image("https://lh3.googleusercontent.com/yuUrDV2DAtBRvItHZ2FvXMkPbHR5NEt4kXbpp8dgK-r9jI9-irP19GJb2CvdBRYmy41KG4BxFu2Hod9GzdgGc46iYmm7As4bNNsc-JP7vYwY8d1BzHgZdvKR7H4xtLM20zR9gn0PJE-nQU0navp9Xh0pHc3Cp-CjYUENN7dWZ3NJiw8CiHFEJn7Mc0ul_A")

#Sidebar
st.sidebar.title("Analyse Your Email")
st.sidebar.button("Click")
st.sidebar.multiselect('Select One Option', ['Generate Word Cloud', 'Sentiment Analysis & Summary'])

#Container
container = st.container()
container.write("This is inside a container")
