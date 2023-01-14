
'''
{
	"Unnamed: 0": 10,
	"Data": "2016-01-28 00:00:00",
	"Countries": "Country_01",
	"Local": "Local_03",
	"Industry Sector": "Mining",
	"Accident Level": "I",
	"Potential Accident Level": "III",
	"Genre": "Male",
	"Employee or Third Party": "Employee",
	"Critical Risk": "Others",
	"Description": "While installing a segment of the polyurethane pulley protective lyner - 60x4x5cm weighing 1.2 kg - on the head pulley of the ore winch, when the pulley is rotated to compress the lyner inside the channel, it falls from its housing 1.50 m rubbing the right side of the worker hip, generating the injury described."
}

'''




from Preprocessing import preprocess_predict
import os
import json
import pandas as pd
from model import predict_model
from flask import Flask, request

from dotenv import load_dotenv
load_dotenv()




def get_data() -> pd.DataFrame:
    data_path = os.getenv('DATA_PATH')
    if not os.path.exists(data_path):
        raise Exception(f"Training: data path f{data_path} not valid.")
    return pd.read_csv(data_path)


def get_config() -> dict:
    config_path = os.getenv('CONFIG_FILE')
    if not os.path.exists(config_path):
        raise Exception(f"Training: config path 'f{config_path}' not valid.")
    with open(config_path, 'r') as f:
        return json.load(f)



# Let's preprocess the data
# df = get_data()
config = get_config()

target_variable = config['target_column']

# Validate and enrich the data
def validate_enrich(input):
    categorical_columns = config['categorical_columns']
    description_column = config["description_column"]
    data = {}
    for col in categorical_columns + [description_column]:
        if input.get(col, "@@") == "@@":
            raise Exception(f"PredictModel.validate and rich: Input data has missing field {col}")
        data[col] = input[col]
    return pd.DataFrame([data])



# Predict from input
def predict_input(input):
    X = preprocess_predict(validate_enrich(input), config)
    prediction, classes, answer = predict_model(config, X)
    # print(prediction)
    # print(classes)
    return {
        "prediction":list(prediction),
        "classes":list(classes),
        "answer":answer
    }


# Let's upsample the data
# df = df.iloc[20:21]

# X = preprocess_predict(df, config)


# y = df[target_variable]

# print(df.shape)
# print(X.shape)

print('''----------------------''')
# print(predict_model(config, X))


# Define services

app = Flask(__name__)

@app.route("/check")
def hello_world():
    return "Hello, World!"



@app.route('/predict', methods=['POST'])
def predict():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(f'''
        Input given is:
        {json}
        ''')
        data = predict_input(json)
        return data
    else:
        return 'Content-Type not supported!'


if __name__ == "__main__":
    app.run(debug=True, port=5010, host="0.0.0.0")



