# Contributing to RealSim

Thank you for your interest in contributing to RealSim! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Simulations.git
   cd Simulations
   ```
3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines below

3. **Test your changes**:
   ```bash
   # Run tests
   pytest tests/

   # Test the desktop app
   python app.py

   # Test the web app
   streamlit run streamlit_app.py
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function parameters and return values
- Maximum line length: 120 characters
- Use meaningful variable and function names

### Code Organization

```
simulations/
├── core/           # Core simulation engine
├── warehouse/      # Warehouse-specific logic
└── __init__.py

examples/           # Example scripts and agents
tests/              # Unit tests
docs/               # Documentation
```

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: int, param2: str) -> bool:
    """Brief description of function.

    More detailed description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When and why this is raised
    """
    pass
```

## Types of Contributions

### 🐛 Bug Reports

Open an issue with:
- Clear title describing the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Screenshots if applicable

### ✨ Feature Requests

Open an issue with:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (optional)
- Any potential drawbacks

### 🎨 New Environments

To add a new simulation environment:

1. Create a new directory under `simulations/`
2. Implement a Gymnasium-compatible environment
3. Add configuration files to `configs/`
4. Create example scripts in `examples/`
5. Document the environment in `docs/`

### 🤖 New RL Algorithms

To add a new RL algorithm:

1. Create a new file in `examples/`
2. Implement the agent interface
3. Add unit tests
4. Create an example training script
5. Document the algorithm

### 📚 Documentation

Improvements to documentation are always welcome:
- Fix typos or unclear explanations
- Add tutorials or examples
- Improve API documentation
- Translate to other languages

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_entity_geometry.py

# Run with coverage
pytest --cov=simulations tests/
```

### Writing Tests

- Place tests in `tests/` directory
- Use `pytest` framework
- Aim for >80% code coverage
- Test edge cases and error conditions

## Pull Request Process

1. **Update documentation** if you've changed APIs
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Keep commits focused** - one logical change per commit
6. **Write clear commit messages**:
   - Use imperative mood ("Add feature" not "Added feature")
   - First line: brief summary (<50 chars)
   - Optional body: detailed explanation

### Commit Message Format

```
Type: Brief summary (50 chars or less)

More detailed explanatory text, if necessary. Wrap at 72 characters.

- Bullet points are okay
- Use dashes for bullets

Fixes #123
```

Types: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Doc`, `Test`

## Code Review

All submissions require review. We aim to:
- Provide feedback within 48 hours
- Be respectful and constructive
- Focus on code quality, not personal preference

## Community Guidelines

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person
- Assume good intentions

## Questions?

- Open an issue with the `question` label
- Check existing issues and documentation first
- Be specific about what you need help with

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked in the community

Thank you for contributing to RealSim! 🚀
