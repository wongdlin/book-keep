# BookKeep - PDF Password Unlocker & Transaction Processing System

A Python-based application that unlocks password-protected PDF files and processes transaction data for financial analysis.

## ✅ Current Features (Implemented)

- **🔓 PDF Password Unlocking**: Automatically unlock password-protected PDFs using encrypted password storage
- **🔐 Secure Password Management**: Encrypted password storage with master key encryption
- **📁 File Organization**: Organized folder structure for input, output, and unlocked PDFs
- **🧪 Comprehensive Testing**: Full test suite with mock and real file testing
- **🛠️ CLI Tools**: Command-line interface for password management
- **📊 Test Framework**: Reusable test framework with filtering and reporting

## 🚧 Still To Be Implemented

- **📄 PDF Transaction Extraction**: Parse transaction data from unlocked PDFs
- **📊 Data Export**: Export transactions to Google Sheets or Excel
- **💰 Financial Calculations**: Calculate totals for income and expenses
- **🔄 Transaction Processing**: Structure and categorize transaction data

## 🎯 Project Overview

This project provides a secure way to unlock password-protected PDF files and will eventually extract transaction data for financial analysis. The current implementation focuses on the PDF unlocking and password management infrastructure.

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

### PDF Unlocking

1. **Place password-protected PDFs in:**
```
pdf_files/input/
```

2. **Run the main application:**
```bash
python main.py
```

3. **Unlocked PDFs will be saved to:**
```
pdf_files/unlocked/
```

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

# Integration tests
python src/tests/test_integration.py
```

**Run tests with filters:**
```bash
# Run specific tests
python src/tests/test_password_manager.py --filter init
python src/tests/test_password_manager.py --filter encrypt
python src/tests/test_pdf_unlocker.py --filter mock

# List available test filters
python src/tests/test_password_manager.py --list
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
│   ├── password_manager.py      # Password encryption/decryption
│   ├── pdf_unlocker.py          # PDF unlocking functionality
│   └── 📁 tests/                 # Test files
│       ├── run_tests.py         # Test runner
│       ├── test_runner.py       # Test framework
│       ├── test_password_manager.py
│       ├── test_pdf_unlocker.py
│       └── test_integration.py
├── 📁 pdf_files/                 # PDF file storage
│   ├── input/                   # Password-protected PDFs
│   ├── output/                  # Processed PDFs (future)
│   └── unlocked/                # Unlocked PDFs
└── 📁 config/                   # Configuration files
```

## 🔧 Configuration

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

2. **Unlocked PDFs will appear in:**
```
pdf_files/unlocked/
```

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

### PDF Unlocking Process
```
🔓 Testing PDF Unlocker
======================

📄 Found 1 PDF file(s):
  1. tng_ewallet_transactions.pdf

🔑 Testing with 1 passwords from passwords.json...
PDF is encrypted. Trying passwords...
Trying password 1/1: 162407577
Password 162407577 unlocked the PDF.
PDF tng_ewallet_transactions.pdf unlocked successfully with password: 162407577
Unlocked PDF saved to: tng_ewallet_transactions.pdf

📊 Summary: 1/1 PDFs processed successfully
```

### Test Results
```
🔑 Testing Password Manager - Comprehensive Unit Tests
============================================================

✅ PASSED - Initialization
✅ PASSED - Encryption/Decryption  
✅ PASSED - Password Loading
✅ PASSED - Password Addition
✅ PASSED - Category Management
✅ PASSED - File Operations
✅ PASSED - Error Handling
✅ PASSED - Integration Test

📈 Total: 8 passed, 0 failed
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

### Phase 2: Transaction Processing (🚧 IN PROGRESS)
- [ ] PDF text extraction from unlocked PDFs
- [ ] Transaction data parsing
- [ ] Date and amount extraction
- [ ] Transaction categorization

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

### Version 0.2.0 (Current)
- ✅ PDF password unlocking with encrypted storage
- ✅ Comprehensive test framework with filtering
- ✅ Password management CLI
- ✅ Organized file structure
- ✅ Security features (encryption, git ignore)

### Version 0.1.0
- ✅ Basic project structure
- ✅ Initial requirements and setup
