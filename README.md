# Workspace - AI Developer Workspace

## Project Structure

```
current directory
├── src/                    # Core source code
│   └── ai/
│       ├── core.py         # Main AI logic
│       ├── planning.py     # Planning and reasoning
│       └── execution.py    # Action execution
├── tests/                  # Comprehensive test suite
│   └── ai/
│       └── core.py         # Core functionality tests
├── docs/                   # Documentation
│   └── guidelines.md       # User guidelines
└── .github/                # GitHub configurations
```

## Development Guidelines

### Commit Message Standards

```
type: <short description>

<ll:long-description>
    <more details about the commit>
    <50-character line limit>
<ll>
```

### Branching Strategy

```
main           ───●─────●───●───●───●───●───●
              │
release/1.0  ─●────●──●
              │
feature/*    ●──●──●
              │
              ●──●──●──●──● (main)
                    │
draft/*      ●──●──●
```

### Code Quality Standards

| Metric | Standard | Tool |
|--------|----------|------|
| Linting | No errors | pylint, flake8 |
| Type Checking | 100% coverage | mypy |
| Test Coverage | >80% min | coverage.py |
| Security | No vulnerabilities | bandit |
| Formatting | Consistent | black, isort |

### Contribution Process
1. Create a feature branch from main
2. Make changes with clear commit messages
3. Write or update tests
4. Run `pre-commit run --all-files`
5. Push changes to GitHub
6. Create a pull request for review