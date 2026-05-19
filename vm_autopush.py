#!/usr/bin/env python3
"""
vm_autopush.py
==============
Roda na VM Oracle Cloud. A cada 5 minutos:
  1. Gera PROGRESS.md e README.md atualizados
  2. Faz git add + commit + push de tudo que mudou

Substitui completamente o sync_and_push.py do computador local.
O computador local pode simplesmente fazer git pull para ver o progresso.

Uso: nohup python3 vm_autopush.py > autopush.log 2>&1 &
"""

import subprocess
import time
from datetime import datetime

REPO = "/home/ubuntu/AI-BIBLE"


def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode == 0


def cycle():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Gera arquivos de progresso
    run("python3 generate_progress.py")
    run("python3 generate_readme.py")

    # 2. Adiciona tudo
    run("git add -A")

    # 3. Verifica se ha mudancas
    status, _ = run("git status --porcelain")
    if not status:
        print(f"[{now}] Sem alteracoes. Aguardando...")
        return

    n = len(status.splitlines())

    # 4. Commit
    msg = f"Auto-push VM: {now} ({n} arquivos)"
    _, ok = run(f'git commit -m "{msg}"')
    if not ok:
        print(f"[{now}] Commit falhou.")
        return

    # 5. Push
    _, pushed = run("git push")
    status_str = "OK" if pushed else "FALHOU"
    print(f"[{now}] Push {status_str} — {n} arquivos atualizados")


def main():
    print("=" * 50)
    print("VM AutoPush ativo — ciclos de 5 minutos")
    print(f"Repositorio: {REPO}")
    print("=" * 50)

    while True:
        try:
            cycle()
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro: {e}")
        time.sleep(300)


if __name__ == "__main__":
    main()
