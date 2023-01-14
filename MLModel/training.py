from Preprocessing import preprocess
import os
import json
import pandas as pd
from model import train_model

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
df = get_data()
config = get_config()

target_variable = config['target_column']

# Let's upsample the data
df = df.groupby(target_variable, group_keys=False).apply(lambda x: x.sample(n=150, replace=True))

X = preprocess(df, config)


# y = df[target_variable]

print(df.shape)
print(X.shape)

train_model(config, X, df[target_variable].values)



