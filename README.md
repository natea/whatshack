# Township Connect - WhatsApp Assistant

A WhatsApp-native assistant designed to empower Cape Town township residents by providing easy-to-use, data-light tools for running daily businesses, accessing vital services, and learning new skills directly through WhatsApp.

## Project Overview

Township Connect is a WhatsApp-based platform that aims to lower the barriers to digital and economic participation for township residents in Cape Town. It offers accessible, affordable, and multilingual functionalities for financial transactions, business management, logistics, information access, and skill development.

### Key Features

- **Account Management & Onboarding:** QR code pairing, language auto-detection, POPIA compliance
- **Business & Finance Tools:** Payment link generation, sales logging, expense tracking
- **Logistics & Information Access:** Parcel tracking, map directions, Q&A capability
- **Learning & Upskilling:** Business tips, compliance guides, multi-language content

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/natea/whatshack.git
   cd township-connect
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Testing

This project follows Test-Driven Development (TDD) practices. Tests are written using pytest.

### Running Tests

To run all tests:
```
pytest
```

To run tests with coverage report:
```
pytest --cov=src tests/
```

To run specific test categories:
```
pytest -m smoke        # Run smoke tests only
pytest -m unit         # Run unit tests only
pytest -m integration  # Run integration tests only
```

### Setting Up Test Environment

For integration tests that require Supabase connectivity:

1. Create a `.env.test` file in the `tests/` directory:
   ```
   cp tests/.env.test.example tests/.env.test
   # Edit tests/.env.test with your test Supabase credentials
   ```

2. Alternatively, set the environment variables directly:
   ```
   export SUPABASE_URL=your-test-supabase-url
   export SUPABASE_SERVICE_KEY=your-test-service-key
   ```

Integration tests will be skipped if these environment variables are not available.

### Test Structure

- `tests/test_smoke.py`: Basic smoke tests to verify imports and core functionality
- `tests/test_core_handler.py`: Tests for the core message handling functionality
- `tests/test_language_detection.py`: Tests for language detection features

## Project Structure

```
township-connect/
├── .github/                # GitHub Actions workflows
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Application entry point
│   └── core_handler.py     # Core message handling
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures and configuration
│   └── test_*.py           # Test modules
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
├── pytest.ini              # Pytest configuration
├── README.md               # This file
└── requirements.txt        # Project dependencies
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Commit your changes: `git commit -m "Add your feature"`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Submit a pull request

## License

[Add license information here]