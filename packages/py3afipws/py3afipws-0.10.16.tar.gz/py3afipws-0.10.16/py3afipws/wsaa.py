#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"Módulo para obtener un ticket de autorización del web service WSAA de AFIP"

# Basado en wsaa-client.php de Gerardo Fisanotti - DvSHyS/DiOPIN/AFIP -
# 13-apr-07
# Definir WSDL, CERT, PRIVATEKEY, PASSPHRASE, SERVICE, WSAAURL
# Devuelve TA.xml (ticket de autorización de WSAA)

__author__ = "Mariano Reingart (reingart@gmail.com)"
__copyright__ = "Copyright (C) 2008-2011 Mariano Reingart"
__license__ = "GPL 3.0"
__version__ = "2.10f"

import hashlib
import datetime
# import email
import os
import sys
import time
import traceback
import warnings
import unicodedata
from .php import date
from py3simplesoap.client import SimpleXMLElement
from .utils import (
    inicializar_y_capturar_excepciones,
    BaseWS,
    get_install_dir,
    # exception_info,
    safe_console
)
from OpenSSL import crypto
from base64 import b64encode

import logging
log = logging.getLogger()

# Constantes (si se usa el script de linea de comandos)
# El WSDL correspondiente al WSAA
WSDL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
CERT = "reingart.crt"        # El certificado X.509 obtenido de Seg. Inf.
PRIVATEKEY = "reingart.key"  # La clave privada del certificado CERT
PASSPHRASE = "xxxxxxx"  # La contraseña para firmar (si hay)
SERVICE = "wsfe"        # El nombre del web service al que se le pide el TA

# WSAAURL: la URL para acceder al WSAA, verificar http/https y wsaa/wsaahomo
WSAAURL = "https://wsaa.afip.gov.ar/ws/services/LoginCms"  # PRODUCCION!!!
# WSAAURL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms" # homologacion
SOAP_ACTION = 'http://ar.gov.afip.dif.facturaelectronica/'  # Revisar WSDL
SOAP_NS = "http://wsaa.view.sua.dvadac.desein.afip.gov"     # Revisar WSDL

# Verificación del web server remoto, necesario para verificar canal seguro
# CACERT = "conf/afip_ca_info.crt"  # WSAA CA Cert (Autoridades de Confiaza)
CACERT = ""  # WSAA CA Cert (Autoridades de Confiaza)

HOMO = False
TYPELIB = False
DEFAULT_TTL = 60*60*5       # five hours
DEBUG = False

# No debería ser necesario modificar nada despues de esta linea


def create_tra(service=SERVICE, ttl=2400):
    "Crear un Ticket de Requerimiento de Acceso (TRA)"
    tra = SimpleXMLElement(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<loginTicketRequest version="1.0">'
        '</loginTicketRequest>')
    tra.add_child('header')
    # El source es opcional. Si falta, toma la firma (recomendado).
    # tra.header.addChild('source','subject=...')
    # tra.header.addChild(
    #     'destination','cn=wsaahomo,o=afip,c=ar,serialNumber=CUIT 33693450239'
    # )
    tra.header.add_child('uniqueId', str(date('U')))
    tra.header.add_child('generationTime', str(date('c', date('U')-ttl)))
    tra.header.add_child('expirationTime', str(date('c', date('U')+ttl)))
    tra.add_child('service', service)
    return tra.as_xml().decode("utf8")


def sign_tra(tra, cert=CERT, privatekey=PRIVATEKEY, passphrase=""):
    "Firmar PKCS#7 el TRA y devolver CMS (recortando los headers SMIME)"
    log.warn("_______entrando en sign_tra_______")

    if True:
        try:
            tra = tra.encode("utf-8")
            try:
                pkey = crypto.load_privatekey(
                    crypto.FILETYPE_PEM, privatekey
                )
                sign_cert = crypto.load_certificate(
                    crypto.FILETYPE_PEM, cert
                )
            except Exception as e:
                log.warn('ERROR: %s' % str(e))
            PKCS7_NOSIGS = 0x4
            bio_in = crypto._new_mem_buf(tra)
            pkcs7 = crypto._lib.PKCS7_sign(
                sign_cert._x509, pkey._pkey, crypto._ffi.NULL, bio_in,
                PKCS7_NOSIGS
            )
            bio_out = crypto._new_mem_buf()
            crypto._lib.i2d_PKCS7_bio(bio_out, pkcs7)
            tra_signed = crypto._bio_to_string(bio_out)

            log.warn("tra_signed: " + str(tra_signed))
            log.warn("tra_signed: " + str(type(tra_signed)))
            return b64encode(tra_signed).decode("latin1")
        except Exception as e:
            log.warn("__out__ Exception: " + str(e))
            if isinstance(e, IOError) and e.errno == 2:
                warnings.warn(
                    "El ejecutable de OpenSSL no esta disponible en el PATH")
                raise


