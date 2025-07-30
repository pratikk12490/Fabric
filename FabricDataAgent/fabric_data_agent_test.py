import requests
import json
import pprint
import typing as t
import time
import uuid
import os

from openai import OpenAI
from openai._exceptions import APIStatusError
from openai._models import FinalRequestOptions
from openai._types import Omit
from openai._utils import is_given
from colorama import init, Fore, Back, Style

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not available, continue without it

# Import our auth helper for dynamic token retrieval
from auth_helper import get_fabric_token

# Initialize colorama for cross-platform colored output
init(autoreset=True)
 
# Configuration - Load from environment variables for security
base_url = os.getenv(
    'FABRIC_DATA_AGENT_URL', 
    'https://your-fabric-endpoint.fabric.microsoft.com/v1/workspaces/YOUR_WORKSPACE_ID/aiskills/YOUR_SKILL_ID/aiassistant/openai'
)
question = os.getenv('FABRIC_TEST_QUESTION', 'What datasources do you have access to?')

# Validate configuration
if 'YOUR_WORKSPACE_ID' in base_url or 'YOUR_SKILL_ID' in base_url:
    print(f"{Fore.RED}❌ ERROR: Please set the FABRIC_DATA_AGENT_URL environment variable with your actual Fabric data agent URL!")
    print(f"{Fore.YELLOW}💡 Example: set FABRIC_DATA_AGENT_URL=https://api.fabric.microsoft.com/v1/workspaces/your-workspace-id/aiskills/your-skill-id/aiassistant/openai")
    print(f"{Fore.CYAN}🔍 Check your Fabric workspace settings for the correct URL")
    import sys
    sys.exit(1)

# Create OpenAI Client
class FabricOpenAI(OpenAI):
    def __init__(
        self,
        api_version: str = "2024-05-01-preview",
        **kwargs: t.Any,
    ) -> None:
        self.api_version = api_version
        default_query = kwargs.pop("default_query", {})
        default_query["api-version"] = self.api_version
        super().__init__(
            api_key="",
            base_url=base_url,
            default_query=default_query,
            **kwargs,
        )
    
    def _prepare_options(self, options: FinalRequestOptions) -> None:
        headers: dict[str, str | Omit] = (
            {**options.headers} if is_given(options.headers) else {}
        )
        options.headers = headers
        # Use dynamic token retrieval
        token = get_fabric_token()
        headers["Authorization"] = f"Bearer {token}"
        if "Accept" not in headers:
            headers["Accept"] = "application/json"
        if "ActivityId" not in headers:
            correlation_id = str(uuid.uuid4())
            headers["ActivityId"] = correlation_id

        return super()._prepare_options(options)

# Pretty printing helper with jazzy colors
def pretty_print(messages):
    print(f"\n{Fore.CYAN}{'='*20} 💬 CONVERSATION {'='*20}{Style.RESET_ALL}")
    for m in messages:
        if m.role == "user":
            print(f"{Fore.GREEN}🙋 User:{Style.RESET_ALL} {Fore.WHITE}{m.content[0].text.value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.MAGENTA}🤖 Assistant:{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}{m.content[0].text.value}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

def main():
    try:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🚀 FABRIC DATA AGENT TESTING SUITE 🚀{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}✨ Initializing Fabric OpenAI client...{Style.RESET_ALL}")
        fabric_client = FabricOpenAI()
        
        # Create assistant
        print(f"{Fore.BLUE}🎭 Creating assistant...{Style.RESET_ALL}")
        assistant = fabric_client.beta.assistants.create(model="not used")
        print(f"{Fore.GREEN}✅ Assistant created with ID: {Fore.WHITE}{assistant.id}{Style.RESET_ALL}")
        
        # Create thread
        print(f"{Fore.BLUE}🧵 Creating conversation thread...{Style.RESET_ALL}")
        thread = fabric_client.beta.threads.create()
        print(f"{Fore.GREEN}✅ Thread created with ID: {Fore.WHITE}{thread.id}{Style.RESET_ALL}")
        
        # Create message on thread
        print(f"{Fore.MAGENTA}💭 Sending question: {Fore.LIGHTYELLOW_EX}'{question}'{Style.RESET_ALL}")
        message = fabric_client.beta.threads.messages.create(
            thread_id=thread.id, 
            role="user", 
            content=question
        )
        
        # Create run
        print(f"{Fore.BLUE}⚡ Creating run...{Style.RESET_ALL}")
        run = fabric_client.beta.threads.runs.create(
            thread_id=thread.id, 
            assistant_id=assistant.id
        )
        print(f"{Fore.GREEN}✅ Run created with ID: {Fore.WHITE}{run.id}{Style.RESET_ALL}")
        
        # Wait for run to complete
        print(f"{Fore.YELLOW}⏳ Waiting for AI magic to happen...{Style.RESET_ALL}")
        spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        spinner_idx = 0
        
        while run.status == "queued" or run.status == "in_progress":
            run = fabric_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            spinner = spinner_chars[spinner_idx % len(spinner_chars)]
            print(f"\r{Fore.CYAN}{spinner} Status: {Fore.YELLOW}{run.status.upper()}{Style.RESET_ALL}", end="", flush=True)
            spinner_idx += 1
            time.sleep(0.5)
        
        print(f"\r{Fore.GREEN}🎉 Run completed with status: {Fore.LIGHTGREEN_EX}{run.status.upper()}{Style.RESET_ALL}")
        
        # Print messages
        print(f"{Fore.CYAN}📥 Retrieving response...{Style.RESET_ALL}")
        response = fabric_client.beta.threads.messages.list(
            thread_id=thread.id, 
            order="asc"
        )
        pretty_print(response)
        
        # Delete thread
        print(f"{Fore.BLUE}🧹 Cleaning up resources...{Style.RESET_ALL}")
        fabric_client.beta.threads.delete(thread_id=thread.id)
        print(f"{Fore.GREEN}✨ Thread deleted successfully!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🎊 ALL DONE! Have a great day! 🎊{Style.RESET_ALL}\n")
        
    except APIStatusError as e:
        print(f"{Fore.RED}❌ API Error: {Fore.LIGHTRED_EX}{e.status_code} - {e.message}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}💥 Unexpected Error: {Fore.LIGHTRED_EX}{str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
