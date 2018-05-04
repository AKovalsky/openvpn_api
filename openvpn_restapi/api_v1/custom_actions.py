#!/usr/bin/env python3


import os
import errno
import socket
from django.utils.crypto import get_random_string
from OpenSSL import crypto, SSL
from django.conf import settings
from .custom_exceptions import CreateSSLCertificateException, ReadSSLCertificateException

def CreateSSLCertificate(name):
    clientkeyname = name + '.key'
    clientcertname = name + '.crt'
    clientcsrname = name + '.csr'
    serial = int.from_bytes(os.urandom(16), byteorder='big')
    ca_key_path = '/usr/local/src/easy-rsa-old/easy-rsa/2.0/keys/ca.key'
    ca_cert_path = '/usr/local/src/easy-rsa-old/easy-rsa/2.0/keys/ca.crt'
    user_certificates_path = '/usr/local/client_certificates/'
    try:
        create_certificate(ca_cert_path, ca_key_path, name, clientcsrname, clientcertname, clientkeyname, serial, user_certificates_path)
    except:
        raise CreateSSLCertificateException
    return clientcertname, clientkeyname, clientcsrname, serial



def RevokeSSLCertificate(basename, certificate_name):
    ca_key_path = '/usr/local/src/easy-rsa-old/easy-rsa/2.0/keys/ca.key'
    ca_cert_path = '/usr/local/src/easy-rsa-old/easy-rsa/2.0/keys/ca.crt'
    certificate_path = '/usr/local/client_certificates/' + basename + '/' + certificate_name
    clr_path = '/usr/local/src/easy-rsa-old/easy-rsa/2.0/keys/clr.pem'
    revoke_certificate(ca_cert_path, ca_key_path, clr_path, certificate_path)
    print(name)

def CreateConfigFile(commons, basename, ca, certificate, key):
    common = read_from_disk('/root', 'commons.txt')
    cacertdump = read_from_disk('/usr/local/src/easy-rsa-old/easy-rsa/2.0/keys','ca.crt')
    clientcert = read_from_disk('/usr/local/client_certificates/' + basename, certificate)
    clientkey = read_from_disk('/usr/local/client_certificates/' + basename, key)
    ovpn = "%s<ca>\n%s</ca>\n<cert>\n%s</cert>\n<key>\n%s</key>\n" % (common, cacertdump, clientcert, clientkey)
    write_to_disk('/usr/local/client_certificates/' + basename, basename + '.ovpn', ovpn)
    return basename + '.ovpn'

def read_from_disk(directory, filename):
    file_path = directory + '/' + filename
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
    except IOError:
        raise ReadSSLCertificateException 
    return content


def write_to_disk(directory, filename, content):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise CreateSSLCertificateException
    try:
        # Write our file.
        with open(directory+'/'+filename, 'w') as f:
            f.write(content)
            f.close()
    except:
        raise CreateSSLCertificateException



# Create a new keypair of specified algorithm and number of bits.
def make_keypair(algorithm=crypto.TYPE_RSA, numbits=2048):
    pkey = crypto.PKey()
    pkey.generate_key(algorithm, numbits)
    return pkey

# Creates a certificate signing request (CSR) given the specified subject attributes.
def make_csr(pkey, CN, C=None, ST=None, L=None, O=None, OU=None, emailAddress=None, hashalgorithm='sha256WithRSAEncryption'):
    req = crypto.X509Req()
    req.get_subject()
    subj  = req.get_subject()

    if C:
        subj.C = C
    if ST:
        subj.ST = ST
    if L:
        subj.L = L
    if O:
        subj.O = O
    if OU:
        subj.OU = OU
    if CN:
        subj.CN = CN
    if emailAddress:
        subj.emailAddress = emailAddress

    req.set_pubkey(pkey)
    req.sign(pkey, hashalgorithm)
    return req

# Create a certificate authority (if we need one)
def create_ca(CN, C="", ST="", L="", O="", OU="", emailAddress="", hashalgorithm='sha256WithRSAEncryption'):
    cakey = make_keypair()
    careq = make_csr(cakey, cn=CN)
    cacert = crypto.X509()
    cacert.set_serial_number(0)
    cacert.gmtime_adj_notBefore(0)
    cacert.gmtime_adj_notAfter(60*60*24*365*10) # 10 yrs - hard to beat this kind of cert!
    cacert.set_issuer(careq.get_subject())
    cacert.set_subject(careq.get_subject())
    cacert.set_pubkey(careq.get_pubkey())
    cacert.set_version(2)

    # Set the extensions in two passes
    cacert.add_extensions([
        crypto.X509Extension('basicConstraints', True,'CA:TRUE'),
        crypto.X509Extension('subjectKeyIdentifier' , True , 'hash', subject=cacert)
    ])

    # ... now we can set the authority key since it depends on the subject key
    cacert.add_extensions([
        crypto.X509Extension('authorityKeyIdentifier' , False, 'issuer:always, keyid:always', issuer=cacert, subject=cacert)
    ])

    cacert.sign(cakey, hashalgorithm)
    return (cacert, cakey)

