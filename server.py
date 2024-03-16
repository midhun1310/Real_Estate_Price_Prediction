from flask import Flask, request, jsonify, render_template
import pickle
import json

app = Flask(__name__)

# Load your model and columns
with open('bangalore_prices_model.pickle', 'rb') as model_file:
    model = pickle.load(model_file)

with open('columns.json', 'r') as columns_file:
    columns = json.load(columns_file)['data_columns']

@app.route('/')
def home():
    locations = columns[3:]  # Assuming the first few columns are not locations
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    # Assuming the first 3 columns in your model are total_sqft, bath, bhk in order,
    # and the rest are dummy variables for locations.
    input_array = [0] * len(columns)
    input_array[0] = total_sqft
    input_array[1] = bath
    input_array[2] = bhk
    if location in columns:
        loc_index = columns.index(location)
        input_array[loc_index] = 1

    prediction = model.predict([input_array])[0]

    return render_template('index.html', prediction_text=f'Estimated Price: {prediction:.2f} Lakhs', locations=columns[3:])

if __name__ == "__main__":
    app.run(debug=True)


