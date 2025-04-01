# Contributing to Project Organizer

Thank you for your interest in contributing to Project Organizer! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be considerate and constructive in your communication and contributions.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- PyQt5 5.12 or higher
- Git

### Setup for Development

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/ProjectOrganizer.git
   cd ProjectOrganizer
   ```
3. Set up the upstream remote:
   ```bash
   git remote add upstream https://github.com/faridfgx/ProjectOrganizer.git
   ```
4. Create a branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Branching Strategy

- `main` - The production branch containing stable code
- `feature/*` - Feature branches for new features or enhancements
- `bugfix/*` - Branches for bug fixes
- `docs/*` - Branches for documentation improvements

## Development Workflow

1. Make sure your fork is up to date with the upstream repository:
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes, following the coding standards and guidelines

4. Test your changes thoroughly

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request from your branch to the main repository

## Pull Request Process

1. Ensure your code follows the project's coding standards
2. Update the documentation if necessary
3. Include tests for your changes if applicable
4. Ensure all tests pass
5. Submit your pull request with a clear description of the changes

## Coding Standards

### Python Style Guide

- Follow PEP 8 coding style
- Use 4 spaces for indentation (no tabs)
- Use docstrings for all functions, classes, and modules
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Example Function Format

```python
def function_name(param1, param2):
    """Short description of the function
    
    More detailed description if needed.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Description of the return value
    """
    # Function implementation
    result = do_something(param1, param2)
    return result
```

### PyQt Best Practices

- Separate UI setup from business logic
- Use descriptive names for UI elements
- Add tooltips for complex UI elements
- Ensure consistent spacing and margins

### Dark Theme UI Guidelines

- Use the color scheme defined in the `colors` dictionary
- Maintain consistent spacing and padding
- Use rounded corners for UI elements (4-8px radius)
- Follow the existing visual style

## Feature Implementation Guidelines

### Adding a New Module

1. Create a new Python file for your module
2. Implement your feature in a modular way
3. Create an integration function with the naming pattern `add_your_feature`
4. Add your integration function to `dark_theme_integration.py`

### Example Integration Function

```python
def add_my_feature(project_organizer):
    """Add my feature to the project organizer
    
    Args:
        project_organizer: The ProjectOrganizer instance
    """
    # Your integration code here
    
    # Example: Add a new method to the project_organizer instance
    def my_feature_function(self):
        """Implement your feature functionality"""
        # Your feature code here
        pass
    
    project_organizer.my_feature_function = my_feature_function.__get__(project_organizer)
```

## Testing Guidelines

- Test your changes with various project configurations
- Test edge cases (empty projects, many projects, long text)
- Test on different operating systems if possible
- Verify dark theme styling is consistent

## Documentation

When adding a new feature, be sure to update the relevant documentation:

- Update README.md if necessary
- Update or add docstrings to all new functions and classes
- Add tooltips for any new UI elements
- Update the User Guide if your feature adds user-facing functionality

## Submitting Changes

1. Push your changes to your fork
2. Create a pull request against the main repository
3. Describe your changes in detail
4. Reference any related issues
5. Wait for review and address any feedback

## Reporting Bugs

When reporting bugs, please include:

1. A clear description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Screenshots if applicable
6. Your operating system and Python version
7. Any error messages or logs

## Suggesting Enhancements

When suggesting enhancements, please include:

1. A clear description of the proposed feature
2. The motivation for the feature
3. How it would benefit users
4. Any implementation ideas you have

## Reviewing Pull Requests

When reviewing pull requests:

1. Be respectful and constructive
2. Check for adherence to coding standards
3. Verify the feature works as expected
4. Ensure documentation is updated
5. Suggest improvements if necessary

## Development Tools

The following tools can help maintain code quality:

- [Pylint](https://www.pylint.org/) - Python code analysis
- [Black](https://black.readthedocs.io/) - Python code formatter
- [isort](https://pycqa.github.io/isort/) - Import sorter

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

If you have any questions about contributing, please open an issue for discussion.

Thank you for contributing to Project Organizer!