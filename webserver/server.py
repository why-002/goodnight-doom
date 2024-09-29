import joblib
import pandas as pd
import flask

model = joblib.load('../models/is_political.joblib')
app = flask.Flask(__name__)

# wait for json post request and return prediction
@app.route('/api', methods=['POST'])
def predict():
    req_data = flask.request.json
    df = pd.DataFrame(req_data)

    prediction = list(model.predict(df))

    return flask.jsonify({'prediction': bool(prediction)})

# load the model and start web api
if __name__ == 'main':
    app.run()