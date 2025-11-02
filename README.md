# BookKeep - PDF Password Unlocker & Transaction Processing System

A Python-based application that unlocks password-protected PDF files and processes transaction data for financial analysis.

## ✅ Current Features (Implemented)

- **🔓 PDF Password Unlocking**: Automatically unlock password-protected PDFs using encrypted password storage
- **🔐 Secure Password Management**: Encrypted password storage with master key encryption
- **📄 PDF Transaction Extraction**: Parse transaction data from unlocked PDFs with intelligent pattern matching
- **📊 CSV Export**: Export extracted transactions to CSV files with incremental naming
- **📁 File Organization**: Organized folder structure for input, output, and unlocked PDFs
- **⚙️ Centralized Configuration**: Easy-to-manage configuration system for file paths
- **🧪 Comprehensive Testing**: Full test suite with mock and real file testing
- **🛠️ CLI Tools**: Command-line interface for password management
- **📊 Test Framework**: Reusable test framework with filtering and reporting

## 🚧 Still To Be Implemented

- **📊 Data Export**: Export transactions to Google Sheets or Excel
- **💰 Financial Calculations**: Calculate totals for income and expenses
- **🔄 Transaction Processing**: Advanced transaction categorization and analysis

## 🎯 Project Overview

This project provides a secure way to unlock password-protected PDF files and extract transaction data for financial analysis. The implementation includes password management, PDF unlocking, intelligent transaction extraction, and CSV export with automatic file naming.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd book_keep
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Password Management

1. **Add passwords to the system:**
```bash
python scripts/password_cli.py
```

2. **View available options:**
   - Add new passwords
   - View all passwords
   - Manage categories
   - Reset encryption

### PDF Unlocking & Transaction Extraction

1. **Place password-protected PDFs in:**
```
pdf_files/input/
```

2. **Run the main application:**
```bash
python main.py
```

3. **The application will:**
   - Unlock password-protected PDFs using stored passwords
   - Extract transaction data from unlocked PDFs
   - Save unlocked PDFs to `pdf_files/unlocked/`
   - Export transactions to CSV files in `pdf_files/output/`
   - Automatically increment filenames to avoid overwriting (e.g., `transactions.csv`, `transactions_1.csv`, `transactions_2.csv`)

### Testing

**Run all tests:**
```bash
python src/tests/run_tests.py
```

**Run specific test suites:**
```bash
# Password Manager tests
python src/tests/test_password_manager.py

# PDF Unlocker tests  
python src/tests/test_pdf_unlocker.py

# Transaction Extractor tests
python src/tests/test_transaction_extractor.py

# Integration tests
python src/tests/test_integration.py
```

**Run tests with filters:**
```bash
# Run specific tests
python src/tests/test_password_manager.py --filter init
python src/tests/test_password_manager.py --filter encrypt
python src/tests/test_pdf_unlocker.py --filter mock
python src/tests/test_transaction_extractor.py --filter pattern_matching
python src/tests/test_transaction_extractor.py --filter incremental_naming

# List available test filters
python src/tests/test_password_manager.py --list
python src/tests/test_transaction_extractor.py --list
```

## 📁 Project Structure

```
book_keep/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 main.py                    # Main application entry point
├── 📁 data/                      # Data files (encrypted)
│   ├── passwords.json           # Encrypted passwords
│   └── master.key              # Encryption key
├── 📁 scripts/                   # Utility scripts
│   └── password_cli.py          # Password management CLI
├── 📁 src/                       # Source code
│   ├── config.py                # Centralized configuration
│   ├── password_manager.py      # Password encryption/decryption
│   ├── pdf_unlocker.py          # PDF unlocking functionality
│   ├── transaction_extractor.py # Transaction data extraction
│   └── 📁 tests/                 # Test files
│       ├── run_tests.py         # Test runner
│       ├── test_runner.py       # Test framework
│       ├── test_password_manager.py
│       ├── test_pdf_unlocker.py
│       ├── test_transaction_extractor.py
│       └── test_integration.py
├── 📁 pdf_files/                 # PDF file storage
│   ├── input/                   # Password-protected PDFs
│   ├── output/                  # Exported transaction CSVs
│   └── unlocked/                # Unlocked PDFs
└── 📁 config/                   # Configuration files
```

