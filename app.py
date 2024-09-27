from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

@app.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if file.filename.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file_path)

    # Save the dataframe in session for future use
    session['data'] = df.to_dict()

    return render_template('select_model.html', columns=df.columns)


@app.route('/train_model', methods=['POST'])
def train_model():
    df = pd.DataFrame(session['data'])  # Retrieve dataset from session
    model_type = request.form['model']
    column = request.form['column']

    X = df.drop(column, axis=1)  # Features
    y = df[column]  # Target

    if model_type == 'linear_regression':
        model = LinearRegression()
    elif model_type == 'decision_tree':
        model = DecisionTreeRegressor()

    model.fit(X, y)

    # Save model and data for use in graph generation
    session['model'] = model
    session['X'] = X.to_dict()
    session['y'] = y.to_dict()
    session['column'] = column
    session['model_type'] = model_type

    return redirect(url_for('select_graph'))


if __name__ == '__main__':
    app.run(debug=True)
