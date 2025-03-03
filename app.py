from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  

# SQLite Datenbank einrichten
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Datenbank-Modell für Bestellungen
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    address = db.Column(db.String(300), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    material = db.Column(db.String(50), nullable=False)
    model_filename = db.Column(db.String(200), nullable=False)

# Erstellt die Datenbank (falls nicht vorhanden)
with app.app_context():
    db.create_all()

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'stl', 'obj'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    name = request.form.get('name')
    company = request.form.get('company')
    address = request.form.get('address')
    quantity = request.form.get('quantity')
    material = request.form.get('material')

    if not all([name, address, quantity, material]):
        return jsonify({'error': 'Missing required fields'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(file_path)
            new_order = Order(name=name, company=company, address=address, quantity=int(quantity), material=material, model_filename=filename)
            db.session.add(new_order)
            db.session.commit()
            return jsonify({'message': 'Order submitted successfully', 'order_id': new_order.id}), 200
        except Exception as e:
            return jsonify({'error': f'File could not be saved: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
