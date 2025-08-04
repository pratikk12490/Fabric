# Fabric Data Agent Testing Suite

A Python testing suite for Microsoft Fabric Data Agent integration.

## Project Structure

```
FabricDataAgent/
├── fabric_data_agent_test.py    # Main testing script
├── auth_helper.py               # Azure authentication helper
├── requirements.txt             # Python dependencies
├── run_test.bat                 # Windows batch runner
├── fabric_env/                  # Virtual environment
├── .env.example                 # Configuration template
└── .gitignore                   # Git ignore rules
```

## Quick Start

### 1. Create Virtual Environment
```bash
# Navigate to project directory
cd FabricDataAgent

# Create virtual environment
python -m venv fabric_env

# Activate virtual environment (Windows PowerShell)
.\fabric_env\Scripts\Activate.ps1

# OR Activate virtual environment (Windows Command Prompt)
.\fabric_env\Scripts\activate.bat
```

### 2. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Configure Data Agent URL
Set your Fabric data agent URL:

**PowerShell:**
```powershell
$env:FABRIC_DATA_AGENT_URL = "https://api.fabric.microsoft.com/v1/workspaces/YOUR_WORKSPACE_ID/aiskills/YOUR_SKILL_ID/aiassistant/openai"
```

**Command Prompt:**
```cmd
set FABRIC_DATA_AGENT_URL=https://api.fabric.microsoft.com/v1/workspaces/YOUR_WORKSPACE_ID/aiskills/YOUR_SKILL_ID/aiassistant/openai
```

### 4. Authentication

The application supports multiple authentication methods through Azure DefaultAzureCredential:

**Option 1: Azure CLI (Interactive)**
```bash
az login
```

**Option 2: Service Principal (Automated/Production)**

Set these environment variables for Service Principal authentication:
```bash
# PowerShell
$env:AZURE_CLIENT_ID = "your-application-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"  
$env:AZURE_TENANT_ID = "your-tenant-id"

# Command Prompt
set AZURE_CLIENT_ID=your-application-id
set AZURE_CLIENT_SECRET=your-client-secret
set AZURE_TENANT_ID=your-tenant-id
```

**Option 3: Environment File (.env)**

Add to your `.env` file:
```
AZURE_CLIENT_ID=your-application-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```

**How to get Service Principal details:**
1. Azure Portal → Azure Active Directory → App registrations
2. Create or select your application
3. Get Application (client) ID → `AZURE_CLIENT_ID`
4. Get Directory (tenant) ID → `AZURE_TENANT_ID`
5. Create new client secret → `AZURE_CLIENT_SECRET`

### 5. Run Tests
```bash
# Using batch file
.\run_test.bat

# Direct execution
python fabric_data_agent_test.py
```

## Features

- **Azure Authentication**: Uses DefaultAzureCredential for secure authentication
- **Environment Configuration**: Environment variables for secure configuration
- **Error Handling**: Clear error messages and validation
- **Conversation Display**: Formatted chat output
- **Resource Cleanup**: Automatic cleanup of resources

## Configuration

Copy `.env.example` to `.env` and update with your values:
```
FABRIC_DATA_AGENT_URL=your-fabric-endpoint-url
FABRIC_TEST_QUESTION=What datasources do you have access to?

# Optional: Service Principal Authentication
AZURE_CLIENT_ID=your-application-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```

## Requirements

See `requirements.txt` for complete list:
- openai>=1.0.0
- azure-identity>=1.12.0
- requests>=2.25.0
- colorama>=0.4.6
- python-dotenv>=0.19.0
