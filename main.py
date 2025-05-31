import hashlib
import requests
import argparse

# Encode Your Password With utf-8 and sha1
def get_sha_1_hash(password):
  return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

def get_pwned_data(prefix):
  url = f"https://api.pwnedpasswords.com/range/{prefix}"
  response = requests.get(url)
  
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
        return f"Your Password Has Been Leaked {counts} time"
        
      else :
        return f"Your Password Has Been Leaked {counts} times"
  
  return f"Your Password Has Never Been Leaked"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if your password has been leaked using the HIBP API.")
    
    parser.add_argument("--password","-p",help= "The password you want to check.")
    

    args = parser.parse_args() 

    if args.password:
      pwd = args.password
    
    else:
      pwd = input("Enter your password to check: ")

    print(check_pwned_data(pwd))
