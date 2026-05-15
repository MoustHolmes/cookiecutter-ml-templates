# GitHub Copilot Custom Instructions

## Project Philosophy
This is a bare bones machine learning project template created using cookiecutter, focused on establishing well-structured machine learning projects with minimal initial code. The template emphasizes best practices, modern tooling, and clean project organization.

## Code Style & Structure
- Follow test-driven development: Write unit tests for all critical components (datasets, models, training loops)
- Always document input/output tensor shapes in machine learning code
- Use type hints and docstrings (Google style) consistently
- Keep code modular and follow the project structure defined in the template
- Utilize callbacks for non-essential functionality in training loops
- Follow PEP 8 guidelines with Ruff and Black formatting

## Template Structure
Standard project structure includes:
- configs/ - Hydra configuration files
- data/ - Dataset storage (raw and processed)
- src/ - Main source code
  - models/ - Model definitions
  - data/ - Dataset and data processing code
- tests/ - Unit tests
- notebooks/ - Development and analysis notebooks

## Best Practices
- Write comprehensive tests for all new features
- Document significant decisions and approaches
- Use Hydra for configuration management
- Implement proper logging with Weights & Biases
- Create reusable components through callbacks
- Handle errors gracefully and provide informative messages

## Dependencies & Tools
Primary tools and frameworks:
- PyTorch Lightning for training structure
- Hydra for configuration
- Weights & Biases for experiment tracking
- pytest for testing
- Ruff and Black for code quality
- Material for MkDocs for documentation

## When Implementing Features
1. Start with a clear roadmap/plan
2. Write tests first (TDD approach)
3. Document input/output expectations
4. Include appropriate logging and metrics
5. Add necessary configuration options
6. Update documentation

## Things to Avoid
- Do not start implementing new features without clear requirements
- Avoid hardcoding parameters that should be in config files
- Don't skip writing tests for critical components
- Don't implement features that deviate from the template's purpose
- Avoid unnecessary dependencies

Remember: This is a minimal template designed to help you start your ML project with proper structure and best practices. Build upon this foundation by adding only what you need for your specific use case.
