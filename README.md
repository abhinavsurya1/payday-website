# PayDayzz - Job Portal Website

A comprehensive job portal built with Django that connects job seekers with employers. Features include user authentication, job posting, application management, and profile management.

## 🚀 Live Demo

https://payday-website.onrender.com

## 🚀 Features

- **User Authentication**: Secure login/signup with Django AllAuth
- **Job Management**: Post, browse, and apply for jobs
- **Profile Management**: Complete candidate and employer profiles
- **File Uploads**: CV, profile pictures, and verification documents
- **Email Notifications**: Automated email notifications
- **WhatsApp Integration**: WhatsApp notifications (configurable)
- **Responsive Design**: Mobile-friendly interface
- **Admin Dashboard**: Comprehensive admin interface

## 🛠️ Tech Stack

- **Backend**: Django 5.1.7
- **Database**: PostgreSQL
- **Authentication**: Django AllAuth
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **File Handling**: Pillow
- **API**: Django REST Framework
- **Deployment**: Render (free hosting)

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/paydayzz-website.git
cd paydayzz-website
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/paydayzz
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see your application!

## 📁 Project Structure

```
paydayzz-website/
├── home/                 # Main app with landing pages
├── jobs/                 # Job posting and application logic
├── profiles/             # User profile management
├── notifications/        # Notification system
├── paydayzz/            # Main Django project settings
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── media/               # User uploaded files
├── requirements.txt     # Python dependencies
├── build.sh            # Deployment build script
├── render.yaml         # Render deployment config
└── DEPLOYMENT.md       # Deployment guide
```

## 🌐 Deployment

This project is configured for free hosting on Render. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy Steps:
1. Push code to GitHub
2. Connect repository to Render
3. Configure environment variables
4. Deploy!

## 🔧 Configuration

### Database
- **Development**: PostgreSQL (local)
- **Production**: PostgreSQL (Render)

### Email Settings
Configure SMTP settings in `.env`:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### WhatsApp Integration
Add WhatsApp Business API credentials:
```env
WHATSAPP_API_KEY=your-api-key
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
WHATSAPP_BUSINESS_ACCOUNT_ID=your-account-id
```

## 👥 User Roles

### Job Seekers
- Create profile with CV upload
- Browse and apply for jobs
- Track application status
- Receive notifications

### Employers
- Post job listings
- Review applications
- Manage company profile
- Send notifications

### Admin
- Manage all users and content
- Monitor system activity
- Configure site settings

## 🔒 Security Features

- CSRF protection
- Secure file uploads
- Password validation
- Environment variable configuration
- CORS settings for production

## 📱 API Endpoints

The project includes Django REST Framework for API functionality:
- User authentication
- Job CRUD operations
- Profile management
- Application tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the deployment guide
- Review Django documentation

---

**Built with ❤️ using Django** 
