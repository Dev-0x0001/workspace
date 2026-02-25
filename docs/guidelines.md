## Development Guidelines

### Commit Message Standards

Commit messages should follow these conventions:

```
type: <short description>

<ll:long-description>
    <more details about the commit>
    <50-character line limit>
<ll>
```

### Branching Strategy

We use a Git Flow variant:
- `main` - production-ready code
- `release/*` - release preparation
- `feature/*` - new features
- `draft/*` - exploratory work

### Code Quality

```
| Metric | Standard | Tool |
|--------|----------|------|
| Linting | No errors | pylint, flake8 |
| Type Checking | 100% coverage | mypy |
| Test Coverage | >80% min | coverage.py |
| Security | No vulnerabilities | bandit |
| Formatting | Consistent | black, isort |
```

### Contribution Process
1. Create a branch from `main`
2. Make changes with clear commit messages
3. Write or update tests
4. Run `pre-commit run --all-files`
5. Push changes
6. Create a pull request