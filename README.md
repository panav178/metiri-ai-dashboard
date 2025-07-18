# Metiri AI - Telematics Dashboard

A professional web dashboard for driving schools to manage telematics data, user profiles, and trip analysis using Damoov's telematics API.

## 🚀 Features

- **Embedded Dashboard**: Real-time telematics dashboard embedded from Damoov
- **User Management**: Add, view, and manage driving school users
- **Driver Profiles**: Generate individual driver profile dashboards
- **Trip Analysis**: Generate detailed trip analysis reports
- **Professional UI**: Clean, modern interface with Metiri AI branding
- **Local Deployment**: Easy setup for driving schools

## 📋 Prerequisites

- **Python 3.7+** installed on your computer
- **Internet connection** for API calls to Damoov
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🛠 Installation & Setup

### Step 1: Download the Files

1. Download all files to a folder on your computer
2. Ensure you have these files in your folder:
   - `server.py` - Main server application
   - `index.html` - Dashboard web interface
   - `logometiri.png` - Metiri AI logo
   - `README.md` - This documentation

### Step 2: Open Terminal/Command Prompt

**On Mac/Linux:**
- Open Terminal
- Navigate to your folder: `cd /path/to/your/folder`

**On Windows:**
- Open Command Prompt
- Navigate to your folder: `cd C:\path\to\your\folder`

### Step 3: Start the Server

Run this command in your terminal:

```bash
python3 server.py
```

**For Windows users, use:**
```bash
python server.py
```

### Step 4: Access the Dashboard

1. Open your web browser
2. Go to: **http://localhost:3000**
3. The Metiri AI dashboard will load automatically

## 🎯 How It Works

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Python Server  │    │  Damoov API     │
│   (localhost)   │◄──►│   (server.py)   │◄──►│  (External)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Server Components

1. **Web Server**: Serves the dashboard HTML/CSS/JavaScript
2. **API Proxy**: Handles trip analysis requests to avoid CORS issues
3. **Token Generation**: Creates fresh tokens for each API call

### API Integration

- **Dashboard**: Uses Damoov's dashboard generate-token API
- **Driver Profiles**: Uses Damoov's driver profile generate-token API  
- **Trip Analysis**: Uses Damoov's nocode generate-token API (server-side)

## 📱 Using the Dashboard

### Main Dashboard
- **Automatic Loading**: The main telematics dashboard loads automatically
- **Fresh Tokens**: New tokens are generated on each page load
- **Real-time Data**: Shows live telematics data from your fleet

### User Management

#### Adding Users
1. Click **"Settings"** in the top navigation
2. Enter the **User ID** (UUID format, e.g., `35e44797-4ec7-40ef-85fe-48da5a08431b`)
3. Enter the **User Name** (e.g., "John Smith")
4. Click **"Add User"**
5. User will appear in the Users list

#### Managing Users
1. Click **"Users"** in the top navigation
2. View all added users with their details
3. Use **"View Profile"** to open individual driver dashboards
4. Use **"Trip Analysis"** to generate trip analysis reports
5. Use **"Delete"** to remove users

### Driver Profiles
- Click **"View Profile"** on any user
- Opens a new tab with that user's individual driver dashboard
- Shows personalized driving metrics and statistics

### Trip Analysis
- Click **"Trip Analysis"** on any user
- Automatically generates a fresh trip analysis URL
- Opens detailed trip analysis dashboard in a new tab
- Includes route visualization, driving behavior, and safety metrics

## 🔧 Technical Details

### Server Configuration

**Port**: 3000 (configurable in server.py)
**API Endpoints**:
- `GET /` - Main dashboard
- `POST /api/trip-analysis` - Trip analysis token generation

### API Keys & Authentication

The server uses pre-configured API keys for Damoov integration:
- **API Key**: `RDFVUlYtYzJlZTFhZjYxYy0yMDI1MDcxNzA3NTcyNw==`
- **Company ID**: `23951f8c-116e-461e-a676-304cd47dcb6b`

### Data Storage

- **Local Storage**: User data is stored in browser's local storage
- **No Database**: No external database required
- **Persistent**: Data persists between browser sessions

## 🚨 Troubleshooting

### Common Issues

#### "Port 3000 is already in use"
**Solution**: 
```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9
# Then restart the server
python3 server.py
```

#### "Python not found"
**Solution**: Install Python 3.7+ from [python.org](https://python.org)

#### "Dashboard not loading"
**Solution**: 
1. Check internet connection
2. Ensure server is running (`python3 server.py`)
3. Clear browser cache and refresh

#### "Trip Analysis not working"
**Solution**: 
1. Check server logs for error messages
2. Ensure user ID is in correct UUID format
3. Verify API key is valid

### Server Logs

The server provides detailed logs in the terminal:
```
Dashboard server running on port 3000
Access the dashboard at: http://localhost:3000
Trip analysis API available at: http://localhost:3000/api/trip-analysis
127.0.0.1 - - [timestamp] "GET / HTTP/1.1" 200 -
Generating trip analysis for user: [user-id]
Making request to: https://extras.telematicssdk.com/token/nocode/generate_token
Response: {"url": "https://portal.damoov.com/trip_details/[token]"}
```

## 🔒 Security Considerations

- **Local Deployment**: Runs only on your local machine
- **No External Access**: Dashboard is not accessible from the internet
- **API Keys**: Embedded in server code (consider environment variables for production)
- **User Data**: Stored locally in browser

## 📈 Performance

- **Fast Loading**: Optimized for quick dashboard loading
- **Fresh Tokens**: Automatic token refresh prevents expired sessions
- **Responsive Design**: Works on desktop and mobile devices
- **Minimal Resources**: Lightweight Python server

## 🎨 Customization

### Changing the Logo
Replace `logometiri.png` with your own logo file (same name)

### Modifying Colors
Edit the CSS in `index.html` to change the color scheme

### Adding Features
The modular design allows easy addition of new features

## 📞 Support

For technical support or questions:
1. Check the server logs for error messages
2. Verify all prerequisites are installed
3. Ensure internet connection is working
4. Contact your system administrator if issues persist

## 🔄 Updates

To update the dashboard:
1. Stop the server (Ctrl+C in terminal)
2. Replace files with new versions
3. Restart the server (`python3 server.py`)

## 📋 System Requirements

**Minimum Requirements:**
- Python 3.7+
- 4GB RAM
- 100MB disk space
- Internet connection

**Recommended:**
- Python 3.9+
- 8GB RAM
- 500MB disk space
- High-speed internet connection

---

**Metiri AI Dashboard** - Professional telematics management for driving schools
