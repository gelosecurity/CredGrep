# CredGrep
CredGrep is a Python script designed to search for hardcoded secrets in an app. This can be useful for detecting and removing sensitive information that may have been accidentally left in application directories.

## Usage
To use CredGrep.py, simply run the script and provide the path to the app that you want to scan. For example:
```
python CredGrep.py /path/to/app
```
By default, CredGrep.py will search for a predefined list of secret strings, including things like API keys, usernames, and passwords. You can customize this list by editing the search variable at the top of the script.

If you want to see more verbose output, you can use the -v or --verbose option:

```
python CredGrep.py -v /path/to/app
```

## Output
When CredGrep.py finds a file that contains a hardcoded secret, it will print out information about the file and the line number where the secret was found. It will also highlight the secret in the output using ANSI color codes.

```
[SECRETS] /path/to/file.js:12
- var secretKey = "abcdefg";
```

Dependencies
You can install the jsbeautifier library using pip:

`pip install jsbeautifier`
