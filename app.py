import os
import pandas as pd
from flask import Flask, render_template, request, session, jsonify
from flask_dropzone import Dropzone
from flask_session import Session
from services.pandas_agent import PandasAgentDescription
from services.pd_ai import PandasAiQuestion
from services.lida_ai import LidaAi

os.environ["OPENAI_API_KEY"] = ""

app = Flask(__name__)
dropzone = Dropzone(app)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.csv, .xlsx'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3
app.config['DROPZONE_IN_FORM'] = True
app.config['DROPZONE_UPLOAD_ON_CLICK'] = True
app.config['DROPZONE_UPLOAD_ACTION'] = 'handle_upload'
app.config['DROPZONE_UPLOAD_BTN_ID'] = 'submit'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_upload', methods=['POST'])
def handle_upload():
    for key, f in request.files.items():
        if key.startswith('file'):
            df = pd.read_excel(f) if '.xlsx' in f.filename else pd.read_csv(f)
            session["df"] = df
            session['df_json'] = df.to_json()
    return '', 204

@app.route('/data_preview')
def data_preview():
    df_json = session.get('df_json')
    if df_json:
        df = pd.read_json(df_json)
        return df.head().to_html(classes='table table-striped table-hover centered-table'), 200
    return "No data uploaded", 404

@app.route('/get_description')
def get_description():
    df = session.get('df')
    agent = PandasAgentDescription(df)
    responses = agent.get_default_answers()
    return jsonify(responses)

@app.route('/process_agent_question', methods=['POST'])
def process_agent_question():
    df = session.get('df')
    question = request.get_json()['question']
    agent = PandasAgentDescription(df)
    response = agent.run(question)
    return jsonify(response)

@app.route('/process_pandasai_question', methods=['POST'])
def process_pandasai_question():
    df = session.get('df')
    question = request.get_json()['question']
    ai_agent = PandasAiQuestion(df)
    response = ai_agent.run(question)
    if isinstance(response, pd.DataFrame):
        response_html = response.to_html(classes='table table-striped table-hover centered-table')
        return jsonify({'type': 'dataframe', 'data': response_html})
    else:
        return jsonify({'type': 'text', 'data': response})

@app.route('/get_lida')
def get_lida():
    print("inside get lida")
    df = session.get("df")
    ai_agent = LidaAi(df)
    results = ai_agent.run()
    print(results)
    return jsonify(results)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
