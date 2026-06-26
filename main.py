# Importa a classe do arquivo blockchain.py
from blockchain import BlockchainAuditoria


def simular_auditoria():
    print("Iniciando Sistema de Auditoria via Blockchain...\n")
    auditoria_log = BlockchainAuditoria(dificuldade=3)

    eventos = [
        "sshd[6302]: pam_unix: failure; user=root",
        "gdm[9447]: pam_unix: session opened for user rodr",
        "sshd[14127]: subsystem request for sftp"
    ]

    for evento in eventos:
        print(f"Registrando e minerando: '{evento}'")
        auditoria_log.registrar_evento(evento)
        print(f"-> Hash gerado: {auditoria_log.obter_ultimo_bloco().hash}\n")

    print("A cadeia de logs é válida e íntegra?", auditoria_log.validar_integridade())

    print("\n[!] ALERTA: Simulando adulteração de log por usuário malicioso...")
    auditoria_log.cadeia[1].evento_auditoria = "sshd[6302]: pam_unix: success; user=root"

    print("A cadeia de logs é válida após adulteração?", auditoria_log.validar_integridade())


if __name__ == "__main__":
    simular_auditoria()