from flask import Flask
from flask_socketio import SocketIO, emit, send
app = Flask(__name__)

socketio = SocketIO(app)

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

KEY = hashlib.sha256("".encode('utf-8')).digest() 

class AESCipher(object):

	def __init__(self): 
		self.bs = AES.block_size
		self.MODE = AES.MODE_CBC 

	def encrypt(self, raw):
		raw = self._pad(raw)
		iv = Random.new().read(self.bs)
		cipher = AES.new(KEY, self.MODE, iv)
		return base64.b64encode(iv + cipher.encrypt(raw))

	def decrypt(self, enc, key):
		enc = base64.b64decode(enc)
		iv = enc[:self.bs]
		cipher = AES.new(key, self.MODE, iv)
		return self._unpad(cipher.decrypt(enc[self.bs:])).decode('utf-8')

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]


@app.route("/")
def hello():
    return open('html/index.html').read()

@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)

if __name__ == "__main__":
    ##app.run()
    socketio.run(app)
