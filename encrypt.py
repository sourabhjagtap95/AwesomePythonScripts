'''
open cmd and type
pip install cryptography
'''




from cryptography.fernet import Fernet
gen_key=Fernet.generate_key()
fer=Fernet(gen_key)
msg="data"              #any data
encrypted=fer.encrypt(msg.encode())
print(encrypted)