# Create a new slave cert.
def create_slave_certificate(csr, cakey, cacert, serial):
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60*60*24*365*10) # 10 yrs - hard to beat this kind of cert!
    cert.set_issuer(cacert.get_subject())
    cert.set_subject(csr.get_subject())
    cert.set_pubkey(csr.get_pubkey())
    cert.set_version(2)

    extensions = []
    extensions.append(crypto.X509Extension('basicConstraints'.encode('ascii'), False ,'CA:FALSE'.encode('ascii')))

    extensions.append(crypto.X509Extension('subjectKeyIdentifier'.encode('ascii') , False , 'hash'.encode('ascii'), subject=cert))
    extensions.append(crypto.X509Extension('authorityKeyIdentifier'.encode('ascii') , False, 'keyid:always,issuer:always'.encode('ascii'), subject=cacert, issuer=cacert))

    cert.add_extensions(extensions)
    cert.sign(cakey, 'sha256WithRSAEncryption')

    return cert

# Dumps content to a string
def dump_file_in_mem(material, format=crypto.FILETYPE_PEM):
    dump_func = None
    if isinstance(material, crypto.X509):
        dump_func = crypto.dump_certificate
    elif isinstance(material, crypto.PKey):
        dump_func = crypto.dump_privatekey
    elif isinstance(material, crypto.X509Req):
        dump_func = crypto.dump_certificate_request
    else:
        raise Exception("Don't know how to dump content type to file: %s (%r)" % (type(material), material))

    return dump_func(format, material)


# Loads the file into the appropriate openssl object type.
def load_from_file(materialfile, objtype, format=crypto.FILETYPE_PEM):
    if objtype is crypto.X509:
        load_func = crypto.load_certificate
    elif objtype is crypto.X509Req:
        load_func = crypto.load_certificate_request
    elif objtype is crypto.PKey:
        load_func = crypto.load_privatekey
    else:
        raise Exception("Unsupported material type: %s" % (objtype,))

    with open(materialfile, 'r') as fp:
        buf = fp.read()

    material = load_func(format, buf)
    return material

def retrieve_key_from_file(keyfile):
    return load_from_file(keyfile, crypto.PKey)

def retrieve_csr_from_file(csrfile):
    return load_from_file(csrfile, crypto.X509Req)

def retrieve_cert_from_file(certfile):
    return load_from_file(certfile, crypto.X509)


def create_certificate(ca_cert, ca_key, name, clientcsrname, clientcertname, clientkeyname, serial, filepath):

    cacert = retrieve_cert_from_file(ca_cert)
    cakey  = retrieve_key_from_file(ca_key)

    # Generate a new private key pair for a new certificate.
    key = make_keypair()
    # Generate a certificate request
    csr = make_csr(key, name)
    # Sign the certificate with the new csr
    crt = create_slave_certificate(csr, cakey, cacert, serial)

    # Now we have a successfully signed certificate. We must now
    # create a .ovpn file and then dump it somewhere.
    clientkey  = dump_file_in_mem(key).decode('utf-8')
    clientcert = dump_file_in_mem(crt).decode('utf-8')
    clientcsr = dump_file_in_mem(csr).decode('utf-8')
    cacertdump = dump_file_in_mem(cacert).decode('utf-8')


    write_to_disk(filepath+name, clientkeyname, clientkey)
    write_to_disk(filepath+name, clientcsrname, clientcsr)
    write_to_disk(filepath+name, clientcertname, clientcert)
    
def revoke_certificate(ca_cert_path, ca_key_path, clr_path, cert_path):
    # load files
    try:
        with open(ca_cert_path) as ca_file:
            ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_file.read())
        with open(ca_key_ath) as ca_key_file:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())
    except IOError as e:
        log.error(e)
        raise

    with open(clr_path, 'r') as f:
        crl = crypto.load_crl(crypto.FILETYPE_PEM, f.read())

    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    revoked = crypto.Revoked()
    revoked.set_serial((hex(x509.get_serial_number())[2:]))
    crl.add_revoked(revoked)
    crl_text = crl.export(ca, ca_key)

    with open(clr_path, 'a') as f:
        f.write(crl_text)




if __name__ == "__main__":
    name = get_random_string(length=16)
    CreateSSLCertificate(name)
    print("Done")
