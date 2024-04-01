# Senior-SWE_AI

SeniorSWE-AI is a command-line interface for in-context embedding that leverages the semantic comprehension capabilities of large language models to analyze the intended codebase and engage in a conversation with it, mimicking the behavior of a seasoned software engineer.

[![Python CI/CD Pipeline](https://github.com/Younis-Ahmed/senior-swe_ai/actions/workflows/pipeline.yml/badge.svg)](https://github.com/Younis-Ahmed/senior-swe_ai/actions/workflows/pipeline.yml)
## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python >=3.9.1 < 3.12
- Pip package manager
- `git` is used as a version control for intended codebase

## Installation
1. Install Package:
    ```shell
    pipx install senior-swe-ai
    ```
    OR
    ```shell
    pip install senior-swe-ai
    ```

2. Initialize the app and choose options:
    ```shell
    sen-ai init
    ```

3. `cd` into desired codebase [`git` as VC is required]
    ```shell
    cd path/to/codebase
    ```

4. Run the application:
    ```shell
    sen-ai chat
    ```

## Re-configuration

- Run `sen-ai init` again to reset options

## Programming Languages support
```
C/C++
C#
GO
JAVA
JAVASCRIPT
KOTLIN
PYTHON
RUBY
RUST
TYPESCRIPT
```

## Credits
This project was developed by [Younis](https://github.com/Younis-ahmed).

## Disclaimer
This project is for educational purposes only and should not be used in production environments without proper testing and validation.
