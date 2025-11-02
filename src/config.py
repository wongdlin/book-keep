#!/usr/bin/env python3
"""
Configuration module for BookKeep
Centralizes all file paths and settings
"""
from pathlib import Path
from typing import Optional

class Config:
    """Centralized configuration for BookKeep"""
    
    # Project root directory
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # PDF file directories
    PDF_INPUT_DIR = PROJECT_ROOT / "pdf_files" / "input"
    PDF_UNLOCKED_DIR = PROJECT_ROOT / "pdf_files" / "unlocked"
    PDF_OUTPUT_DIR = PROJECT_ROOT / "pdf_files" / "output"
    
    # Data directories
    DATA_DIR = PROJECT_ROOT / "data"
    PASSWORDS_FILE = DATA_DIR / "passwords.json"
    MASTER_KEY_FILE = DATA_DIR / "master.key"
    
    # Config directories
    CONFIG_DIR = PROJECT_ROOT / "config"
    
    @staticmethod
    def get_pdf_input_dir() -> Path:
        """Get PDF input directory path"""
        return Config.PDF_INPUT_DIR
    
    @staticmethod
    def get_pdf_unlocked_dir() -> Path:
        """Get PDF unlocked directory path"""
        return Config.PDF_UNLOCKED_DIR
    
    @staticmethod
    def get_pdf_output_dir() -> Path:
        """Get PDF output directory path"""
        return Config.PDF_OUTPUT_DIR
    
    @staticmethod
    def get_passwords_file() -> Path:
        """Get passwords file path"""
        return Config.PASSWORDS_FILE
    
    @staticmethod
    def get_master_key_file() -> Path:
        """Get master key file path"""
        return Config.MASTER_KEY_FILE
    
    @staticmethod
    def get_data_dir() -> Path:
        """Get data directory path"""
        return Config.DATA_DIR
    
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist"""
        directories = [
            Config.PDF_INPUT_DIR,
            Config.PDF_UNLOCKED_DIR,
            Config.PDF_OUTPUT_DIR,
            Config.DATA_DIR,
            Config.CONFIG_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("✅ All required directories verified/created")
    
    @staticmethod
    def get_relative_path(path: Path) -> str:
        """Convert absolute path to relative path from project root"""
        try:
            return str(path.relative_to(Config.PROJECT_ROOT))
        except ValueError:
            return str(path)