## 🔧 Configuration

### Centralized Configuration
All file paths are managed through `src/config.py`. This makes it easy to change directories without modifying multiple files:

```python
from config import Config

# Get directory paths
input_dir = Config.get_pdf_input_dir()      # pdf_files/input
unlocked_dir = Config.get_pdf_unlocked_dir()  # pdf_files/unlocked
output_dir = Config.get_pdf_output_dir()     # pdf_files/output

# Get file paths
passwords_file = Config.get_passwords_file()  # data/passwords.json
master_key = Config.get_master_key_file()    # data/master.key

# Ensure all directories exist
Config.ensure_directories()
```

To customize paths, modify `src/config.py` or pass custom paths when initializing components.

### Password Management

1. **First time setup:**
```bash
python scripts/password_cli.py
```

2. **Add your PDF passwords:**
   - Choose option 2: "Add new password"
   - Enter your PDF password
   - Choose a category (e.g., "bank_passwords")

3. **View all passwords:**
   - Choose option 1: "View all passwords"

### PDF File Setup

1. **Place password-protected PDFs in:**
```
pdf_files/input/
```

2. **After running `main.py`:**
   - Unlocked PDFs will appear in: `pdf_files/unlocked/`
   - Transaction CSV files will appear in: `pdf_files/output/`

### Security Notes

- **`data/passwords.json`** - Contains encrypted passwords (never share!)
- **`data/master.key`** - Encryption key (CRITICAL - never share!)
- Both files are automatically ignored by Git for security

## 🧪 Testing

### Test Framework Features

- **Comprehensive Test Suite**: Unit tests, integration tests, and mock tests
- **Filter Support**: Run specific tests with `--filter` option
- **Mock Testing**: Test PDF unlocker without real files
- **Real File Testing**: Test with actual password-protected PDFs
- **Clear Reporting**: Pass/fail status with detailed error messages

### Available Test Filters

**Password Manager Tests:**
- `init` - Initialization tests
- `encrypt` - Encryption/decryption tests
- `load` - Password loading tests
- `add` - Password addition tests
- `category` - Category management tests
- `file` - File operation tests
- `error` - Error handling tests
- `integration` - Integration workflow tests

**PDF Unlocker Tests:**
- `mock` - Mock data tests (no real files needed)

**Transaction Extractor Tests:**
- `pattern_matching` - Transaction pattern matching tests
- `incremental_naming` - CSV filename incremental naming tests

### Test Examples

```bash
# Run all tests
python src/tests/run_tests.py

# Run specific test with filter
python src/tests/test_password_manager.py --filter encrypt

# List all available test filters
python src/tests/test_password_manager.py --list

# Run integration test
python src/tests/test_integration.py
```

## 📊 Example Output

### Password Management
```
🔐 Password Management CLI
========================

Options:
1. View all passwords
2. Add new password
3. View passwords by category
4. List categories
5. Test password decryption
6. Reset encryption system
7. Encrypt all plain text passwords
8. Exit
```

### Complete PDF Processing Workflow
```
🚀 BookKeep - Complete PDF Processing System
==================================================

📄 Step 1: Checking for PDF files...
✅ Found 1 PDF file(s):
  1. tng_ewallet_transactions.pdf

🔑 Step 2: Loading passwords...
✅ Loaded 1 passwords from 1 categories

🔓 Step 3: Unlocking PDFs...
✅ Successfully unlocked 1/1 PDFs

📊 Step 4: Extracting transactions to CSV...
✅ Extracted 246 transactions from 'tng_ewallet_transactions.pdf' to 'tng_ewallet_transactions_transactions.csv'

📈 Step 5: Transaction Extraction Results
------------------------------
CSV Files Generated: 1

📁 Generated Files:
  - tng_ewallet_transactions_transactions.csv

🎉 Transaction extraction complete! Check 'pdf_files/output/' for CSV files
```

