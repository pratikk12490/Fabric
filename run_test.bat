@echo off
echo Activating Fabric Data Agent virtual environment...
call .\fabric_env\Scripts\activate.bat

echo.
echo Checking environment configuration...
if "%FABRIC_DATA_AGENT_URL%"=="" (
    echo WARNING: FABRIC_DATA_AGENT_URL environment variable not set!
    echo Please set it with your actual Fabric data agent URL:
    echo set FABRIC_DATA_AGENT_URL=https://api.fabric.microsoft.com/v1/workspaces/YOUR_WORKSPACE_ID/aiskills/YOUR_SKILL_ID/aiassistant/openai
    echo.
    echo Continuing with default configuration...
)

echo.
echo Running Fabric Data Agent test...
python fabric_data_agent_test.py

echo.
echo Deactivating virtual environment...
call deactivate

pause
