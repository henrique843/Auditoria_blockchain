# parallelblockchain.py

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
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

    def _minerar_faixa(self, inicio, passo, dificuldade):
        alvo = "0" * dificuldade
        nonce = inicio

        while True:
            bloco_string = json.dumps({
                "index": self.index,
                "timestamp": self.timestamp,
                "evento": self.evento_auditoria,
                "hash_anterior": self.hash_anterior,
                "nonce": nonce
            }, sort_keys=True).encode()

            hash_calculado = hashlib.sha256(bloco_string).hexdigest()

            if hash_calculado.startswith(alvo):
                return nonce, hash_calculado

            nonce += passo

    def realizar_prova_de_trabalho(self, dificuldade, workers=None):
        if workers is None:
            workers = os.cpu_count() or 4

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    self._minerar_faixa,
                    inicio,
                    workers,
                    dificuldade
                )
                for inicio in range(workers)
            ]

            for future in as_completed(futures):
                nonce, hash_encontrado = future.result()

                self.nonce = nonce
                self.hash = hash_encontrado

                executor.shutdown(wait=False, cancel_futures=True)
                return


class ParallelBlockchainAuditoria:
    def __init__(self, dificuldade=3):
        self.dificuldade = dificuldade
        self.cadeia = [self.criar_bloco_genesis()]

    def criar_bloco_genesis(self):
        bloco_genesis = BlocoAuditoria(
            0,
            "INICIO DA AUDITORIA - SISTEMA INICIADO",
            "0"
        )

        bloco_genesis.realizar_prova_de_trabalho(self.dificuldade)
        return bloco_genesis

    def obter_ultimo_bloco(self):
        return self.cadeia[-1]

    def registrar_evento(self, evento):
        ultimo_bloco = self.obter_ultimo_bloco()

        novo_bloco = BlocoAuditoria(
            len(self.cadeia),
            evento,
            ultimo_bloco.hash
        )

        novo_bloco.realizar_prova_de_trabalho(self.dificuldade)
        self.cadeia.append(novo_bloco)

    @staticmethod
    def _validar_bloco(bloco_atual, bloco_anterior):
        if bloco_atual.hash != bloco_atual.calcular_hash():
            return False

        if bloco_atual.hash_anterior != bloco_anterior.hash:
            return False

        return True

    def validar_integridade(self):
        if len(self.cadeia) <= 1:
            return True

        workers = os.cpu_count() or 4

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    self._validar_bloco,
                    self.cadeia[i],
                    self.cadeia[i - 1]
                )
                for i in range(1, len(self.cadeia))
            ]

            for future in as_completed(futures):
                if not future.result():
                    executor.shutdown(wait=False, cancel_futures=True)
                    return False

        return True
