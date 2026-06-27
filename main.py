# main.py

from blockchain import BlockchainAuditoria
from parallelblockchain import ParallelBlockchainAuditoria
BlockChain = ParallelBlockchainAuditoria

from random import choice, randint
from time import time

N_EVENTOS = 5


class Timer:
    def __init__(self, name):
        self.name = name
        self.time_init = time()

    def marcar(self):
        dt = time() - self.time_init
        print(f"{self.name}: {dt:.5f}s\n")


def simular_auditoria():
    timer = Timer("Sistema Iniciado")
    print("Iniciando Sistema de Auditoria via Blockchain...")
    auditoria_log = BlockChain(dificuldade=4)
    timer.marcar()

    timer = Timer("Lista Gerada")
    print("Gerando lista de eventos:")
    t_eventos = [
        "sshd[<n>]: pam_unix: failure; user=root",
        "gdm[<n>]: pam_unix: session opened for user rodr",
        "sshd[<n>]: subsystem request for sftp"
    ]
    eventos = [choice(t_eventos).replace("<n>", str(randint(1000, 99999))) for _ in range(N_EVENTOS)]
    for n, e in enumerate(eventos):
        print(n, e)
    timer.marcar()

    timer = Timer("Eventos Registrados e Minerados")
    print("Registrando e minerando eventos:")
    for n, evento in enumerate(eventos):
        print(f"{n/N_EVENTOS*100:.02f}%")
        print(f"Registrando e minerando: '{evento}'")
        auditoria_log.registrar_evento(evento)
        print(f"-> Hash gerado: {auditoria_log.obter_ultimo_bloco().hash}\n")
    timer.marcar()

    timer = Timer("Tempo")
    print("A cadeia de logs é válida e íntegra?", auditoria_log.validar_integridade())
    timer.marcar()

    timer = Timer("Tempo")
    print("\n[!] ALERTA: Simulando adulteração de log por usuário malicioso...")
    auditoria_log.cadeia[-2].evento_auditoria = "sshd[6302]: pam_unix: success; user=root"

    print("A cadeia de logs é válida após adulteração?", auditoria_log.validar_integridade())
    timer.marcar()


if __name__ == "__main__":
    simular_auditoria()
