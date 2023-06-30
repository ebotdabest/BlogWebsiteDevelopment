import hashlib

def encrypt(data):
    data = str(data)  # Convert to string to ensure that it can be encoded
    data = data.encode('utf-8')  # Encode the string to bytes
    hashed_data = hashlib.sha256(data)  # Hash the data using SHA-256
    return hashed_data.hexdigest()  #