def call_wsaa(cms, location=WSAAURL, proxy=None, trace=False, cacert=None):
    "Llamar web service con CMS para obtener ticket de autorización (TA)"

    # creo la nueva clase
    wsaa = WSAA()
    try:
        wsaa.Conectar(proxy=proxy, wsdl=location, cache="", cacert=cacert)
        ta = wsaa.LoginCMS(cms)
        if not ta:
            raise RuntimeError(wsaa.Excepcion)
        else:
            return ta
    except Exception as e:
        print(e)
        raise


class WSAA(BaseWS):
    "Interfaz para el WebService de Autenticación y Autorización"
    _public_methods_ = [
        'CreateTRA', 'SignTRA', 'CallWSAA', 'LoginCMS', 'Conectar',
        'AnalizarXml', 'ObtenerTagXml', 'Expirado', 'Autenticar',
        'DebugLog', 'AnalizarCertificado',
        'CrearClavePrivada', 'CrearPedidoCertificado',
    ]
    _public_attrs_ = [
        'Token', 'Sign', 'ExpirationTime', 'Version',
        'XmlRequest', 'XmlResponse',
        'InstallDir', 'Traceback', 'Excepcion',
        'Identidad', 'Caducidad', 'Emisor',
        'SoapFault', 'LanzarExcepciones',
    ]
    _readonly_attrs_ = _public_attrs_[:-1]
    _reg_progid_ = "WSAA"
    _reg_clsid_ = "{6268820C-8900-4AE9-8A2D-F0A1EBD4CAC5}"

    if TYPELIB:
        _typelib_guid_ = '{30E9C94B-7385-4534-9A80-DF50FD169253}'
        _typelib_version_ = 2, 10
        _com_interfaces_ = ['IWSAA']

    # Variables globales para BaseWS:
    HOMO = HOMO
    WSDL = WSDL
    Version = "%s %s" % (__version__, HOMO and 'Homologación' or '')

    @inicializar_y_capturar_excepciones
    def CreateTRA(self, service="wsfe", ttl=2400):
        "Crear un Ticket de Requerimiento de Acceso (TRA)"
        return create_tra(service, ttl)

    @inicializar_y_capturar_excepciones
    def AnalizarCertificado(self, crt, binary=False):
        "Carga un certificado digital y extrae los campos más importantes"
        from M2Crypto import (
            BIO,
            # EVP,
            # RSA,
            X509
        )
        if binary:
            try:
                bio = BIO.MemoryBuffer(cert)
            except Exception as e:
                print(e)
                bio = BIO.MemoryBuffer(crt)
            x509 = X509.load_cert_bio(bio, X509.FORMAT_DER)
        else:
            if not crt.startswith("-----BEGIN CERTIFICATE-----"):
                crt = open(crt).read()
            bio = BIO.MemoryBuffer(crt)
            x509 = X509.load_cert_bio(bio, X509.FORMAT_PEM)
        if x509:
            self.Identidad = x509.get_subject().as_text()
            self.Caducidad = x509.get_not_after().get_datetime()
            self.Emisor = x509.get_issuer().as_text()
        return True

    @inicializar_y_capturar_excepciones
    def CrearClavePrivada(
        self, filename="privada.key", key_length=1024,
        pub_exponent=0x10001, passphrase=""
    ):
        "Crea una clave privada (private key)"
        from M2Crypto import RSA, EVP

        # only protect if passphrase was given (it will fail otherwise)
        callback = lambda *args, **kwarg: passphrase
        chiper = None if not passphrase else "aes_128_cbc"
        # create the RSA key pair (and save the result to a file):
        rsa_key_pair = RSA.gen_key(key_length, pub_exponent, callback)
        bio = BIO.MemoryBuffer()
        rsa_key_pair.save_key_bio(bio, chiper, callback)
        f = open(filename, "w")
        f.write(bio.read())
        f.close()
        # create a public key to sign the certificate request:
        self.pkey = EVP.PKey(md='sha1')
        self.pkey.assign_rsa(rsa_key_pair)

    @inicializar_y_capturar_excepciones
    def CrearPedidoCertificado(
        self, cuit="", empresa="", nombre="pyafipws",
        filename="empresa.csr"
    ):
        "Crear un certificate signing request (X509 CSR)"
        from M2Crypto import (
            RSA, EVP, X509
        )

        # create the certificate signing request (CSR):
        self.x509_req = X509.Request()

        # normalizar encoding (reemplazar acentos, eñe, etc.)
        if isinstance(empresa, str):
            empresa = unicodedata.normalize('NFKD', empresa)\
                    .encode('ASCII', 'ignore')
        if isinstance(nombre, str):
            nombre = unicodedata.normalize('NFKD', nombre)\
                    .encode('ASCII', 'ignore')

        # subjet: C=AR/O=[empresa]/CN=[nombre]/serialNumber=CUIT [nro_cuit]
        x509name = X509.X509_Name()
        # default OpenSSL parameters:
        kwargs = {"type": 0x1000 | 1, "len": -1, "loc": -1, "set": 0}
        x509name.add_entry_by_txt(field='C', entry='AR', **kwargs)
        x509name.add_entry_by_txt(field='O', entry=empresa, **kwargs)
        x509name.add_entry_by_txt(field='CN', entry=nombre, **kwargs)
        x509name.add_entry_by_txt(
            field='serialNumber', entry="CUIT %s" % cuit, **kwargs)
        self.x509_req.set_subject_name(x509name)

        # sign the request with the previously created key (CrearClavePrivada)
        self.x509_req.set_pubkey(pkey=self.pkey)
        self.x509_req.sign(pkey=self.pkey, md='sha256')
        # save the CSR result to a file:
        f = open(filename, "w")
        f.write(self.x509_req.as_pem())
        f.close()

    @inicializar_y_capturar_excepciones
    def SignTRA(self, tra, cert, privatekey, passphrase=""):
        "Firmar el TRA y devolver CMS"
        return sign_tra(
            tra,
            cert.encode('latin1'),
            privatekey.encode('latin1'),
            passphrase.encode("utf8")
        )

    @inicializar_y_capturar_excepciones
    def LoginCMS(self, cms):
        "Obtener ticket de autorización (TA)"
        log.warn("Entrando a LoginCMS")
        try:
            # log.warn("CMS: " + str(cms))
            results = self.client.loginCms(in0=str(cms))
        except Exception as e:
            log.warn("_______Chk1 ISSUE_______ " + str(e))
        ta_xml = results['loginCmsReturn']
        log.warn("_______Chk2_______")
        self.xml = ta = SimpleXMLElement(ta_xml)
        log.warn("_______Chk3_______")
        self.Token = str(ta.credentials.token)
        log.warn("_______Chk4_______")
        self.Sign = str(ta.credentials.sign)
        log.warn("_______Chk5_______")
        self.ExpirationTime = str(ta.header.expirationTime)
        return ta_xml

    def CallWSAA(self, cms, url="", proxy=None):
        "Obtener ticket de autorización (TA) -version retrocompatible-"
        self.Conectar("", url, proxy)
        ta_xml = self.LoginCMS(cms)
        if not ta_xml:
            raise RuntimeError(self.Excepcion)
        return ta_xml

    @inicializar_y_capturar_excepciones
    def Expirado(self, fecha=None):
        "Comprueba la fecha de expiración, devuelve si ha expirado"
        if not fecha:
            fecha = self.ObtenerTagXml('expirationTime')
        now = datetime.datetime.now()
        d = datetime.datetime.strptime(fecha[:19], '%Y-%m-%dT%H:%M:%S')
        return now > d

    def Autenticar(
        self, service, crt, key, wsdl=None, proxy=None, wrapper=None,
        cacert=None, cache=None, debug=False
    ):
        "Método unificado para obtener el ticket de acceso (cacheado)"

        self.LanzarExcepciones = True
        try:
            # sanity check: verificar las credenciales
            for filename in (crt, key):
                if not os.access(filename, os.R_OK):
                    raise RuntimeError("Imposible abrir %s\n" % filename)
            # creo el nombre para el archivo del TA (según credenciales y ws)
            hash = service + crt + key
            fn = "TA-%s.xml" % hashlib.md5(hash.encode("latin1")).hexdigest()
            if cache:
                fn = os.path.join(cache, fn)
            else:
                fn = os.path.join(self.InstallDir, "cache", fn)

            # leer el ticket de acceso (si fue previamente solicitado)
            if not os.path.exists(fn) or os.path.getsize(fn) == 0 or \
               os.path.getmtime(fn) + (DEFAULT_TTL) < time.time():
                # ticket de acceso (TA) vencido, crear un nuevo req. (TRA)
                if DEBUG:
                    print("Creando TRA...")
                tra = self.CreateTRA(service=service, ttl=DEFAULT_TTL)
                # firmarlo criptográficamente
                if DEBUG:
                    print("Frimando TRA...")
                cms = self.SignTRA(tra, crt, key)
                # concectar con el servicio web:
                if DEBUG:
                    print("Conectando a WSAA...")
                ok = self.Conectar(cache, wsdl, proxy, wrapper, cacert)
                if not ok or self.Excepcion:
                    raise RuntimeError(
                        "Fallo la conexión: %s" % self.Excepcion)
                # llamar al método remoto para solicitar el TA
                if DEBUG:
                    print("Llamando WSAA...")
                ta = self.LoginCMS(cms)
                if not ta:
                    raise RuntimeError(
                        "Ticket de acceso vacio: %s" % WSAA.Excepcion)
                # grabar el ticket de acceso para poder reutilizarlo luego
                if DEBUG:
                    print(("Grabando TA en %s..." % fn))
                try:
                    open(fn, "w").write(ta)
                except IOError as e:
                    print(e)
                    self.Excepcion = "Imposible grabar ticket de \
                            accesso: %s" % fn
            else:
                # leer el ticket de acceso del archivo en cache
                if DEBUG:
                    print(("Leyendo TA de %s..." % fn))
                ta = open(fn, "r").read()
            # analizar el ticket de acceso y extraer los datos relevantes
            self.AnalizarXml(xml=ta)
            self.Token = self.ObtenerTagXml("token")
            self.Sign = self.ObtenerTagXml("sign")
        except Exception as e:
            ta = ""
            if not self.Excepcion:
                # avoid encoding problem when reporting exceptions to the user:
                self.Excepcion = traceback.format_exception_only(
                    sys.exc_info()[0],
                    sys.exc_info()[1])[0]
                self.Traceback = ""
            if DEBUG or debug:
                raise
        return ta


