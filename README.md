# 🚀 Fabric Data Agent Testing Suite

*AI-powered data conversations made simple* ✨

## 📁 Project Structure

Everything you need to chat with your Microsoft Fabric Data Agent:

```
FabricDataAgent/
├── 🐍 fabric_data_agent_test.py    # Main testing script
├── 🔐 auth_helper.py               # Smart auth with DefaultAzureCredential
├── 📦 requirements.txt             # Python dependencies
├── 📖 README.md                   # This awesome file
├── 🎯 run_test.bat                # One-click runner
├── 🌐 fabric_env/                 # Virtual environment
├── 🔧 .env.example               # Configuration template
└── 🛡️ .gitignore                 # Security protection
```

## ⚡ Quick Start

### 🏃‍♂️ Super Fast Setup
```bash
cd C:\Projects\Fabric\FabricDataAgent
```

### 🔌 Power Up Your Environment
```bash
.\fabric_env\Scripts\Activate.ps1
```

### ⚙️ Configure Your Data Agent
**IMPORTANT**: Set your Fabric data agent URL before running!

**Option 1: Environment Variables**
```bash
# Windows PowerShell
$env:FABRIC_DATA_AGENT_URL = "https://api.fabric.microsoft.com/v1/workspaces/YOUR_WORKSPACE_ID/aiskills/YOUR_SKILL_ID/aiassistant/openai"

# Windows Command Prompt
set FABRIC_DATA_AGENT_URL=https://api.fabric.microsoft.com/v1/workspaces/YOUR_WORKSPACE_ID/aiskills/YOUR_SKILL_ID/aiassistant/openai

# Optional: Customize the test question
$env:FABRIC_TEST_QUESTION = "What data sources do you have access to?"
```

**Option 2: Environment File** (Recommended for development)
```bash
# Copy the example and customize
copy .env.example .env
# Then edit .env with your actual values
```

> 💡 **Where to find your URL**: Navigate to your Fabric workspace → AI Skills → Your data agent → Settings

### 🔑 Authentication Magic
Our script is smart AF! It automatically tries multiple auth methods:
- 🌍 Environment variables (`FABRIC_AUTH_TOKEN`)
- 💻 Azure CLI authentication
- 🛡️ Managed Identity (for Azure deployments)
- 🎨 Visual Studio authentication
- 🔄 And more Azure auth wizardry!

**Pro Tips for Auth Success:**
```bash
# 🚀 Option 1: Azure CLI (Recommended)
az login

# 🎯 Option 2: Environment variable
$env:FABRIC_AUTH_TOKEN="your-secret-token"
```

### 🎬 Showtime!
```bash
# 🎪 Method 1: One-click magic
.\run_test.bat

# 🛠️ Method 2: Manual control
python fabric_data_agent_test.py
```

## 🔥 Features That Slap

- 🤖 **Zero-config authentication** - DefaultAzureCredential does the heavy lifting
- 🔒 **Fort Knox security** - No hardcoded tokens, period!
- 💯 **Bulletproof error handling** - Clear messages when things go sideways
- 🎨 **Instagram-worthy conversation display** - Beautiful chat formatting
- 🧹 **Self-cleaning** - Automatic resource cleanup (Marie Kondo approved)
- ⚡ **Lightning fast** - Optimized for speed and efficiency

## 🎯 Customization Playground

- 💬 **Change the vibe**: Edit the `question` variable in `fabric_data_agent_test.py`
- 🎛️ **Your endpoint, your rules**: Script connects to your specific Fabric data agent
- 📊 **Pretty responses**: All outputs are formatted for maximum readability
- 🔧 **Tweak everything**: Open source = unlimited customization power

## 📊 Your Data Universe

Your AI agent has access to these data goldmines:

### 🗓️ **Date Dimension**
*Time is everything* - Complete date attributes for temporal analysis

### 🌍 **Geography Data** 
*Location, location, location* - Zip codes, cities, states, and more

### 🚗 **HackneyLicense Registry**
*Licensed to thrill* - Comprehensive license information and codes

---

*Built with ❤️ and lots of ☕ for the modern data scientist*
