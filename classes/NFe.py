from dataclasses import dataclass
from datetime import datetime
from client import Client
from enterprise import Enterprise
from order import Order

@dataclass
class NFe:
    issue: Client
    reciver: Enterprise
    product: list[Order]
    number: int
    serie: int = 1
    date_issue: datetime = datetime.now()
    
    def generate_xml(self) -> str:
        """Gera o XML da NF-e conforme o padrão da SEFAZ"""
        total = self.calcular_total()
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <nfe>
            <infNFe>
                <ide>
                    <cUF>35</cUF> <!-- Código da UF (Ex: 35 = SP) -->
                    <nNF>{self.number}</nNF>
                    <serie>{self.serie}</serie>
                    <dhEmi>{self.date_issue.isoformat()}</dhEmi>
                </ide>
                <emit>
                    <CNPJ>{self.issuer.cnpj}</CNPJ>
                    <xNome>{self.issuer.nome}</xNome>
                    <enderEmit>
                        <xLgr>{self.issuer.endereco}</xLgr>
                        <cMun>{self.issuer.cidade}</cMun>
                        <UF>{self.issuer.uf}</UF>
                        <CEP>{self.issuer.cep}</CEP>
                    </enderEmit>
                </emit>
                <dest>
                    <CPF>{self.reciver.cpf_cnpj}</CPF>
                    <xNome>{self.reciver.nome}</xNome>
                    <enderDest>
                        <xLgr>{self.reciver.endereco}</xLgr>
                        <cMun>{self.reciver.cidade}</cMun>
                        <UF>{self.reciver.uf}</UF>
                        <CEP>{self.reciver.cep}</CEP>
                    </enderDest>
                </dest>
                <det> <!-- Produtos -->
                    {''.join(
                        f'<prod><cProd>{p.codigo}</cProd><xProd>{p.descricao}</xProd>'
                        f'<qCom>{p.quantidade}</qCom><vUnCom>{p.valor_unitario}</vUnCom>'
                        f'<uCom>{p.unidade_medida}</uCom></prod>'
                        for p in self.produtos
                    )}
                </det>
                <total>
                    <ICMSTot>
                        <vNF>{total}</vNF>
                    </ICMSTot>
                </total>
            </infNFe>
        </nfe>"""
        return xml