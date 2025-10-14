# CobraFramework

A lightweight, high-performance Python web framework built from scratch with modern features and clean architecture.

## 🚀 Features

- **High Performance**: Multi-threaded HTTP server with connection pooling
- **File Upload Support**: Built-in multipart file upload handling
- **Route Mapping**: Flexible routing system with parameter support
- **View Engine**: Template rendering system
- **Configuration Management**: JSON-based configuration
- **Cookie Support**: Built-in cookie handling
- **Static Assets**: Automatic static file serving
- **Middleware Support**: Extensible middleware architecture

## 📋 Requirements

- Python 3.6+
- No external dependencies (pure Python implementation)

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/realcyberdyne/CobraFramework.git
```

Navigate to the project directory:

```bash
cd CobraFramework
```

## 🚀 Quick Start

Run the application:

```bash
python app.py
```

The server will start on `localhost:9009` by default.

## 📁 Project Structure

```
CobraFramework/
├── app.py                 # Main application entry point
├── config.json           # Configuration file
├── Assets/               # Static assets (CSS, images)
├── Config/               # Configuration management
├── Controllers/          # MVC Controllers
├── Http/                 # HTTP handling
│   ├── Handlers/         # Request/Response handlers
│   └── Middleware/       # Middleware components
├── Reponse/              # Response utilities
├── Route/                # Routing system
├── View/                 # HTML templates
├── FileManager/          # File management utilities
├── Files/                # File storage
└── FileTmp/              # Temporary file uploads
```

## ⚙️ Configuration

Edit `config.json` to customize your application:

```json
{
  "app": {
    "PORT": 9009,
    "HOST": "localhost",
    "BUFFERSIZE": 99999,
    "RequestTimeOut": 0.5,
    "MAX_FILE_SIZE": 10,
    "UPLOAD_DIR": "C:\\Users\\rezafta\\Desktop\\CobraFramework\\FileTmp"
  }
}
```

### Configuration Options

- `PORT`: Server port number
- `HOST`: Server host address
- `BUFFERSIZE`: Request buffer size in bytes
- `RequestTimeOut`: Request timeout in seconds
- `MAX_FILE_SIZE`: Maximum file upload size in MB
- `UPLOAD_DIR`: Directory for file uploads

## 🎯 Usage Examples

### Basic Controller

```python
from Reponse.DResponse import DResponse
from Reponse.DView import DView

class HomeController:
    def index(self, params, request):
        return DResponse(DView("index"))
    
    def sayhello(self, request, params):
        return DResponse("Hello %s!" % params["name"])
```

### Route Configuration

Routes are defined in `Route/GetMapping.py`:

```python
routes = [
    {
        'pattern': '/',
        'controller': HomeController,
        'method': 'index'
    },
    {
        'pattern': '/hello/{name}',
        'controller': HomeController,
        'method': 'sayhello'
    }
]
```

### File Upload

The framework automatically handles multipart file uploads. Uploaded files are saved to the configured `UPLOAD_DIR`.

### Static Assets

Static files in the `Assets/` directory are automatically served at `/Assets/` URLs.

## 🔧 Development

### Adding New Routes

1. Create a controller method in `Controllers/`
2. Add the route pattern in `Route/GetMapping.py`
3. Map the route to your controller method

### Creating Views

1. Add HTML templates to the `View/` directory
2. Use `DView("template_name")` in your controller
3. Templates are automatically rendered

### Middleware

Add custom middleware in `Http/Middleware/` to extend functionality.

## 🌐 API Endpoints

- `GET /` - Home page
- `GET /sampleform` - Sample form page
- `GET /Assets/*` - Static assets

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support and questions, please open an issue on GitHub.

---

**Powered by Cyberdyne** 🚀
