from transaction import Transaction
from enum import Enum
from uuid import uuid4
import qrcode


class TypeKeyPix(Enum):
    EMAIL = 'email'
    UUID = 'UUID'
    CELPHONE = 'celphone'
    CPF = 'CPF'
    CNPJ = 'cnpj'


class Pix(Transaction):
    def __init__(self, value, date, time_for_pay, payment_status, key, key_type):
        super().__init__(value, date, time_for_pay, payment_status)
        self._key = key
        self._key_type = key_type

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def key_type(self):
        return self._key_type

    @key_type.setter
    def key_type(self, value):
        self._key_type = value
        
    
    def generate_pix_payload(self,
        key: str,
        name: str,
        city: str,
        amount: float = None,
        txid: str = None,
        description: str = None) -> str:
        gui = f"BR.GOV.BCB.PIX0114{key}"
        gui_len = f"{len(gui):02d}"
        merchant_account = f"0014{gui_len}{gui}"
        
        # Obrigatório
        payload = [
            "000201",  # Payload Format Indicator
            "26" + str(len(merchant_account)) + merchant_account,  # Merchant Account Information
            "52040000",  # Merchant Category Code
            "5303986",  # Transaction Currency (BRL)
        ]

        if amount is not None:
            amount_str = f"{amount:.2f}"
            payload.append(f"54{len(amount_str)}{amount_str}")
        
        # País e quem recebe
        payload.extend([
            "5802BR",  # Country Code
            f"59{len(name[:25]):02d}{name[:25]}",  # Merchant Name
            f"60{len(city[:15]):02d}{city[:15]}",  # Merchant City
        ])
        
        # ID da transação
        if txid:
            txid = txid[:25]
            additional = f"050{len(txid):02d}{txid}"
            payload.append(f"62{len(additional):02d}{additional}")
        
        if description:
            description = description[:99]  # Limite arbitrário
            payload.append(f"05{len(description):02d}{description}")

        payload.append("6304")
        
        # Junta tudo e calcula o CRC
        payload_str = ''.join(payload)
        crc = self.calculate_crc16(payload_str)
        
        return payload_str + crc

    @staticmethod
    def calculate_crc16(data: str) -> str:
        """Calcula o CRC16 conforme especificação PIX(sim, isso eu descobri pelo gpt caso haja duvidas)""" 
        from crcmod import mkCrcFun
        
        crc16 = mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
        calculated_crc = crc16(data.encode('utf-8'))
        return f"{calculated_crc:04X}"

    def generate_pix_qrcode(self,
        key: str,
        name: str,
        city: str,
        amount: float = None,
        txid: str = None,
        description: str = None, # seria msg, gostei de testar com isso por isso deixei
        save_path: str = None
    ):
        #payload seria o copia e cola
        payload = self.generate_pix_payload(
            key=key,
            name=name,
            city=city,
            amount=amount,
            txid=txid,
            description=description
        )
        
        qr = qrcode.make(payload)
        
        if save_path:
            qr.save(save_path)
            print(f"QRCode PIX salvo em: {save_path}")
        else:
            qr.show()
        
        return qr



