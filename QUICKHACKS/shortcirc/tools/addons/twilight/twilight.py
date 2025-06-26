import tools.addons.twilight.xor as Xor
import tools.addons.twilight.salt as Salt
import tools.addons.twilight.hash as Hash
def Encrypt(text, key):
    salt = Hash.getSaltByKey(key, text)
    saltedText = Salt.protect(text, salt)
    xoredText  = Xor.encode(saltedText, key)
    return xoredText
def Decrypt(text, key):
    unxoredText = Xor.decode(text, key)
    salt = Hash.getSaltByKey(key, unxoredText)
    unsaltData  = Salt.unprotect(unxoredText, salt)
    return unsaltData