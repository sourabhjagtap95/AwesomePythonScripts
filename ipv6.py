import sys

result = []

def is_leading_zero(token):
    return len(token) > 1 and token[0] == "0"
    
def is_valid_hex_digit(token):
    for c in token:
        if c not in "0123456789abcdef":
            return False
            
    return True

def is_valid_length_token(token):
    return len(token) > 0 and len(token) < 5

def is_enough_group(ip):
    return len(ip.split(":") == 8
    
while True:
    line = sys.stdin.readline()
    if not line:
        print "\n".join(result) if len(result) else "EMPTY"
        break
    else:
        if is_enough_group(ip):
            tokens = ip.split(":")
            for token in tokens:
                bad = False
                if is_valid_length_token(token) and not is_leading_zero(token) and is_valid_hex_digit(token):
                    bad = False
                else:
                    bad = True
                    break
                
                if not bad:
                    result.append(ip)
                    
    
                
            
            
            
            
            