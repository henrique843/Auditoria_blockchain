# parallelblockchain.py

import hashlib
import time
import json


class BlocoAuditoria:
    def __init__(self, index, evento_auditoria, hash_anterior):
        self.index = index
        self.timestamp = time.time()
        self.evento_auditoria = evento_auditoria
        self.hash_anterior = hash_anterior
        self.nonce = 0
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        bloco_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "evento": self.evento_auditoria,
            "hash_anterior": self.hash_anterior,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(bloco_string).hexdigest()

    def realizar_prova_de_trabalho(self, dificuldade):
        alvo = '0' * dificuldade
        while self.hash[:dificuldade] != alvo:
            self.nonce += 1
            self.hash = self.calcular_hash()

class ParallelBlockchainAuditoria:
    def __init__(self, dificuldade=3):
        self.dificuldade = dificuldade
        self.cadeia = [self.criar_bloco_genesis()]

    def criar_bloco_genesis(self):
        bloco_genesis = BlocoAuditoria(0, "INICIO DA AUDITORIA - SISTEMA INICIADO", "0")
        bloco_genesis.realizar_prova_de_trabalho(self.dificuldade)
        return bloco_genesis

    def obter_ultimo_bloco(self):
        return self.cadeia[-1]

    def registrar_evento(self, evento):
        ultimo_bloco = self.obter_ultimo_bloco()
        novo_bloco = BlocoAuditoria(len(self.cadeia), evento, ultimo_bloco.hash)
        novo_bloco.realizar_prova_de_trabalho(self.dificuldade)
        self.cadeia.append(novo_bloco)

    def validar_integridade(self):
        for i in range(1, len(self.cadeia)):
            bloco_atual = self.cadeia[i]
            bloco_anterior = self.cadeia[i - 1]

            if bloco_atual.hash != bloco_atual.calcular_hash():
                return False

            if bloco_atual.hash_anterior != bloco_anterior.hash:
                return False

        return True
