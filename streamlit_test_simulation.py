import numpy as np
import streamlit as st
import plotly.graph_objects as go
import scipy.stats as stats
import satlas as sat

# ABC = [Al, Au, Bl, Bu, 0, 0]
def model(I, J, centre=0., Fwhm=50., Al=-391.5, Au=-82.2, Bl=-650, Bu=-302):
    ABC = [Al, Au, Bl, Bu, 0, 0]
    centroid = centre
    scale = 100
    fwhm = [Fwhm, Fwhm]
    background = [0]
    basemodel_low1 = sat.HFSModel(I, J, ABC, centroid, fwhm=fwhm, scale=scale, background_params=[10])
    ux = np.linspace(-10000, 10000, 14000)
    u = basemodel_low1(ux)
    return u


def plotdata(res=50.):
    I_even = 0
    J = [3, 2]
    Pd102 = model(I_even, J, 1446.9, res) * 1.02
    Pd104 = model(I_even, J, 954.3, res) * 11.14
    Pd106 = model(I_even, J, 492.9, res) * 27.33
    Pd108 = model(I_even, J, 0., res) * 26.46
    Pd110 = model(I_even, J, -434.6, res) * 11.72
    Pd_even = Pd102 + Pd104 + Pd106 + Pd108 + Pd110
    return Pd_even


def plotdataodd(res=50., Al=-391.5, Au=-82.2, Bl=-650, Bu=-302):
    J = [3, 2]
    I_odd = 5 / 2
    Pd_odd_105 = model(I_odd, J, 836.9, res, Al, Au, Bl, Bu) * 22.33
    return Pd_odd_105


x = np.linspace(-10000, 10000, 14000)
Pd_even = plotdata()
Pd_odd = plotdataodd()

# Initialize the Streamlit app
st.title("Isotope Spectra Visualization")

# Slider for FWHM
fwhm = st.slider("FWHM", 0.1, 3000.0, 50.0)

# Sliders for parameters
Al = st.slider("A_Lower", -600.0, 600.0, -391.5)
Au = st.slider("A_Upper", -600.0, 600.0, -82.2)
Bl = st.slider("B_Lower", -600.0, 600.0, -650.0)
Bu = st.slider("B_Upper", -600.0, 600.0, -302.0)

Pd_even_updated = plotdata(fwhm)
Pd_odd_updated = plotdataodd(fwhm, Al, Au, Bl, Bu)
Pd_total = Pd_even_updated + Pd_odd_updated

# Create the plotly figures
fig_even = go.Figure()
fig_odd = go.Figure()
fig_total = go.Figure()

fig_even.add_trace(go.Scatter(x=x, y=Pd_even_updated, mode="lines", name="Even Isotope Spectra"))
fig_odd.add_trace(go.Scatter(x=x, y=Pd_odd_updated, mode="lines", name="105Pd(Odd) Isotope Spectra"))
fig_total.add_trace(go.Scatter(x=x, y=Pd_total, mode="lines", name="Total Spectra"))

# Update layout
fig_even.update_layout(title="Even Isotope Spectra", xaxis_title="x", yaxis_title="Intensity")
fig_odd.update_layout(title="105Pd(Odd) Isotope Spectra", xaxis_title="x", yaxis_title="Intensity")
fig_total.update_layout(title="Total Spectra", xaxis_title="x", yaxis_title="Intensity")

# Display the plots in Streamlit
st.plotly_chart(fig_even)
st.plotly_chart(fig_odd)
st.plotly_chart(fig_total)
