import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario == 'admin' and senha == '1234':
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro=True)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Build robust path to CSV relative to this file
    from pathlib import Path
    csv_path = Path(__file__).resolve().parent.parent / 'data' / 'raw' / 'usuarios_admin_center.csv'
    # Import pipeline functions
    from src.data_reader import read_data_users
    from src.data_cleaner import clean_user_data
    from src.data_analysis import process_user_data
    # Execute pipeline
    df_raw = read_data_users(csv_path)
    df_clean = clean_user_data(df_raw)
    df_final = process_user_data(df_clean)
    # Select only required columns and first 5 rows
    df_top5 = df_final.head(5)[['nome', 'email', 'status']]
    usuarios = df_top5.to_dict('records')
    return render_template('dashboard.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
