# MIT License

# Copyright (c) 2022 Gramscript Telegram API

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class DataCenter:
    TEST = {
        1: "149.154.175.10",
        2: "149.154.167.40",
        3: "149.154.175.117",
        121: "95.213.217.195"
    }

    PROD = {
        1: "149.154.175.53",
        2: "149.154.167.51",
        3: "149.154.175.100",
        4: "149.154.167.91",
        5: "91.108.56.130",
        121: "95.213.217.195"
    }

    TEST_IPV6 = {
        1: "2001:b28:f23d:f001::e",
        2: "2001:67c:4e8:f002::e",
        3: "2001:b28:f23d:f003::e",
        121: "2a03:b0c0:3:d0::114:d001"
    }

    PROD_IPV6 = {
        1: "2001:b28:f23d:f001::a",
        2: "2001:67c:4e8:f002::a",
        3: "2001:b28:f23d:f003::a",
        4: "2001:67c:4e8:f004::a",
        5: "2001:b28:f23f:f005::a",
        121: "2a03:b0c0:3:d0::114:d001"
    }

    def __new__(cls, dc_id: int, test_mode: bool, ipv6: bool):
        if ipv6:
            return (
                (cls.TEST_IPV6[dc_id], 80)
                if test_mode
                else (cls.PROD_IPV6[dc_id], 443)
            )
        else:
            return (
                (cls.TEST[dc_id], 80)
                if test_mode
                else (cls.PROD[dc_id], 443)
            )
