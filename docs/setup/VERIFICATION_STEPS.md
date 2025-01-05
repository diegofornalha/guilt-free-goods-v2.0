# Code Verification Guide

## Overview
This guide outlines the essential steps for verifying code changes in the Guilt Free Goods v2.0 project. The primary verification method is through CI/CD pipelines, with optional local verification when environment setup permits.

## Essential Verification Steps

### 1. Dependency Installation
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install
```

Verify successful installation by checking for error messages.

### 2. Lint Checks
```bash
# JavaScript/TypeScript linting
npm run lint
npm run lint -- --fix  # Auto-fix issues where possible
```

### 3. Optional Local Testing
If environment variables are properly configured:
```bash
# Backend tests (requires configured test environment)
pytest backend/tests -v

# Frontend tests
npm test
```

Note: Local testing is optional and depends on proper environment setup. Prefer CI verification over local testing unless specifically configured for local development.

## CI/CD Verification

### GitHub Actions
The primary method for code verification is through GitHub Actions:
1. Automated tests run on pull requests
2. Required checks must pass before merging
3. CI provides comprehensive test coverage

### Required Checks
1. Lint validation
2. Unit tests
3. Integration tests
4. Type checking
5. Build verification

## Manual Review Process

### Before Submitting PR
1. Check for lint errors:
   ```bash
   npm run lint
   ```
2. Review changed files:
   ```bash
   git diff --staged
   ```
3. Verify documentation updates if applicable

### After CI Runs
1. Monitor GitHub Actions progress
2. Address any CI failures
3. Request code review if all checks pass

## Common Issues

### Lint Errors
- Run auto-fix: `npm run lint -- --fix`
- Manual fixes may be required
- Consult ESLint/Prettier documentation

### Dependency Issues
- Verify `package.json` changes
- Check for conflicting versions
- Update lock files if necessary

### Environment Setup
- Refer to ENVIRONMENT.md for setup
- Verify required credentials
- Check environment variables

## Best Practices

### Code Review
1. Wait for CI checks to complete
2. Address all automated feedback
3. Request human review
4. Document manual testing if performed

### Documentation
1. Update relevant docs
2. Include setup changes
3. Document new dependencies
4. Note environment requirements

### Security
1. Never commit credentials
2. Review security implications
3. Follow security guidelines

## Verification Checklist

### Required
- [ ] Dependencies install without errors
- [ ] Lint checks pass
- [ ] CI pipeline succeeds
- [ ] Documentation updated
- [ ] Security considerations addressed

### Optional (Environment Dependent)
- [ ] Local tests pass
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Next Steps

### After Verification
1. Wait for CI completion
2. Address any failures
3. Request code review
4. Monitor deployment

### If Issues Occur
1. Check CI logs
2. Review error messages
3. Consult documentation
4. Request assistance if needed

Remember:
1. CI is the primary verification method
2. Local testing is optional
3. Always wait for CI before merging
4. Document any environment-specific requirements

For detailed environment setup and testing information, refer to:
- ENVIRONMENT.md
- TESTING_GUIDE.md
- SETUP_GUIDE.md
