import streamlit as st
import requests
import folium 
from streamlit_folium import folium_static, st_folium
from folium.plugins import Draw
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
st.title("Property Location")

belgium_coords = [50.8503, 4.3517]  # Latitude and Longitude for Brussels, Belgium
m = folium.Map(location=belgium_coords, zoom_start=8)
Draw(export=True).add_to(m)
# Add a marker for Brussels

# Call to render Folium map in Streamlit
st_data = st_folium(m, width=725,draw_options={"polygon": False, "polyline": False, "rectangle": False, "circle": False, "circlemarker": False})
# if st_data is not None and st_data.get("last_clicked") is not None:
#     latitude = st_data["last_clicked"].get("lat")
#     longitude = st_data["last_clicked"].get("lng")

#     if latitude is not None and longitude is not None:
#         # Now you can use last_clicked_lat and last_clicked_lng
#         st.write(f"Last Clicked Latitude: {latitude}")
#         st.write(f"Last Clicked Longitude: {longitude}")
# else:
#     st.warning("Please click on the map to retrieve coordinates")
if st_data is not None and st_data.get("last_active_drawing") is not None:
    # Accessing coordinates from the last_active_drawing
    coordinates = st_data["last_active_drawing"].get("geometry", {}).get("coordinates")

    if coordinates is not None and len(coordinates) == 2:
        # Extract latitude and longitude
        latitude, longitude = coordinates
else:
    st.warning("Please click on the map to retrieve coordinates")
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
