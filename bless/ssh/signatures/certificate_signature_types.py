from cryptography.hazmat.primitives import hashes

class SSHSignatureType(object):
    """
    Signature tpyes used during generation of certificate signature
    """
    RSA = 'ssh-rsa'
    RSA_SHA2_256 = 'rsa-sha2-256'
    RSA_SHA2_512 = 'rsa-sha2-512'

def signature_hasher(signature_type):
    if signature_type == SSHSignatureType.RSA:
        return hashes.SHA1()
    elif signature_type == SSHSignatureType.RSA_SHA2_256:
        return hashes.SHA256()
    elif signature_type == SSHSignatureType.RSA_SHA2_512:
        return hashes.SHA512()