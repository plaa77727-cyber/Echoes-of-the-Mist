import random

secret_number = random.randint(1, 9)
max_attempts = 3 # จำกัดแค่ 10 ครั้ง
attempts = 0       # ตัวนับจำนวนครั้ง

print("เกมทายเลข 1-100! คุณมีโอกาสทายแค่ 10 ครั้ง")

while attempts < max_attempts:
    try:
        guess = int(input(f"ครั้งที่ {attempts+1}: ทายเลข = "))
        attempts += 1

        if guess == secret_number:
            print(f"ถูกต้อง! คุณทายถูกในครั้งที่ {attempts}")
            break
        elif guess < secret_number:
            print("ต่ำไป!")
        else:
            print("สูงไป!")

    except :
        print("กรอกตัวเลขเท่านั้น!")

else:
    print(f"หมดสิทธิ์ทายแล้ว! เลขที่ถูกต้องคือ {secret_number}")
