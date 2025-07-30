"""
Azure Authentication Helper for Fabric Data Agent

This module provides different ways to obtain authentication tokens for Microsoft Fabric.
"""

import os
import subprocess
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def get_token_from_env():
    """Get token from environment variable."""
    return os.getenv('FABRIC_AUTH_TOKEN')

def get_token_from_azure_cli():
    """Get token using Azure CLI."""
    try:
        result = subprocess.run(
            ['az', 'account', 'get-access-token', '--resource', 'https://api.fabric.microsoft.com'],
            capture_output=True,
            text=True,
            check=True
        )
        token_info = json.loads(result.stdout)
        return token_info['accessToken']
    except FileNotFoundError:
        print(f"{Fore.YELLOW}⚠️  Azure CLI not found. Install Azure CLI or use alternative authentication methods.{Style.RESET_ALL}")
        return None
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
        print(f"{Fore.RED}❌ Error getting token from Azure CLI: {e}{Style.RESET_ALL}")
        return None

def get_token_from_azure_identity():
    """Get token using Azure Identity library with DefaultAzureCredential."""
    try:
        from azure.identity import DefaultAzureCredential
        
        # Use DefaultAzureCredential which tries multiple authentication methods
        credential = DefaultAzureCredential()
        token = credential.get_token("https://api.fabric.microsoft.com/.default")
        return token.token
    except ImportError:
        print(f"{Fore.YELLOW}⚠️  Azure Identity library not installed. Install with: pip install azure-identity{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Error getting token from Azure Identity (DefaultAzureCredential): {e}{Style.RESET_ALL}")
        return None

def get_fabric_token():
    """
    Try multiple methods to get a Fabric authentication token.
    Returns the first successful token found or raises an error if none work.
    """
    # Method 1: Environment variable
    token = get_token_from_env()
    if token and token != 'your-auth-token-here':
        print(f"{Fore.GREEN}🔑 Using token from environment variable{Style.RESET_ALL}")
        return token
    
    # Method 2: Azure Identity library (DefaultAzureCredential)
    # This tries multiple methods: managed identity, Azure CLI, Visual Studio, etc.
    token = get_token_from_azure_identity()
    if token:
        print(f"{Fore.CYAN}🔐 Using token from Azure Identity (DefaultAzureCredential){Style.RESET_ALL}")
        return token
    
    # Method 3: Azure CLI (as fallback)
    token = get_token_from_azure_cli()
    if token:
        print(f"{Fore.BLUE}💻 Using token from Azure CLI{Style.RESET_ALL}")
        return token
    
    # If all methods fail, raise an error
    raise ValueError(
        f"{Fore.RED}❌ Could not obtain authentication token. Please ensure one of the following:\n"
        f"{Fore.YELLOW}1. Set FABRIC_AUTH_TOKEN environment variable\n"
        f"2. Login with Azure CLI: az login\n"
        f"3. Use managed identity or other Azure authentication methods\n"
        f"4. Ensure you have proper permissions for https://api.fabric.microsoft.com{Style.RESET_ALL}"
    )

if __name__ == "__main__":
    # Test the token retrieval
    token = get_fabric_token()
    if token and token != 'your-auth-token-here':
        print(f"{Fore.GREEN}🎉 Successfully obtained token: {Fore.WHITE}{token[:20]}...{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}💥 Failed to obtain token{Style.RESET_ALL}")
