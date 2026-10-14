# Static Code Analysis — Issues and Fixes

The original `pharmacy_manager.py` was analyzed using Pylint, Bandit, and Flake8. The table below records representative findings from the baseline reports and the corresponding fixes made in the cleaned version. Line numbers refer to the original source file.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Weak MD5 hash | High — Security (Bandit B324) | 51 | MD5 is considered weak for security-sensitive hashing. | Replaced MD5 with SHA-256. This change alone does not guarantee patient-data privacy. |
| Shell command execution | High — Security (Bandit B605) | 68 | `os.system()` builds a shell command using the medicine name, creating command-injection risk. | Removed shell execution and printed the label directly. |
| Unrestricted `eval()` | Medium — Security (Bandit B307) | 48 | Evaluates a string as Python code, potentially allowing arbitrary code execution. | Replaced it with an AST-based evaluator that permits basic arithmetic only. |
| Unsafe pickle loading | Medium — Security (Bandit B301) | 64 | Deserializing untrusted pickle data can execute arbitrary code. | Replaced pickle storage with JSON and validated loaded stock records. |
| Mutable default argument | Code quality (Pylint W0102) | 13 | The default audit list may be shared between function calls. | Changed the default to `None` and create a list when no audit list is supplied. |
| Bare exception handler | Reliability (Pylint W0702; Bandit B110) | 27–28 | Silently ignores errors and makes failures difficult to diagnose. | Removed the broad exception-swallowing behavior and added explicit validation. |
| Hardcoded password | Security (Bandit B105) | 11 | The password is embedded in the source code. | Read the configured password from the `PHARMACIST_PASSWORD` environment variable and used `secrets.compare_digest()`. |
| Predictable prescription number | Security (Bandit B311) | 54 | The standard `random` module is not intended for security-sensitive unpredictability. | Used `secrets.randbelow()` to generate prescription references. |
| Missing docstrings | Code quality (Pylint C0114/C0116) | 1, 13–89 | The module and functions lack documentation. | Added a module docstring and function docstrings. |
| Inconsistent function naming | Style (Pylint C0103) | 13, 22, 30, 33, 40, 46, 50, 53, 56, 61, 67, 70, 78, 84 | CamelCase names do not follow the recommended snake_case convention. | Renamed functions using snake_case. |
| Unused imports | Code quality (Pylint W0611) | 2, 6 | `sys` and `logging` are imported but unused. | Removed unused imports. |
| File handling without context managers | Code quality (Pylint R1732) | 57, 62 | Files are manually opened and closed, which is less robust if an error occurs. | Used `with` statements for file operations. |
| Insufficient stock and input validation | Functional reliability | Review original stock and dispensing functions | Negative stock or dispensing unavailable quantities can produce invalid inventory state. | Added validation for medicine names, quantities, prices, and available stock. |

## Before-and-After Results

| Tool | Baseline result | Final result |
|---|---|---|
| Pylint | 4.83/10 | 10.00/10 |
| Bandit | 8 findings: 2 High, 2 Medium, 4 Low | No issues identified |
| Flake8 | Style violations reported | No violations reported |

## Conclusion

The cleaned version addresses multiple security, reliability, and maintainability problems. The final scans reported a Pylint score of 10.00/10, no Bandit findings, and no Flake8 violations.