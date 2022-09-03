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

from .accept_terms_of_service import AcceptTermsOfService
from .check_password import CheckPassword
from .connect import Connect
from .disconnect import Disconnect
from .get_password_hint import GetPasswordHint
from .initialize import Initialize
from .log_out import LogOut
from .recover_password import RecoverPassword
from .resend_code import ResendCode
from .send_code import SendCode
from .send_recovery_code import SendRecoveryCode
from .sign_in import SignIn
from .sign_in_bot import SignInBot
from .sign_up import SignUp
from .terminate import Terminate


class Auth(
    AcceptTermsOfService,
    CheckPassword,
    Connect,
    Disconnect,
    GetPasswordHint,
    Initialize,
    LogOut,
    RecoverPassword,
    ResendCode,
    SendCode,
    SendRecoveryCode,
    SignIn,
    SignInBot,
    SignUp,
    Terminate
):
    pass
