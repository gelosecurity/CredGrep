import os
import re
import sys
import argparse
import jsbeautifier

print('\033[1;34m _____           _______           \033[0m')
print('\033[1;34m/ ___/______ ___/ / ___/______ ___ \033[0m')
print('\033[1;34m/ /__/ __/ -_) _  / (_ / __/ -_) _ \\\033[0m')
print('\033[1;34m\\___/_/  \\__/\\_,_/\\___/_/  \\__/ .__/\033[0m')
print('\033[1;34m                             /_/    \033[0m')

search = ["admin", "api_key", "api-key", "api_secret", "api-secret", "access_token", "access-token", "username", "password", "secret_key", "auth_token", "private_key", "public_key", "master_key", "encryption_key", "decryption_key", "client_id", "client-id", "client_secret", "client-secret", "aws_access_key", "aws-access-key", "aws_secret_key", "aws-secret-key", "s3_key", "s3-key", "s3_secret", "s3-secret", "app_id", "app-id", "app_secret", "app-secret", "AKIA", "appKey", "appSecret"]
file_types = [".smali", ".xml", ".json", ".conf", ".gradle", ".properties"]
print('\n\033[1;33m' + 'Searching for ' + str(search) + ' in file types: ' + str(file_types) + '\033[0m\n')

def scan_for_secrets(path, verbose):
   secrets = []
   file_count = 0
   for root, dirs, files in os.walk(path):
       for file in files:
           if not any(file.endswith(ext) for ext in file_types):
               continue
           file_count += 1
           try:
               with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                   contents = f.read()
                   if file.endswith(".js"):
                       beautified_contents = jsbeautifier.beautify(contents)
                       contents_lines = beautified_contents.split("\n")
                   else:
                       contents_lines = contents.split("\n")
                   for line_number, line in enumerate(contents_lines):
                       matches = re.findall(f"({'|'.join(search)})\\s*:?\\s*['\"][^'\"]+['\"]", line, re.IGNORECASE)
                       cred_pairs = re.findall(r"{\"username\":\"[^\"]+\",\"password\":\"[^\"]+\"}", line)
                       if matches or cred_pairs:
                           print(f"[\033[1;33mSECRETS\033[0m] \033[32m{os.path.join(root, file)}:{line_number + 1}\033[0m")
                           for match in matches:
                               line = re.sub(f"{match}", f"\033[1;31m{match}\033[0m", line)
                           print(f"- {line.strip()}")
                       secrets += matches + cred_pairs
           except UnicodeDecodeError:
               if verbose:
                   print(f"[ERROR] {os.path.join(root, file)} could not be decoded with UTF-8 encoding. Skipping...")
   if file_count == 0:
       sys.exit("[ERROR] No files are found. Are you in the correct directory with the app contents?")
   return secrets

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Search for hardcoded secrets in an app.")
   parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output.")
   parser.add_argument("path", metavar="PATH", type=str, help="The path to the directory containing the app files.")
   args = parser.parse_args()
   app_path = args.path
   secrets = scan_for_secrets(app_path, args.verbose)
   if secrets:
       print("[\033[1;34mINFO\033[0m] \033[1mScan complete.\033[0m")
   else:
       print("[\033[1;34mINFO\033[0m] \033[1mNo hardcoded secrets found.\033[0m")
