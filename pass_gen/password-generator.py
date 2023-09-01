import random
import string

total = string.ascii_letters + string.digits + string.punctuation
print(total)
length = 16
password = "".join(random.sample(total, length))
print(password)