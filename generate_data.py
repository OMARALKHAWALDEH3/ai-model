import random
import pandas as pd

base_sql = [
    "SELECT * FROM users WHERE id=1",
    "' OR 1=1--",
    "UNION SELECT username,password FROM users",
    "admin' --",
    "1' OR '1'='1",
    "SELECT * FROM users WHERE username='admin' OR '1'='1'",
    "1'; DROP TABLE users--",
    "1' AND SLEEP(5)--"
]

base_xss = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "javascript:alert(1)",
    "<iframe src=javascript:alert(1)>",
    "<body onload=alert(1)>",
    "<script>alert(document.cookie)</script>"
]

base_cmd = [
    "; ls",
    "&& whoami",
    "| cat /etc/passwd",
    "`id`",
    "$(whoami)",
    "; ping -c 4 127.0.0.1",
    "&& rm -rf /"
]

base_trav = [
    "../etc/passwd",
    "../../etc/passwd",
    "..\\..\\windows\\system32",
    "../../../../etc/shadow",
    "../windows/system32/drivers/etc/hosts",
    "..%2f..%2fetc%2fpasswd"
]

base_normal = [
    "login user",
    "search product",
    "view dashboard",
    "get user data",
    "home page",
    "user profile",
    "update settings",
    "checkout cart"
]

base_normal_real = [
    "login user password",
    "username=omar password=123456",
    "POST /login username=admin password=1234",
    "GET /api/user?id=5",
    "update profile name=omar",
    "search product iphone",
    "add to cart item=123",
    "email=test@example.com",
    "reset password request"
]

data = []

for _ in range(2000):
    data.append(["sql", random.choice(base_sql) + str(random.randint(1,100))])
    data.append(["xss", random.choice(base_xss)])
    data.append(["cmdinj", random.choice(base_cmd)])
    data.append(["traversal", random.choice(base_trav)])

    for _ in range(8):
        data.append(["normal", random.choice(base_normal)])
        data.append(["normal", random.choice(base_normal_real)])
        data.append(["normal", f"login username=user{random.randint(1,100)} password=pass{random.randint(1,1000)}"])
        data.append(["normal", "login user password"])
        data.append(["normal", "username=admin password=1234"])
        data.append(["normal", f"GET /api/products?id={random.randint(1,100)}"])
        data.append(["normal", f"user_id={random.randint(1,50)} action=view"])
        data.append(["normal", f"user request id={random.randint(1,5000)}"])
        data.append(["normal", f"search query item {random.randint(1,200)}"])

    data.append(["normal", f"hello {random.choice(base_xss)} world"])
    data.append(["normal", f"user={random.randint(1,10)} action=view"])

random.shuffle(data)

df = pd.DataFrame(data, columns=["Type", "Payload"])
df.to_csv("big_data_generated.csv", index=False)

print("FINAL DATASET GENERATED!")
print("Total Rows:", len(df))