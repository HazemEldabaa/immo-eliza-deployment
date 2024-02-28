import streamlit as st
import requests
import folium 
from streamlit_folium import folium_static
#Define the URL of the FastAPI endpoint
FASTAPI_URL = 'https://immo-eliza-deployment-15s3.onrender.com/predict'  # Update with your FastAPI endpoint URL

#Streamlit App Title
st.title('Price Prediction Web App')

#Image
#st.image('streamlit', caption='Streamlit Logo', use_column_width=True)

#Input features for price prediction
st.header('Enter Features for Prediction')
equipped_kitchen=st.selectbox("Pick kitchen type",['USA_UNINSTALLED','USA_SEMI_EQUIPPED',
                                               'USA_INSTALLED', 'NOT_INSTALLED', 'USA_HYPER_EQUIPPED',
                                               'SEMI_EQUIPPED', 'HYPER_EQUIPPED', 'INSTALLED', 'MISSING'])
nbr_frontages = st.number_input('Number of Frontages:', min_value=0, max_value=10, value=1)
fl_terrace = st.selectbox('Terrace ?:',  [0, 1])
fl_garden = st.selectbox('Garden ?:',  [0, 1])
fl_swimming_pool = st.selectbox('Swimming pool ?:',  [0, 1])
property_type=st.selectbox("Pick property type",['House','appartement'])
# Initial coordinates for Brussels
st.title("Dynamic Map with Click Event")

if 'latitude' not in st.session_state:
    st.session_state.latitude = None

if 'longitude' not in st.session_state:
    st.session_state.longitude = None

m = folium.Map(location=[51.509865, -0.118092], zoom_start=12)

# Use folium_static to embed the Folium map in Streamlit
folium_static(m, width=800, height=600)

# Streamlit script to capture click events and deploy marker
st.markdown("""
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const map = document.querySelector(".folium-map");
            map.addEventListener("click", function(e) {
                const lat = e.latlng.lat.toFixed(6);
                const lng = e.latlng.lng.toFixed(6);
                console.log("Latitude:", lat, "Longitude:", lng);
                
                // Add a marker to the Folium map
                const marker = L.marker([lat, lng]).addTo(map);
                marker.bindPopup(`Latitude: ${lat}<br>Longitude: ${lng}`).openPopup();
                
                // Save latitude and longitude to Streamlit session state
                Streamlit.setComponentValue({latitude: lat, longitude: lng});
            });
        });
    </script>
""", unsafe_allow_html=True)
longitude = st.session_state.longitude
latitude = st.session_state.latitude
region=st.selectbox("Pick region",["Flanders","Wallonia","Brussels-Capital"])
province = st.selectbox('Province', [
    "West Flanders",
    "Antwerp",
    "East Flanders",
    "Hainaut",
    "Brussels",
    "Liège",
    "Flemish Brabant",
    "Limburg",
    "Walloon Brabant",
    "Namur",
    "Luxembourg",
    "MISSING"
])
heating_type = st.selectbox('Type of heating:', [
    "GAS",
    "MISSING",
    "FUELOIL",
    "ELECTRIC",
    "PELLET",
    "WOOD",
    "SOLAR",
    "CARBON"
])
state_building = st.selectbox('State of building:', [
    "MISSING",
    "GOOD",
    "AS_NEW",
    "TO_RENOVATE",
    "TO_BE_DONE_UP",
    "JUST_RENOVATED",
    "TO_RESTORE"
])

epc = st.selectbox('EPC:', [
    "MISSING",
    "B",
    "C",
    "D",
    "A",
    "F",
    "E",
    "G",
    "A+",
    "A++"
])
subproperty_type = st.selectbox('Select type of subproperty:',[
    "HOUSE",
    "APARTMENT",
    "VILLA",
    "GROUND_FLOOR",
    "APARTMENT_BLOCK",
    "MIXED_USE_BUILDING",
    "PENTHOUSE",
    "DUPLEX",
    "FLAT_STUDIO",
    "EXCEPTIONAL_PROPERTY",
    "TOWN_HOUSE",
    "SERVICE_FLAT",
    "MANSION",
    "BUNGALOW",
    "KOT",
    "LOFT",
    "FARMHOUSE",
    "COUNTRY_COTTAGE",
    "MANOR_HOUSE",
    "TRIPLEX",
    "OTHER_PROPERTY",
    "CHALET",
    "CASTLE"
])
nbr_bedrooms = st.number_input('Number of Bedrooms:', min_value=0, max_value=10, value=1)
surface_area = st.number_input('Surface Area (sqm):', min_value=0.0, step=10.0)
garden_sqm = st.number_input('Garden Area (sqm):', min_value=0.0, step=10.0)
total_area_sqm = st.number_input('Living Area (sqm):', min_value=0.0, step=10.0)
surface_land_sqm = st.number_input('Plot Area (sqm):', min_value=0.0, step=10.0)
terrace_sqm = st.number_input('Terrace Area (sqm):', min_value=0.0, step=2.0)


locality = st.selectbox('Locality:', [
    "Brussels",
    "Antwerp",
    "Liège",
    "Brugge",
    "Halle-Vilvoorde",
    "Gent",
    "Turnhout",
    "Leuven",
    "Nivelles",
    "Oostend",
    "Aalst",
    "Charleroi",
    "Kortrijk",
    "Hasselt",
    "Namur",
    "Mechelen",
    "Sint-Niklaas",
    "Mons",
    "Veurne",
    "Dendermonde",
    "Verviers",
    "Tournai",
    "Oudenaarde",
    "Soignies",
    "Thuin",
    "Mouscron",
    "Dinant",
    "Tongeren",
    "Maaseik",
    "Ath",
    "Huy",
    "Marche-en-Famenne",
    "Waremme",
    "Neufchâteau",
    "Arlon",
    "Diksmuide",
    "Virton",
    "Bastogne",
    "Philippeville",
    "Roeselare",
    "Eeklo",
    "Tielt",
    "Ieper",
    "MISSING"
])




#Button to trigger prediction
if st.button('Predict Price'):
    # Prepare input data as JSON
    input_data = {
  "nbr_frontages": nbr_frontages,
  "equipped_kitchen": equipped_kitchen,
  "nbr_bedrooms": nbr_bedrooms,
  "latitude": latitude,
  "longitude": longitude,
  "total_area_sqm": total_area_sqm,
  "surface_land_sqm": surface_land_sqm,
  "terrace_sqm": terrace_sqm,
  "garden_sqm": garden_sqm,
  "province": province,
  "heating_type": heating_type,
  "state_building": state_building,
  "property_type": property_type,
  "epc": epc,
  "locality": locality,
  "subproperty_type": subproperty_type,
  "region": region,
  "fl_terrace": fl_terrace,
  "fl_garden": fl_garden,
  "fl_swimming_pool": fl_swimming_pool
}




    # Make POST request to FastAPI endpoint
    try:
        response = requests.post(FASTAPI_URL, json=input_data)
        if response.status_code == 200:
            predicted_price = response.json()[0]
            st.success(f'Predicted Price: €{predicted_price:.2f}')
        else:
            st.error('Failed to get prediction. Please try again.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
