import streamlit as st

# Conversion functions
def wavelength_to_frequency(wavelength,wavelength_unit, speed_of_light):
    wavelength = convert_to_meters(wavelength, wavelength_unit)
    return speed_of_light / wavelength

def frequency_to_wavelength(frequency,frequency_unit, speed_of_light):
    frequency = convert_to_hertz(frequency, frequency_unit)
    return speed_of_light / frequency

def wavelength_to_wavenumber(wavelength,wavelength_unit):
    wavelength = convert_to_meters(wavelength, wavelength_unit)
    return 1 / wavelength

def wavenumber_to_wavelength(wavenumber,wavenumber_unit):
    wavenumber = convert_to_per_meter(wavenumber, wavenumber_unit)
    return 1 / wavenumber

# Units for each quantity
wavelength_units = ['m', 'cm', 'mm', 'μm', 'nm', 'pm', 'fm']
frequency_units = ['Hz', 'kHz', 'MHz', 'GHz', 'THz']
wavenumber_units = ['1/m', '1/cm', '1/mm', '1/μm', '1/nm']
speed_of_light_options = {
    'Air': 299792458,  # Speed of light in air
    'Vacuum': 299792458e6  # Speed of light in vacuum (scaled for convenience)
}
anti_conversion_factors = {
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'μm': 1e-6,
        'nm': 1e-9,
        'pm': 1e-12,
        'fm': 1e-15,
        'Hz': 1,
        'kHz': 1e-3,
        'MHz': 1e-6,
        'GHz': 1e-9,
        'THz': 1e-12,
        '1/m': 1,
        '1/cm': 1e2,
        '1/mm': 1e3,
        '1/μm': 1e6,
        '1/nm': 1e9

    }

def convert_to_meters(value, unit):
    conversion_factors = {
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'μm': 1e-6,
        'nm': 1e-9,
        'pm': 1e-12,
        'fm': 1e-15
    }
    return value * conversion_factors[unit]

def convert_to_hertz(value, unit):
    conversion_factors = {
        'Hz': 1,
        'kHz': 1e3,
        'MHz': 1e6,
        'GHz': 1e9,
        'THz': 1e12
    }
    return value * conversion_factors[unit]

def convert_to_per_meter(value, unit):
    conversion_factors = {
        '1/m': 1,
        '1/cm': 1e2,
        '1/mm': 1e3,
        '1/μm': 1e6,
        '1/nm': 1e9
    }
    return value * conversion_factors[unit]

def convert_quantities(wavelength, wavelength_unit, frequency, frequency_unit, wavenumber, wavenumber_unit, speed_of_light):
    if wavelength:
        wavelength = float(wavelength)
        frequency = wavelength_to_frequency(wavelength, wavelength_unit, speed_of_light)
        wavenumber = wavelength_to_wavenumber(wavelength, wavelength_unit)
    elif frequency:
        frequency = float(frequency)
        wavelength = frequency_to_wavelength(frequency, frequency_unit, speed_of_light)
        wavenumber = wavelength_to_wavenumber(wavelength, wavelength_unit)
    elif wavenumber:
        wavenumber = float(wavenumber)
        wavelength = wavenumber_to_wavelength(wavenumber, wavenumber_unit)
        frequency = wavelength_to_frequency(wavelength, wavelength_unit, speed_of_light)

    return wavelength, frequency, wavenumber
def doppler_correction(mass, laser, Vs, Vc):
    mass=float(mass)*931494102.42
    laser=2*float(laser)*2.99792458*1e10
    volt=float(Vc)-float(Vs)+15
    a=volt/mass
    c=(1+a+((2*a)+a**2)**0.5)
    cor_laser=laser*c
    return cor_laser,c,a
# Streamlit app
def main():
    st.title("Conversion Calculator")

    col1, col2, col3 = st.columns(3) 
    
    with col1:
        wavelength = st.text_input("Wavelength")
        wavelength_unit = st.selectbox("Wavelength Unit", wavelength_units)
    
    with col2:
        frequency = st.text_input("Frequency")
        frequency_unit = st.selectbox("Frequency Unit", frequency_units)
    
    with col3:
        wavenumber = st.text_input("Wavenumber")
        wavenumber_unit = st.selectbox("Wavenumber Unit", wavenumber_units)
    
    speed_of_light_option = st.radio("Speed of Light", ('Air', 'Vacuum'))
    speed_of_light = speed_of_light_options[speed_of_light_option]
    
    # Perform the conversions
    if st.button("Enter"):
        converted_wavelength_value, converted_frequency_value, converted_wavenumber_value = convert_quantities(
            wavelength,wavelength_unit, frequency,frequency_unit, wavenumber,wavenumber_unit, speed_of_light
        )
    else:
        converted_wavelength_value = 0
        converted_frequency_value = 0
        converted_wavenumber_value = 0
    
    st.write("Converted Results:")
    converted_wavelength, converted_frequency, converted_wavenumber = st.columns(3)
    converted_wavelength.text_input("Wavelength Result", value=str(float(converted_wavelength_value)*anti_conversion_factors[wavelength_unit]))
    converted_frequency.text_input("Frequency Result", value=str(float(converted_frequency_value)*anti_conversion_factors[frequency_unit]))
    converted_wavenumber.text_input("Wavenumber Result", value=str(float(converted_wavenumber_value)/anti_conversion_factors[wavenumber_unit]))

    st.title("Doppler calculator")
    mass = st.text_input("Mass of the isotope(in amu)")
    laser=st.text_input("Laser frequncy (in cm-1)(will be doubled)")
    Vs=st.text_input("Scanning Voltage")
    Vc=st.text_input("Cooler Voltage")
    st.write("Doppler corrected frequency:")
    if st.button("Convert"):
        cor_freq=doppler_correction(mass,laser,Vs,Vc)[0]
        C=doppler_correction(mass,laser,Vs,Vc)[1]
        alp=doppler_correction(mass,laser,Vs,Vc)[2]
    else:
        cor_freq=0
        C=0
        alp=0

    st.text_input("Doppler corrected frequency",value=str(cor_freq))
    st.text_input("Doppler factor",value=str(C))
    st.text_input("Alpha",value=str(alp))

def calculate_doppler_corrected_freq(coolervoltage, scanningvoltage, mass, laserwavenumber):
    laserfreq = laserwavenumber * 2.99792458 * 1e10
    alpha = (coolervoltage - scanningvoltage + 15.) / (mass * 931494102.42)
    DopplerCorrectedFreq = laserfreq * (1 + alpha + (2 * alpha + alpha**2)**0.5)
    return DopplerCorrectedFreq

def main1():
    st.title("Doppler Corrected Frequency Calculator")

    coolervoltage = st.number_input("Cooler Voltage (V)", value=0.0)
    scanningvoltage = st.number_input("Scanning Voltage (V)", value=0.0)
    mass = st.number_input("Mass of Isotope (amu)", value=0.0)
    laserwavenumber = st.number_input("Laser Wavenumber (cm-1)", value=0.0)

    if st.button("Calculate"):
        DopplerCorrectedFreq = calculate_doppler_corrected_freq(coolervoltage, scanningvoltage, mass, laserwavenumber)
        st.success(f"The Doppler Corrected Frequency is: {DopplerCorrectedFreq}")
    


if __name__ == "__main__":
    main1()
