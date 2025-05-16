import qrcode
from classes.order import Order
from classes.user.enterprise import Enterprise


class PixQrcode:
    def __init__(self, enterprise: Enterprise, order: Order):
        self._key = enterprise.pix_key
        self._name = enterprise.name
        self._city = enterprise.address.city    
        self._value_total = order.value_total


    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def value_total(self):
        return self._value_total

    @property
    def city(self):
        return self._city

    def calculate_crc16(self, data: str) -> str:
        """Calcula o CRC16 conforme especificação PIX"""
        from crcmod import mkCrcFun

        crc16 = mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
        calculated_crc = crc16(data.encode('utf-8'))
        return f"{calculated_crc:04X}"
        
    def generate_pix_payload(self, txid: str = None, description: str = None) -> str:
        key = self.key
        name = self.name
        city = self.city
        value_total = self.value_total
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

        if value_total is not None:
            amount_str = f"{value_total:.2f}"
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



    def generate_pix_qrcode(self,
        txid: str = None,
        description: str = None,  # seria msg, gostei de testar com isso por isso deixei
        save_path: str = None
    ):
        # payload seria o copia e cola
        payload = self.generate_pix_payload(
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

# from datetime import date, timedelta
# from pix import Pix, TypeKeyPix

# # Criando uma transação Pix
# pix = Pix(
#     value=100.50,
#     date=date.today(),
#     time_for_pay=timedelta(minutes=15),
#     payment_status="pendente",
#     key="teste@exemplo.com",
#     key_type=TypeKeyPix.EMAIL
# )

# #