# busco el directorio de instalación (global para que no cambie si usan
# otra dll)
INSTALL_DIR = WSAA.InstallDir = get_install_dir()


if __name__ == "__main__":

    safe_console()

    if '--register' in sys.argv or '--unregister' in sys.argv:
        import pythoncom
        if TYPELIB:
            if '--register' in sys.argv:
                tlb = os.path.abspath(
                    os.path.join(INSTALL_DIR, "typelib", "wsaa.tlb"))
                print(("Registering %s" % (tlb,)))
                tli = pythoncom.LoadTypeLib(tlb)
                pythoncom.RegisterTypeLib(tli, tlb)
            elif '--unregister' in sys.argv:
                k = WSAA
                pythoncom.UnRegisterTypeLib(k._typelib_guid_,
                                            k._typelib_version_[0],
                                            k._typelib_version_[1],
                                            0,
                                            pythoncom.SYS_WIN32)
                print("Unregistered typelib")
        import win32com.server.register
        win32com.server.register.UseCommandLine(WSAA)
    elif "/Automate" in sys.argv:
        # MS seems to like /automate to run the class factories.
        import win32com.server.localserver
        # win32com.server.localserver.main()
        # start the server.
        win32com.server.localserver.serve([WSAA._reg_clsid_])
    elif "--crear_pedido_cert" in sys.argv:
        # instanciar el helper y revisar los parámetros
        wsaa = WSAA()
        args = [arg for arg in sys.argv if not arg.startswith("--")]
        # obtengo el CUIT y lo normalizo:
        cuit = len(args) > 1 and args[1] or eval(input("Ingrese un CUIT: "))
        cuit = ''.join([c for c in cuit if c.isdigit()])
        nombre = len(args) > 2 and args[2] or "PyAfipWs"
        # consultar el padrón online de AFIP si no se especificó razón social:
        empresa = len(args) > 3 and args[3] or ""
        if not empresa:
            from .padron import PadronAFIP
            padron = PadronAFIP()
            ok = padron.Consultar(cuit)
            if ok and padron.denominacion:
                print(("Denominación según AFIP:", padron.denominacion))
                empresa = padron.denominacion
            else:
                print(
                    ("CUIT %s no encontrado: %s..." % (cuit, padron.Excepcion))
                )
                empresa = eval(input("Empresa: "))
        # generar los archivos (con fecha para no pisarlo)
        ts = datetime.datetime.now().strftime("%Y%m%d%M%S")
        clave_privada = "clave_privada_%s_%s.key" % (cuit, ts)
        pedido_cert = "pedido_cert_%s_%s.csr" % (cuit, ts)
        wsaa.CrearClavePrivada(clave_privada)
        wsaa.CrearPedidoCertificado(cuit, empresa, nombre, pedido_cert)
        print("Se crearon los archivos:")
        print(clave_privada)
        print(pedido_cert)
        # convertir a terminación de linea windows y abrir con bloc de notas
        if sys.platform == "win32":
            txt = open(pedido_cert + ".txt", "wb")
            for linea in open(pedido_cert, "r"):
                txt.write("%s\r\n" % linea)
            txt.close()
            os.startfile(pedido_cert + ".txt")
    else:
        # Leer argumentos desde la linea de comando (si no viene tomar default)
        args = [arg for arg in sys.argv if arg.startswith("--")]
        argv = [arg for arg in sys.argv if not arg.startswith("--")]
        crt = len(argv) > 1 and argv[1] or CERT
        key = len(argv) > 2 and argv[2] or PRIVATEKEY
        service = len(argv) > 3 and argv[3] or "wsfe"
        ttl = len(argv) > 4 and int(argv[4]) or 36000
        url = len(argv) > 5 and argv[5] or WSAAURL
        wrapper = len(argv) > 6 and argv[6] or None
        cacert = len(argv) > 7 and argv[7] or CACERT
        DEBUG = "--debug" in args

        log.warn(
            "Usando CRT=%s KEY=%s URL=%s SERVICE=%s TTL=%s" % (
                crt, key, url, service, ttl)
        )

        # creo el objeto para comunicarme con el ws
        wsaa = WSAA()
        wsaa.LanzarExcepciones = True

        log.warn("WSAA Version %s %s" % (WSAA.Version, HOMO))

        if '--proxy' in args:
            proxy = sys.argv[sys.argv.index("--proxy")+1]
            log.warn("Usando PROXY:", proxy)
        else:
            proxy = None

        if '--analizar' in sys.argv:
            wsaa.AnalizarCertificado(crt)
            print((wsaa.Identidad))
            print((wsaa.Caducidad))
            print((wsaa.Emisor))

        ta = wsaa.Autenticar(service, crt, key, url, proxy, wrapper, cacert)
        if not ta:
            if DEBUG:
                log.warn(wsaa.Traceback)
            sys.exit("Excepcion: %s" % wsaa.Excepcion)

        else:
            print(ta)

        if wsaa.Excepcion:
            log.warn(wsaa.Excepcion)

        if DEBUG:
            print(("Source:", wsaa.ObtenerTagXml('source')))
            print(("UniqueID Time:", wsaa.ObtenerTagXml('uniqueId')))
            print(("Generation Time:", wsaa.ObtenerTagXml('generationTime')))
            print(("Expiration Time:", wsaa.ObtenerTagXml('expirationTime')))
            print(("Expiro?", wsaa.Expirado()))
            # import time; time.sleep(10)
            print("Expiro?", wsaa.Expirado())
