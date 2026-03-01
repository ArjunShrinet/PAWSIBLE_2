# 🐾 Pawsible - Pet Care Management System

> Making Pet Care Pawsible!

A comprehensive web-based pet management system that helps pet owners organize and track their pets' information, medical documents, schedules, and more—all in one place.

![Pawsible Banner](static/img/PawsibleIcon.jpg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)

## ✨ Features

### 🔐 User Authentication
- Secure user registration and login
- Password hashing with werkzeug security
- Session management
- Protected routes requiring authentication

### 🐕 Pet Management
- Add multiple pets with detailed information (name, breed, age)
- Upload pet photos
- Delete pets
- Each user sees only their own pets

### 📁 Document Management
- Upload documents per pet (PDF, DOC, DOCX, JPG, PNG, TXT)
- Organize medical records, vaccination certificates, etc.
- View documents in browser
- Delete documents
- Separate document storage for each pet

### 📅 Schedule Management
- Create appointments and reminders for each pet
- Multiple schedule types:
  - 🏥 Vet Appointments
  - ✂️ Grooming Sessions
  - 💊 Medication Reminders
  - 📌 Other Activities
- Filter schedules by pet or type
- Upcoming schedules sorted by date
- Add location and notes to appointments

### 🎨 User Interface
- Clean, modern design
- Responsive layout
- Consistent color scheme
- Easy navigation with sidebar menu
- Visual feedback and animations

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 3.x
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Werkzeug Security (password hashing)
- **File Upload:** Werkzeug Utils (secure filename)
- **CORS:** Flask-CORS

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (ES6+)** - Interactivity
- **Bootstrap 5.3** - UI Components
- **Fetch API** - Asynchronous requests

### Database
- **SQLite** - Lightweight, file-based database
- **SQLAlchemy** - Python SQL toolkit and ORM

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pawsible.git
cd pawsible
```

### Step 2: Install Dependencies
```bash
pip install flask flask-cors flask-sqlalchemy werkzeug
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:8000`

### Step 4: Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## 🚀 Usage

### First Time Setup
1. Navigate to `http://127.0.0.1:8000/login`
2. Click "Sign Up" to create a new account
3. Enter your email and password (minimum 6 characters)
4. Login with your credentials

### Adding Pets
1. After login, you'll be redirected to the Dashboard
2. Fill in pet details: Name, Breed, Age
3. Upload a pet photo
4. Click "Add Pet"

### Managing Documents
1. Go to "Documents" from the sidebar
2. Select a pet from the dropdown
3. Upload documents (medical records, vaccination certificates, etc.)
4. Click on any document to view it
5. Delete documents as needed

### Creating Schedules
1. Go to "Schedules" from the sidebar
2. Click the floating "+" button
3. Fill in schedule details:
   - Select pet
   - Choose schedule type (Vet, Grooming, Medication, Other)
   - Add title, date/time, location, and notes
4. View and filter upcoming schedules

## 📁 Project Structure

```
pawsible/
├── app.py                      # Main Flask application
├── instance/
│   └── users.db               # SQLite database (auto-generated)
├── static/
│   ├── img/
│   │   └── PawsibleIcon.jpg   # Logo and images
│   ├── uploads/
│   │   ├── pets/              # Pet photos
│   │   └── documents/         # Pet documents
│   └── docs.js                # JavaScript utilities
├── templates/
│   ├── index.html             # Home page
│   ├── login.html             # Login/Signup page
│   ├── dashboard.html         # Pet management
│   ├── documents.html         # Document management
│   ├── schedules.html         # Schedule management
│   ├── settings.html          # User settings
│   ├── info.html              # About page
│   └── comingsoon.html        # Placeholder page
├── README.md                   # This file
└── requirements.txt           # Python dependencies (optional)
```

## 🔌 API Endpoints

### Authentication
- `POST /api/signup` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/check-session` - Check if user is logged in

### Pets
- `GET /api/pets` - Get all pets for logged-in user
- `POST /api/pets` - Add new pet
- `DELETE /api/pets/<pet_id>` - Delete pet

### Documents
- `GET /api/documents/pets` - Get all pets for document selection
- `POST /api/documents` - Upload document for a pet
- `GET /api/documents/pet/<pet_id>` - Get all documents for a pet
- `DELETE /api/documents/<doc_id>` - Delete document

## 🗄️ Database Schema

### User Table
| Column   | Type    | Description              |
|----------|---------|--------------------------|
| id       | Integer | Primary key              |
| email    | String  | Unique email address     |
| password | String  | Hashed password          |

### Pet Table
| Column           | Type     | Description                    |
|------------------|----------|--------------------------------|
| id               | Integer  | Primary key                    |
| name             | String   | Pet name                       |
| breed            | String   | Pet breed                      |
| age              | Integer  | Pet age                        |
| picture_filename | String   | Path to pet photo              |
| user_id          | Integer  | Foreign key to User            |
| created_at       | DateTime | Timestamp of creation          |

### Document Table
| Column            | Type     | Description                    |
|-------------------|----------|--------------------------------|
| id                | Integer  | Primary key                    |
| filename          | String   | Stored filename                |
| original_filename | String   | Original uploaded filename     |
| file_type         | String   | File extension                 |
| pet_id            | Integer  | Foreign key to Pet             |
| user_id           | Integer  | Foreign key to User            |
| uploaded_at       | DateTime | Timestamp of upload            |

## 📸 Screenshots

### Login Page
User-friendly authentication with signup option.

### Dashboard
Manage all your pets in one place with photos and details.

### Documents
Upload and organize pet documents by pet profile.

### Schedules
Never miss a vet appointment or medication time.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- [ ] Vet Details management
- [ ] Advanced settings (change password, profile info)
- [ ] Email/SMS reminders for schedules
- [ ] Multi-pet comparison and analytics
- [ ] Export pet data as PDF
- [ ] Mobile app version
- [ ] Integration with vet clinic systems
- [ ] Pet health tracking and charts
- [ ] Vaccination schedule automation
- [ ] Community features (share tips, connect with other pet owners)

## 🐛 Known Issues

- Schedule data currently uses demo data (backend integration pending)
- Settings page is a placeholder

## 💡 Tips

- Regular backups recommended (copy `instance/users.db`)
- Keep pet photos under 5MB for best performance
- Use descriptive filenames for documents
- Set up schedules in advance for timely reminders

---

**Made with ❤️ for pet lovers everywhere!**

*Pawsible - Making Pet Care Pawsible!*
