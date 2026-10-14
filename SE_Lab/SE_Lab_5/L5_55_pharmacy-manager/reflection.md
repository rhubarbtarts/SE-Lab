# Reflection on Static Code Analysis

## 1. What did you learn from using static analysis tools?

I learned that static analysis tools can identify potential security vulnerabilities, programming errors, and code-style problems without executing the program. Pylint helped evaluate code quality and maintainability, Bandit identified security risks, and Flake8 checked coding-style violations.

## 2. Which issues were the most important to fix, and why?

The most important issues were the use of `eval()`, unsafe pickle deserialization, shell command execution, and the hardcoded password. These could create security vulnerabilities. Input validation and stock-handling improvements were also important because incorrect quantities or invalid medicine data could affect pharmacy operations.

## 3. How did the fixes improve the program?

The fixes made the program safer and more reliable. Arithmetic expressions are now evaluated using an AST-based evaluator instead of unrestricted `eval()`. Stock is stored as JSON with validation, shell execution was removed, and the pharmacist password is read from an environment variable. Additional checks prevent invalid stock quantities and dispensing more medicine than is available.

## 4. What challenges did you face, and how did you overcome them?

One challenge was resolving the findings while keeping the program functional. I addressed the issues incrementally and tested the program after updating it. I also reran the static-analysis tools to verify the changes. The final Pylint score improved from 4.83/10 to 10.00/10, Bandit reported no issues, and Flake8 produced no violations.

## Conclusion

This lab helped me understand the value of static code analysis in improving security, reliability, readability, and maintainability. I learned that tool results should be followed by code changes and testing rather than simply suppressing warnings.