import os
import re
import json
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from typing import (
    IO,
    Optional,
    Union,
    Any,
    Dict,
    List,
    Tuple,
    Callable,
    TypeVar,
    Generic,
)


# Convenience functions
def load_env(env_file: Optional[str] = None) -> bool:
    """
    Load environment variables from .env file

    Args:
        env_file (str, optional): Path to .env file

    Returns:
        bool: True if .env file was found and loaded, False otherwise
    """
    loader = EnvLoader(env_file)
    return loader.load()


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable value"""
    return os.getenv(key, default)


def require_env(key: str) -> str:
    """Get environment variable value or raise exception if not found"""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


class EnvLoader:
    """Environment variables loader with enhanced functionality"""

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize EnvLoader

        Args:
            env_file (str, optional): Path to .env file. If None, will search automatically.
        """
        self.env_file = env_file or find_dotenv()
        self.loaded = False

    def load(self) -> bool:
        """
        Load environment variables from .env file

        Returns:
            bool: True if .env file was found and loaded, False otherwise
        """
        if self.env_file and os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            self.loaded = True
            print(f"Environment variables loaded from: {self.env_file}")
            return True
        else:
            print("No .env file found")
            return False

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable value

        Args:
            key (str): Environment variable name
            default (str, optional): Default value if variable not found

        Returns:
            str: Environment variable value or default
        """
        return os.getenv(key, default)

    def require(self, key: str) -> str:
        """
        Get environment variable value or raise exception if not found

        Args:
            key (str): Environment variable name

        Returns:
            str: Environment variable value

        Raises:
            ValueError: If environment variable is not set
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get environment variable as integer

        Args:
            key (str): Environment variable name
            default (int): Default value

        Returns:
            int: Environment variable as integer
        """
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            print(
                f"Warning: Could not convert {key}='{value}' to integer, using default {default}"
            )
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get environment variable as boolean

        Args:
            key (str): Environment variable name
            default (bool): Default value

        Returns:
            bool: Environment variable as boolean
        """
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    def all_vars(self) -> Dict[str, str]:
        """
        Get all environment variables (filtered to avoid sensitive data exposure)

        Returns:
            Dict[str, str]: Dictionary of environment variables
        """
        # Only return non-sensitive variables (you can customize this filter)
        sensitive_keywords = ["key", "secret", "password", "token"]
        return {
            k: v
            for k, v in os.environ.items()
            if not any(keyword in k.lower() for keyword in sensitive_keywords)
        }
