import hashlib
import requests
import argparse
import os

# Encode Your Password With utf-8 and sha1
def get_sha_1_hash(password):
  return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

def get_pwned_data(prefix):
  url = f"https://api.pwnedpasswords.com/range/{prefix}"
  try:
    response = requests.get(url,timeout= 5)
  except requests.exceptions.RequestException:
      raise RuntimeError("Network error: Unable to connect to the HIBP API. Please check your internet connection or try again later.")  
  
  if response.status_code != 200:
    raise RuntimeError(f"Error fetching data: {response.status_code}")

  return response.text

# Check Your Password Has Been Leaked ?
def check_pwned_data(password):
  sha1 = get_sha_1_hash(password)
  prefix , suffix = sha1[:5] , sha1[5:]
  
  response_suffix = get_pwned_data(prefix)
  
  for line in response_suffix.splitlines():
    api_suffix , counts = line.split(":")

    if api_suffix == suffix:  
      counts = int(counts)
      if counts == 1 :
        return f"Your Password ({password}) Has Been Leaked {counts} time"
        
      else :
        return f"Your Password ({password}) Has Been Leaked {counts} times"
  
  return f"Your Password ({password}) Has Never Been Leaked"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if your password has been leaked using the HIBP API.")
    
    parser.add_argument("--password","-p",help= "The password you want to check")
    parser.add_argument("--file","-f",help= "Path to a file containing passwords")
    parser.add_argument("--output", "-o",nargs='?',const="result.txt",help="Output file to save results (default: result.txt if --output is given without value)")

    args = parser.parse_args() 
    
    result = []
  
    if args.file:
      if not os.path.isfile(args.file):
        print(f"File not found. {args.file}")
      else:
        with open(args.file,"r", encoding='utf8') as file:
          for line in file:
            line = line.strip()
            res = check_pwned_data(line)
            result.append(res)
            print(res)
    
    else:
      if args.password:
        pwd = args.password
        res = check_pwned_data(pwd)
        result.append(res)
        print(res)
      else:
        pwd = input("Enter your password to check: ")
        res = check_pwned_data(pwd)
        result.append(res)
        print(res)
    

    if args.output:
      try:
        with open(args.output, "w", encoding='utf8') as output_file:
          output_file.write("\n".join(result))
        print(f"Results saved to {args.output}")
      except IOError as e:
        print(f"Error writing to file {args.output}: {e}")
          













