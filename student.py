import bcrypt
plain = 'secret'
hash1 = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())
hash2 = bcrypt.hashpw(plain.encode('utf-8'), hash1)
print(hash1==hash2)
print(hash1.decode('utf-8') == hash2.decode('utf-8'))