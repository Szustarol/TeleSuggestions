from typing import List
from joblib import load

import numpy as np

# replace with the name of the model file to be loaded
model_path = "rfc_model_full_data_final.joblib"
encoder_path = "encoder.pkl"
label_encoder = load(encoder_path)
model = load(model_path)
nlags = 4

lag_weights = [1, 0.5, 0.1, 0.05]


def clean(ls):
    res_list = []
    for elem in ls:
        if elem != "" and elem != "fr" and elem != "en":
            res_list.append(elem)
    return res_list


def process_list(ls):
    res_list = []
    missing = nlags - len(ls)
    if missing < 0:
        return ls[-missing:]
    for i in range(missing):
        res_list.append(ls[0])
    res_list.extend(ls)
    return res_list


def transform_actual_data(list_strings):
    res_list = []
    for url in list_strings:
        origin = ["/"]
        origin.extend(url.split("/")[1:])
        processed = process_list(clean(origin))
        res_list.append(processed)
    return res_list


def predict_next_site(history: List[str]) -> List[str]:
    history = list(reversed(history))[:4]
    data = transform_actual_data(history)

    w_sum = 0
    vec = None
    for site, weight in zip(data, lag_weights):
        x_new = np.array([site])
        original_shape = x_new.shape

        x_new_enc = label_encoder.transform(
            x_new.flatten()).reshape(original_shape)

        y_pred = model.predict_proba(x_new_enc)

        if vec is None:
            vec = y_pred * weight
        else:
            vec += y_pred * weight

        w_sum += weight

    weighted = vec / w_sum

    prediction = label_encoder.inverse_transform(
        np.argpartition(weighted.reshape(-1), -5)[-5:])
    prediction = [
        "/" + x for x in prediction if not '.' in x and not "select" in x.lower()]

    return prediction
