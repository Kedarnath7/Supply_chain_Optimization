from flask import Flask, request, render_template
import os
import pandas as pd
from src.supply_chain_optimization.pipelines.prediction_pipeline import preprocess_and_predict 

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('upload.html', message="No file uploaded!")

    file = request.files['file']
    if file.filename == '':
        return render_template('upload.html', message="No selected file!")

    input_csv_path = os.path.join("temp", "uploaded_input.csv")
    os.makedirs(os.path.dirname(input_csv_path), exist_ok=True)
    file.save(input_csv_path)

    output_csv_path = os.path.join("temp", "output_predictions.csv")
    preprocess_and_predict(input_csv_path, output_csv_path)
    output_df = pd.read_csv(output_csv_path)
    return render_template('result.html', table_data=output_df.to_dict(orient='records'), columns=output_df.columns.tolist())

if __name__ == "__main__":
    app.run(debug=True)
