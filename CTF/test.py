from Crypto.Util.number import bytes_to_long
from binascii import unhexlify
def splitmix64(x: int) -> int:
    U64_MASK = 0xFFFFFFFFFFFFFFFF
    x = (x + 0x9E3779B97F4A7C15) & U64_MASK
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & U64_MASK
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & U64_MASK
    return x ^ (x >> 31)


class Hash:

    def __init__(self):
        self.secret = 1


    def pad(self, message: bytes) -> bytes:
        c = -len(message) % 8
        return message + b'\x00' * c


    def digest(self, message: bytes, state) -> bytes:
        print("before", len(message))
        message = self.pad(message)
        print("after", len(message))
        blocks = [int.from_bytes(message[i:i+8], 'big')
                  for i in range(0, len(message), 8)]

        def f(a: int, b: int) -> int:
            for i in range(16):
                a, b = b, a ^ splitmix64(b)
            return b

        for block in blocks:
            state = f(state, block)

        return state.to_bytes(8, 'big')


    def hexdigest(self, message: bytes, init) -> str:
        return self.digest(message, init).hex()
hhh = Hash()
h = b"9828e58adc1a0027"
message = ",1"
h = unhexlify(h)
h = bytes_to_long(h)
print(hhh.hexdigest(message.encode(), h))

a = "29,6,9,7,28,5,12,1:72564df8eb002bb7
"
