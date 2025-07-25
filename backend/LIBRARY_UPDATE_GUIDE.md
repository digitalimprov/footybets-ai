# Google Generative AI Library Update Guide

## Current Status

**Current Version**: `google-generativeai==0.1.0rc1`  
**Python Version**: 3.8  
**Status**: ✅ Working but limited functionality

## The Issue

The current version (`0.1.0rc1`) has limited support for Gemini models and uses an older API structure. The latest versions require Python 3.9+ and provide full Gemini model support.

## Update Options

### Option 1: Upgrade Python Version (Recommended)

**Prerequisites**: Python 3.9 or higher

1. **Install Python 3.9+**:
   ```bash
   # On macOS with Homebrew
   brew install python@3.9
   
   # Or download from python.org
   # https://www.python.org/downloads/
   ```

2. **Create new virtual environment**:
   ```bash
   # Remove old venv
   rm -rf venv/
   
   # Create new venv with Python 3.9+
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Update Google Generative AI**:
   ```bash
   pip uninstall google-generativeai -y
   pip install google-generativeai --upgrade
   ```

5. **Verify installation**:
   ```bash
   python -c "import google.generativeai as genai; print(genai.__version__)"
   ```

### Option 2: Use Latest Compatible Version

If you can't upgrade Python, try installing a newer version that still supports Python 3.8:

```bash
pip uninstall google-generativeai -y
pip install google-generativeai==0.3.2
```

### Option 3: Alternative AI Libraries

Consider using alternative libraries that support Gemini API:

1. **OpenAI GPT** (if you have OpenAI API key):
   ```bash
   pip install openai
   ```

2. **Hugging Face Transformers**:
   ```bash
   pip install transformers torch
   ```

3. **Direct HTTP requests to Gemini API**:
   ```python
   import requests
   
   def call_gemini_api(prompt, api_key):
       url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
       headers = {"Content-Type": "application/json"}
       data = {
           "contents": [{"parts": [{"text": prompt}]}]
       }
       response = requests.post(f"{url}?key={api_key}", json=data)
       return response.json()
   ```

## Current Working Setup

The current setup works with the following limitations:

### ✅ What Works:
- API key configuration
- Basic text generation
- Backend integration
- Frontend interface

### ⚠️ Limitations:
- Limited model support
- Older API structure
- No `GenerativeModel` class
- Restricted functionality

### 🔧 Current API Usage:

```python
import google.generativeai as genai

# Configure API
genai.configure(api_key="your_api_key")

# Available methods in current version:
# - genai.generate_text(prompt="your prompt")
# - genai.chat()
# - genai.list_models()
# - genai.get_model()
```

## Testing the Update

After updating, test with this script:

```python
#!/usr/bin/env python3
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# Test with new API
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello!")
    print("✅ New API working:", response.text)
except Exception as e:
    print("❌ Error:", e)
```

## Migration Steps

1. **Backup current setup**:
   ```bash
   cp -r venv venv_backup
   ```

2. **Update Python** (if possible)

3. **Update library**:
   ```bash
   pip install google-generativeai --upgrade
   ```

4. **Update code** (if needed):
   ```python
   # Old way (current)
   response = genai.generate_text(prompt="Hello")
   
   # New way (after update)
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Hello")
   ```

5. **Test thoroughly**:
   ```bash
   python -c "from app.ai.predictor import AFLPredictor; print('✅ AI Predictor loads successfully')"
   ```

## Troubleshooting

### Common Issues:

1. **Python version error**:
   ```
   ERROR: Package requires Python >=3.9
   ```
   **Solution**: Upgrade Python or use compatible version

2. **Import error**:
   ```
   ModuleNotFoundError: No module named 'google.generativeai'
   ```
   **Solution**: Reinstall the library

3. **API errors**:
   ```
   404 Requested entity was not found
   ```
   **Solution**: Check API key and model names

### Fallback Plan:

If updates fail, the current setup still works for:
- Basic text generation
- API integration
- Frontend functionality
- Database operations

## Next Steps

1. **Immediate**: Current setup is functional for development
2. **Short-term**: Consider Python upgrade for full Gemini support
3. **Long-term**: Monitor library updates for Python 3.8 compatibility

## Resources

- [Google Generative AI Python Library](https://github.com/google/generative-ai-python)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Python Version Management](https://docs.python.org/3/using/index.html)

---

**Note**: The current setup is fully functional for development and testing. The library update is for enhanced features and better Gemini model support. 