import secrets
import hashlib
import base64

# Generate a random string of 128 characters
code_verifier = secrets.token_urlsafe(128)
print("Code Verifier:", code_verifier)

# Calculate the SHA-256 hash of the code verifier
code_verifier_hash = hashlib.sha256(code_verifier.encode()).digest()

# Base64url encode the SHA-256 hash and remove padding characters
code_challenge = base64.urlsafe_b64encode(code_verifier_hash).rstrip(b'=').decode()
print("Code Challenge:", code_challenge)

https://www.fitbit.com/oauth2/authorize?client_id=23RR77&response_type=code
  &code_challenge=EFiGt6s3s2E-uU7Mm9gDvuuhO6IkgDaoHAF0icsy1WY
  &code_challenge_method=S256
  &scope=activity%20heartrate%20location%20nutrition%20oxygen_saturation%20profile%20respiratory_rate%20settings%20sleep%20social%20temperature%20weight
