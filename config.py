from typing import Any, Dict
import os
import json
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Application configuration"""
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Metrics configuration
    metrics:
        enabled: bool = True
        retention_days: int = 7
        
    # Logging configuration
    logging:
        level: str = "info"
        format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
    # Rate limiting configuration
    rate_limiting:
        default_limit: int = 100
        default_window_seconds: int = 60
        
    # Cache configuration
    cache:
        enabled: bool = True
        max_size: int = 1024
        expiration_seconds: int = 3600
        
    # Database configuration
    database:
        url: str = "sqlite:///:memory:"
        pool_size: int = 5
        
    # Model configuration
    model:
        max_input_tokens: int = 4096
        max_output_tokens: int = 2048
        
    def load(self, config_path: str = "config.json"):
        """Load configuration from file"""
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = json.load(f)
            self.__dict__.update(config_data)
            logger.info(f"Loaded configuration from {config_path}")
        else:
            logger.warning(f"Configuration file {config_path} not found, using defaults")

    def save(self, config_path: str = "config.json"):
        """Save configuration to file"""
        with open(config_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
            logger.info(f"Saved configuration to {config_path}")