from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Secret key for session management
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload configuration for pets
UPLOAD_FOLDER = 'static/uploads/pets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upload configuration for documents
DOCUMENT_FOLDER = 'static/uploads/documents'
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt'}
app.config['DOCUMENT_FOLDER'] = DOCUMENT_FOLDER

# Create upload folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    pets = db.relationship('Pet', backref='owner', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

# Pet Model
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    picture_filename = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    documents = db.relationship('Document', backref='pet', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pet {self.name}>'

# Document Model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50))
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.original_filename}>'

# Create database tables
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_document_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS

# Your existing routes
@app.route('/')
def base():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')
    
@app.route('/schedules')
def schedules():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('schedules.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/comingsoon')
def comingsoon():
    return render_template('comingsoon.html')

# Authentication API routes
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'email': email
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_email'] = email
            session['user_id'] = user.id
            return jsonify({
                'message': 'Login successful',
                'email': email
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_email', None)
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# PET API ROUTES

@app.route('/api/pets', methods=['GET'])
def get_pets():
    """Get all pets for the logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        user_id = session['user_id']
        pets = Pet.query.filter_by(user_id=user_id).all()
        
        pets_data = []
        for pet in pets:
            pets_data.append({
                'id': pet.id,
                'name': pet.name,
                'breed': pet.breed,
                'age': pet.age,
                'picture': pet.picture_filename
            })
        
        return jsonify({'pets': pets_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pets', methods=['POST'])
def add_pet():
    """Add a new pet for the logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        # Get form data
        name = request.form.get('name')
        breed = request.form.get('breed')
        age = request.form.get('age')
        
        # Validate input
        if not name or not breed or not age:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Handle file upload
        picture_filename = None
        if 'picture' in request.files:
            file = request.files['picture']
            if file and file.filename and allowed_file(file.filename):
                # Create unique filename
                filename = secure_filename(file.filename)
                user_id = session['user_id']
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                picture_filename = f"user_{user_id}_pet_{timestamp}_{filename}"
                
                # Save file
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
                file.save(filepath)
        
        # Create new pet
        new_pet = Pet(
            name=name,
            breed=breed,
            age=int(age),
            picture_filename=picture_filename,
            user_id=session['user_id']
        )
        
        db.session.add(new_pet)
        db.session.commit()
        
        return jsonify({
            'message': 'Pet added successfully',
            'pet': {
                'id': new_pet.id,
                'name': new_pet.name,
                'breed': new_pet.breed,
                'age': new_pet.age,
                'picture': new_pet.picture_filename
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """Delete a pet"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        pet = Pet.query.filter_by(id=pet_id, user_id=session['user_id']).first()
        
        if not pet:
            return jsonify({'error': 'Pet not found'}), 404
        
        # Delete image file if exists
        if pet.picture_filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], pet.picture_filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        db.session.delete(pet)
        db.session.commit()
        
        return jsonify({'message': 'Pet deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DOCUMENT API ROUTES

@app.route('/api/documents/pets', methods=['GET'])
def get_user_pets_for_documents():
    """Get all pets for the logged-in user (for document upload selection)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        user_id = session['user_id']
        pets = Pet.query.filter_by(user_id=user_id).all()
        
        pets_data = []
        for pet in pets:
            pets_data.append({
                'id': pet.id,
                'name': pet.name,
                'breed': pet.breed
            })
        
        return jsonify({'pets': pets_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents', methods=['POST'])
def upload_document():
    """Upload a document for a specific pet"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        pet_id = request.form.get('pet_id')
        
        if not pet_id:
            return jsonify({'error': 'Pet ID is required'}), 400
        
        # Verify pet belongs to user
        pet = Pet.query.filter_by(id=pet_id, user_id=session['user_id']).first()
        if not pet:
            return jsonify({'error': 'Pet not found'}), 404
        
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_document_file(file.filename):
            # Create unique filename
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"pet_{pet_id}_doc_{timestamp}.{file_extension}"
            
            # Save file
            filepath = os.path.join(app.config['DOCUMENT_FOLDER'], new_filename)
            file.save(filepath)
            
            # Create document record
            new_document = Document(
                filename=new_filename,
                original_filename=original_filename,
                file_type=file_extension,
                pet_id=pet_id,
                user_id=session['user_id']
            )
            
            db.session.add(new_document)
            db.session.commit()
            
            return jsonify({
                'message': 'Document uploaded successfully',
                'document': {
                    'id': new_document.id,
                    'filename': new_document.filename,
                    'original_filename': new_document.original_filename,
                    'file_type': new_document.file_type
                }
            }), 201
        else:
            return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents/pet/<int:pet_id>', methods=['GET'])
def get_pet_documents(pet_id):
    """Get all documents for a specific pet"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        # Verify pet belongs to user
        pet = Pet.query.filter_by(id=pet_id, user_id=session['user_id']).first()
        if not pet:
            return jsonify({'error': 'Pet not found'}), 404
        
        documents = Document.query.filter_by(pet_id=pet_id).all()
        
        docs_data = []
        for doc in documents:
            docs_data.append({
                'id': doc.id,
                'filename': doc.filename,
                'original_filename': doc.original_filename,
                'file_type': doc.file_type,
                'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'pet_name': pet.name,
            'documents': docs_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        document = Document.query.filter_by(id=doc_id, user_id=session['user_id']).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Delete file
        filepath = os.path.join(app.config['DOCUMENT_FOLDER'], document.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# SETTINGS API ROUTES

@app.route('/api/user/info', methods=['GET'])
def get_user_info():
    """Get current user information"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'email': user.email}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/update-email', methods=['PUT'])
def update_email():
    """Update user email address"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        new_email = data.get('new_email')
        
        if not new_email:
            return jsonify({'error': 'New email is required'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user and existing_user.id != session['user_id']:
            return jsonify({'error': 'Email already in use'}), 400
        
        user = User.query.get(session['user_id'])
        user.email = new_email
        db.session.commit()
        
        session['user_email'] = new_email
        
        return jsonify({'message': 'Email updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/change-password', methods=['PUT'])
def change_password():
    """Change user password"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'All fields are required'}), 400
        
        user = User.query.get(session['user_id'])
        
        if not check_password_hash(user.password, current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/delete-account', methods=['DELETE'])
def delete_account():
    """Delete user account and all associated data"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        user = User.query.get(session['user_id'])
        
        # Delete all user's pet images
        for pet in user.pets:
            if pet.picture_filename:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], pet.picture_filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        # Delete all user's documents
        for pet in user.pets:
            for doc in pet.documents:
                filepath = os.path.join(app.config['DOCUMENT_FOLDER'], doc.filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        db.session.delete(user)
        db.session.commit()
        
        session.clear()
        
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)