### Test Results
```
🚀 BookKeep Test Suite
============================================================
🧪 Running: src/tests/test_password_manager.py
✅ PASSED - test_password_manager.py

🧪 Running: src/tests/test_pdf_unlocker.py  
✅ PASSED - test_pdf_unlocker.py

🧪 Running: src/tests/test_transaction_extractor.py
✅ PASSED - test_transaction_extractor.py

🧪 Running: src/tests/test_transaction_parser.py
✅ PASSED - test_transaction_parser.py

🧪 Running: src/tests/test_integration.py
✅ PASSED - test_integration.py

============================================================
📊 TEST SUMMARY
============================================================
✅ PASSED - src/tests/test_password_manager.py
✅ PASSED - src/tests/test_pdf_unlocker.py
✅ PASSED - src/tests/test_transaction_extractor.py
✅ PASSED - src/tests/test_transaction_parser.py
✅ PASSED - src/tests/test_integration.py

📈 Results: 5 passed, 0 failed
🎉 All tests passed!
```

## 🛡️ Security & Error Handling

### Security Features
- **Encrypted Password Storage**: All passwords encrypted with Fernet encryption
- **Master Key Protection**: Separate master key file for encryption
- **Git Ignore**: Sensitive files automatically excluded from version control
- **Secure File Handling**: Proper cleanup of temporary files

### Error Handling
The application includes robust error handling for:
- **Invalid PDF files**: Graceful handling of corrupted or invalid PDFs
- **Encryption errors**: Automatic key regeneration if master key is corrupted
- **File permission errors**: Clear error messages for file access issues
- **Password decryption errors**: Fallback to plain text if decryption fails
- **Missing dependencies**: Clear error messages for missing libraries
- **Transaction extraction errors**: Handles malformed PDF data gracefully
- **File collision errors**: Automatic filename incrementation prevents overwriting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review the example files

## 🗺️ Roadmap

### Phase 1: PDF Unlocking (✅ COMPLETED)
- [x] Password-protected PDF unlocking
- [x] Encrypted password storage
- [x] Secure password management
- [x] Comprehensive testing framework

### Phase 2: Transaction Processing (✅ COMPLETED)
- [x] PDF text extraction from unlocked PDFs
- [x] Intelligent transaction data parsing with pattern matching
- [x] Date, status, type, amount, and balance extraction
- [x] CSV export with incremental file naming
- [x] Centralized configuration system

### Phase 3: Data Export (📋 PLANNED)
- [ ] Excel export functionality
- [ ] Google Sheets integration
- [ ] Financial calculations
- [ ] Summary reports

### Phase 4: Advanced Features (🔮 FUTURE)
- [ ] Web interface
- [ ] Machine learning for categorization
- [ ] Multi-currency support
- [ ] Integration with accounting software

## 📝 Changelog

### Version 0.3.0 (Current)
- ✅ PDF transaction extraction with intelligent pattern matching
- ✅ CSV export with automatic incremental file naming
- ✅ Centralized configuration system for easy path management
- ✅ Enhanced transaction type detection (handles split words like DUITNOW_RECEIVEFROM)
- ✅ Complete test coverage including incremental naming tests
- ✅ Fixed PDF unlocker mock tests to properly test functionality

### Version 0.2.0
- ✅ PDF password unlocking with encrypted storage
- ✅ Comprehensive test framework with filtering
- ✅ Password management CLI
- ✅ Organized file structure
- ✅ Security features (encryption, git ignore)

### Version 0.1.0
- ✅ Basic project structure
- ✅ Initial requirements and setup
