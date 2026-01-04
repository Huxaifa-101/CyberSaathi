# Contributing to CyberSaathi

First off, thank you for considering contributing to CyberSaathi! 🎉

It's people like you that make CyberSaathi a great tool for understanding Pakistani cyber laws. We welcome contributions from everyone, whether you're fixing a typo, adding a feature, or improving documentation.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 11, macOS 14, Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - Node Version: [e.g. 18.16.0]
 - Browser: [e.g. Chrome 120, Firefox 121]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

**Enhancement Template:**
```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features.

**Additional context**
Add any other context or screenshots about the feature request here.
```

### Contributing Code

1. **Bug Fixes**: Always welcome!
2. **New Features**: Please open an issue first to discuss
3. **Documentation**: Improvements are always appreciated
4. **Tests**: Adding tests is highly valued

### Contributing Documentation

- Fix typos or clarify existing documentation
- Add examples and use cases
- Translate documentation (Urdu translations welcome!)
- Create tutorials or guides

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **Git**: Latest version
- **Code Editor**: VSCode recommended

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
```bash
git clone https://github.com/YOUR_USERNAME/CyberSaathi.git
cd CyberSaathi
```

3. **Add upstream remote**:
```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/CyberSaathi.git
```

### Backend Setup

```bash
cd CyberSaathi_BackEnd

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Run tests (if available)
pytest

# Start development server
uvicorn api:api --reload
```

### Frontend Setup

```bash
cd CyberSaathi_FrontEnd

# Install dependencies
npm install

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

---

## 🔄 Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
# or
git checkout -b docs/documentation-update
```

**Branch Naming Convention:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks

### 2. Make Your Changes

- Write clean, readable code
- Follow the style guidelines (see below)
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and focused

### 3. Test Your Changes

**Backend Testing:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=.
```

**Frontend Testing:**
```bash
# Run tests
npm test

# Run linter
npm run lint

# Type check
npm run typecheck
```

### 4. Commit Your Changes

See [Commit Messages](#commit-messages) section below.

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## 🎨 Style Guidelines

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line Length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized in groups (standard library, third-party, local)

**Example:**
```python
"""
Module docstring explaining the purpose.
"""
import os
from typing import List, Dict

from langchain_core.messages import HumanMessage
from fastapi import FastAPI

from config import Config
from tools.law_retriever import get_law_retriever


class MyClass:
    """Class docstring."""
    
    def __init__(self, name: str):
        """Initialize with name."""
        self.name = name
    
    def process_query(self, query: str) -> Dict[str, str]:
        """
        Process a user query.
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        # Implementation here
        pass
```

**Tools:**
- Use `black` for formatting: `black .`
- Use `flake8` for linting: `flake8 .`
- Use `mypy` for type checking: `mypy .`

### TypeScript/JavaScript Style Guide

We follow **Airbnb JavaScript Style Guide** with TypeScript:

- **Indentation**: 2 spaces
- **Quotes**: Single quotes for strings
- **Semicolons**: Required
- **Trailing Commas**: Always

**Example:**
```typescript
import { useState, useEffect } from 'react';
import { Message } from '../types';

interface ChatProps {
  onSend: (message: string) => void;
}

export default function Chat({ onSend }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  
  useEffect(() => {
    // Effect logic
  }, []);
  
  const handleSubmit = (content: string) => {
    // Handle submission
    onSend(content);
  };
  
  return (
    <div className="chat-container">
      {/* JSX content */}
    </div>
  );
}
```

**Tools:**
- Use `eslint` for linting: `npm run lint`
- Use `prettier` for formatting: `npm run format`
- Use TypeScript compiler: `npm run typecheck`

### Documentation Style

- Use **Markdown** for all documentation
- Use **clear headings** and structure
- Include **code examples** where appropriate
- Add **screenshots** for UI changes
- Keep language **simple and accessible**

---

## 📝 Commit Messages

We follow the **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

**Simple commit:**
```
feat(agent): add PII detection for credit cards
```

**Detailed commit:**
```
fix(api): resolve CORS issue with frontend requests

The CORS middleware was not properly configured to allow
credentials. This commit updates the middleware configuration
to allow credentials and specifies exact origins instead of
using wildcards.

Fixes #123
```

**Breaking change:**
```
feat(api)!: change response format for chat endpoint

BREAKING CHANGE: The chat endpoint now returns source_documents
as an array of objects instead of strings. Update frontend to
handle new format.
```

### Best Practices

- Use **present tense** ("add feature" not "added feature")
- Use **imperative mood** ("move cursor to..." not "moves cursor to...")
- Keep **subject line under 50 characters**
- Capitalize **first letter** of subject
- **No period** at end of subject
- Separate subject from body with **blank line**
- Wrap body at **72 characters**
- Use body to explain **what and why**, not how
- Reference **issues and PRs** in footer

---

## 🔀 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No console errors or warnings
- [ ] Commits follow commit message guidelines

### PR Template

When creating a PR, use this template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Fixes #(issue number)

## How Has This Been Tested?
Describe the tests you ran

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, PR will be merged
5. **Merge**: Squash and merge or rebase and merge

### After Merge

- Delete your branch
- Pull latest changes from upstream
- Celebrate! 🎉

---

## 🌍 Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions

### Getting Help

If you need help:

1. Check existing **documentation**
2. Search **closed issues**
3. Ask in **GitHub Discussions**
4. Create a **new issue** with details

### Recognition

Contributors will be:
- Listed in **CONTRIBUTORS.md**
- Mentioned in **release notes**
- Credited in **documentation**

---

## 📚 Additional Resources

### Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Project Resources

- [README.md](README.md) - Project overview
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community guidelines
- [LICENSE](LICENSE) - Project license

---

## 🙏 Thank You!

Thank you for contributing to CyberSaathi! Your efforts help make legal information more accessible to everyone.

**Questions?** Don't hesitate to ask! We're here to help.

---

<div align="center">

**Happy Contributing! 🚀**

Made with ❤️ by the CyberSaathi community

</div>
