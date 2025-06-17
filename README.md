# Password Leak Checker

A command-line tool to check if your passwords have been exposed in data breaches using the Have I Been Pwned API.

## Features

- Check single passwords
- Process multiple passwords from a file
- Save results to output file
- Secure password handling with k-anonymity

## Usage

### Basic Password Check
```bash
python main.py -p mypassword
```

### Check Password and Save Result
```bash
# Save to default result.txt
python main.py -p mypassword --output

# Save to custom file
python main.py -p mypassword -o custom.txt
```

### Check Multiple Passwords from File
```bash
# Check passwords and display results
python main.py -f passwords.txt

# Check and save results
python main.py -f passwords.txt --output results.txt
```

## Output Options

The `--output` / `-o` argument supports two formats:

1. With filename:
   ```bash
   python main.py -p mypassword -o custom.txt
   ```

2. Without filename (uses default "result.txt"):
   ```bash
   python main.py -p mypassword --output
   ```

## Output Format

The output file contains one result per line:
```
Your Password (****) Has Been Leaked 5 times
Your Password (****) Has Never Been Leaked
```

## Requirements

- Python 3.6+
- requests