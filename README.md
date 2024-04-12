# 🚀Immo-Eliza-Deployment

Explore the possibilities of real-time machine learning with my latest creation: the Immo Eliza Price Predictor App. Designed to integrate seamlessly with my [trained machine learning model](https://github.com/HazemEldabaa/immo-eliza-ml) via an API, this app allows you to enter the specific features of your house and instantly receive a tailored price prediction.

But that’s not all—my app also provides a comparative analysis, showing you how your house stacks up against others in the same area. Gain insights into the local market and see where your property stands in terms of value, all in real-time.
##  ↩️Previous Parts
This project is a follow up of  the [Immo Eliza Scraper & Data Analyser](https://github.com/HazemEldabaa/immo-eliza-goats) and the [Immo Eliza Machine Learning Models](https://github.com/HazemEldabaa/immo-eliza-ml)
##  📁Project Structure
- src : contains predictions endpoints and artifacts for the ML models
- Dockerfile : Dockerfile building image and dependencies required for both API and Streamlit for online deployment
- streamlit.py : interactive app configurations
# 🏁Getting Started

## 📋Prerequisites
- Python 3.x
## 🛠️Installation

**Clone the Repository:**

```bash
git clone https://github.com/HazemEldabaa/immo-eliza-deployment.git
cd immo-eliza-deployment
```
**Create a Virtual Environment (Optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: \venv\Scripts\activate
```
**Install Dependencies:**

```bash
pip install -r requirements.txt
```
## 👩‍💻Usage
Make sure to edit the ```FASTAPI_URL``` variable inside ```streamlit.py``` with your API endpoint, locally or on Render

#### To run locally:
To run the API:
```bash
python src/main.py
```

To run the Streamlit App:
```bash
streamlit run streamlit.py
```
Once all the services are running, you should be able to access the Airflow UI from http://localhost:8080/

#### To deploy online:
Create a fork of the repo, then use Render to deploy the API, and Streamlit to deploy the interface


## 📷Screenshots

### Interface:
![Streamlit Interface](https://i.ibb.co/48TpjVY/immo-eliza-screenshot1.png)
### Prediction:
![Prediction](https://i.ibb.co/mcTPhmX/image.png)

