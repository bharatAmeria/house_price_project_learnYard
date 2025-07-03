from flask import Flask, render_template, request
import pandas as pd
from joblib import load

app = Flask(__name__)

# Load preprocessed data and model
data = pd.read_csv("app/processed_data.csv")
model = load('app/model.pkl')

@app.route('/')
def index():
    # Get sorted list of unique locations
    locations = sorted(data["location"].unique())
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        bath = int(request.form.get('bath'))
        sqft = float(request.form.get('total_sqft'))

        # Log for debugging
        print(f"Input received - Location: {location}, BHK: {bhk}, Bath: {bath}, Sqft: {sqft}")

        # Create input dataframe
        input_df = pd.DataFrame([[location, sqft, bath, bhk]], columns=["location", "total_sqft", "bath", "bhk"])

        # Predict
        prediction = model.predict(input_df)[0] * 1e5

        return str(round(float(prediction), 2))

    except Exception as e:
       return f"Error in prediction: {e}"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
