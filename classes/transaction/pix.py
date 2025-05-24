import sqlite3
from typing import Optional

import qrcode
from crcmod import mkCrcFun

from classes.order import Order
from classes.user.enterprise import Enterprise


class PixQrcode:
    def __init__(self, enterprise: Enterprise, order: Order) -> None:
        """
        Inicializa o gerador de QRCode PIX com os dados da empresa e do pedido.

        Args:
            enterprise (Enterprise): Empresa que irá receber o pagamento.
            order (Order): Pedido vinculado ao pagamento.
        """
        self._key: str = enterprise.pix_key
        self._name: str = enterprise.name
        self._city: str = enterprise.address.city
        self._value_total: float = order.value_total

    @property
    def key(self) -> str:
        """Retorna a chave PIX da empresa."""
        return self._key

    @property
    def name(self) -> str:
        """Retorna o nome da empresa recebedora."""
        return self._name

    @property
    def city(self) -> str:
        """Retorna a cidade da empresa recebedora."""
        return self._city

    @property
    def value_total(self) -> float:
        """Retorna o valor total do pedido."""
        return self._value_total

    def calculate_crc16(self, data: str) -> str:
        """
        Calcula o CRC16 do payload conforme especificação do Banco Central.

        Args:
            data (str): String de dados para calcular o CRC.

        Retorna:
            str: Valor CRC16 calculado em hexadecimal.
        """
        crc16 = mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
        calculated_crc: int = crc16(data.encode("utf-8"))
        return f"{calculated_crc:04X}"

    def generate_pix_payload(self, txid: Optional[str], description: Optional[str]) -> str:
        """
        Gera o payload de pagamento PIX com base nas informações da empresa e pedido.

        Args:
            txid (Optional[str]): ID da transação.
            description (Optional[str]): Descrição opcional do pagamento.

        Retorna:
            str: Payload PIX formatado com CRC16.
        """
        key = self.key
        name = self.name
        city = self.city
        value_total = self.value_total

        gui = f"BR.GOV.BCB.PIX0114{key}"
        gui_len = f"{len(gui):02d}"
        merchant_account = f"0014{gui_len}{gui}"

        payload: list[str] = [
            "000201",  # Payload Format Indicator
            "26" + str(len(merchant_account)) + merchant_account,  # Merchant Info
            "52040000",  # Merchant Category Code
            "5303986",  # Transaction Currency (BRL)
        ]

        if value_total is not None:
            amount_str = f"{value_total:.2f}"
            payload.append(f"54{len(amount_str)}{amount_str}")

        payload.extend([
            "5802BR",  # País
            f"59{len(name[:25]):02d}{name[:25]}",  # Nome
            f"60{len(city[:15]):02d}{city[:15]}",  # Cidade
        ])

        if txid:
            txid = txid[:25]
            additional = f"050{len(txid):02d}{txid}"
            payload.append(f"62{len(additional):02d}{additional}")

        if description:
            description = description[:99]
            payload.append(f"05{len(description):02d}{description}")

        payload.append("6304")

        payload_str = "".join(payload)
        crc = self.calculate_crc16(payload_str)
        return payload_str + crc

    def generate_pix_qrcode(
        self,
        txid: Optional[str],
        description: Optional[str],
        save_path
    ):
        """
        Gera e salva um QRCode PIX com base no payload gerado.

        Args:
            txid (Optional[str]): ID da transação.
            description (Optional[str]): Descrição do pagamento.
            save_path (Optional[str]): Caminho para salvar a imagem do QRCode.

        Retorna:
            qrcode.image.pil.PilImage: Imagem gerada do QRCode.
        """
        payload: str = self.generate_pix_payload(txid=txid, description=description)
        qr = qrcode.make(payload)
        if save_path:
            qr.save(save_path)
            print(f"QRCode PIX salvo em: {save_path}")
        return qr

    def insert(self) -> None:
        """
        Insere os dados do PIX no banco de dados.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pix (key)
                VALUES (?);
                """,
                (self.key,),
            )
            conn.commit()

    @staticmethod
    def get_by_transaction(transaction_id: str) -> Optional[tuple]:
        """
        Busca um registro PIX pelo ID da transação.

        Args:
            transaction_id (str): ID da transação.

        Retorna:
            Optional[tuple]: Tupla com os dados do PIX, se encontrado.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pix WHERE transaction_id = ?;", (transaction_id,)
            )
            return cursor.fetchone()

    @staticmethod
    def delete_by_transaction(transaction_id: str) -> None:
        """
        Remove um registro PIX do banco de dados com base no ID da transação.

        Args:
            transaction_id (str): ID da transação.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM pix WHERE transaction_id = ?;", (transaction_id,)
            )
            conn.commit()
