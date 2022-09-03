

try:
    from pyaes import AESModeOfOperationCTR
except ImportError:
    pass


class CTR:
    def __init__(self, key: bytes, iv: bytes):
        self.ctr = AESModeOfOperationCTR(key)
        self.iv = iv

    def decrypt(self, data: bytes, offset: int) -> bytes:
        replace = int.to_bytes(offset // 16, byteorder="big", length=4)
        iv = self.iv[:-4] + replace
        self.ctr._counter._counter = list(iv)

        return self.ctr.decrypt(data)
