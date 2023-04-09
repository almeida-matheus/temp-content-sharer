import random
import string

get_random_id = lambda c : ''.join(random.choice(string.digits+string.ascii_lowercase) for _ in range(c))