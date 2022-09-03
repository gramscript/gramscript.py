

from pyaes import AES

BLOCK_SIZE = 16


# TODO: Performance optimization

class IGE:
    @classmethod
    def encrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        return cls.ige(data, key, iv, True)

    @classmethod
    def decrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        return cls.ige(data, key, iv, False)

    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )

    @classmethod
    def ige(cls, data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
        cipher = AES(key)

        iv_1 = iv[:BLOCK_SIZE]
        iv_2 = iv[BLOCK_SIZE:]

        data = [data[i: i + BLOCK_SIZE]
                for i in range(0, len(data), BLOCK_SIZE)]

        if encrypt:
            for i, chunk in enumerate(data):
                iv_1 = data[i] = cls.xor(
                    cipher.encrypt(cls.xor(chunk, iv_1)), iv_2)
                iv_2 = chunk
        else:
            for i, chunk in enumerate(data):
                iv_2 = data[i] = cls.xor(
                    cipher.decrypt(cls.xor(chunk, iv_2)), iv_1)
                iv_1 = chunk

        return b"".join(data)
