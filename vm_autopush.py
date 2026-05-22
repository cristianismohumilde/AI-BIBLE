#!/usr/bin/env python3
"""
vm_autopush.py
==============
Roda na VM Oracle Cloud. A cada 5 minutos:
  1. Faz git pull das alterações remotas
  2. Se translate_bible.py foi atualizado remotamente, reinicia o serviço
  3. Se vm_autopush.py foi atualizado remotamente, reinicia a si mesmo
  4. Garante que transliterate.py está rodando em background (catch-up contínuo)
  5. Gera PROGRESS.md e README.md atualizados
  6. Faz git add + commit + push de tudo que mudou

Uso: nohup python3 vm_autopush.py > autopush.log 2>&1 &
"""

import subprocess
import time
import os
import sys
from datetime import datetime

REPO = "/home/ubuntu/AI-BIBLE"
OUTPUT_DIR = os.path.join(REPO, "output")
TRANSLIT_FLAG = os.path.join(REPO, "translit_started.flag")


def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode == 0


def is_transliterate_running():
    """Verifica se transliterate.py está rodando em background."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "transliterate.py"],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def maybe_start_transliteration():
    """
    Garante que transliterate.py está rodando em background para catch-up contínuo.
    Roda mesmo que as traduções não estejam 100% concluídas — processa arquivos já prontos.
    """
    if is_transliterate_running():
        return  # Já está rodando

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Verifica se há alguma coleção com output já traduzido
    has_output = False
    try:
        for d in os.listdir(OUTPUT_DIR):
            col_path = os.path.join(OUTPUT_DIR, d)
            if os.path.isdir(col_path) and any(f.endswith(".json") for f in os.listdir(col_path)):
                has_output = True
                break
    except Exception:
        pass

    if not has_output:
        return  # Ainda não há nada para transliterar

    print(f"[{now}] 🔤 Iniciando transliterate.py em background (catch-up)...")

    # Cria/atualiza flag de controle
    with open(TRANSLIT_FLAG, "w") as f:
        f.write(f"iniciado em {now}")

    subprocess.Popen(
        [sys.executable, "transliterate.py"],
        cwd=REPO,
        stdout=open(os.path.join(REPO, "transliterate.log"), "a"),
        stderr=subprocess.STDOUT
    )
    print(f"[{now}] 🔤 transliterate.py iniciado. Log: transliterate.log")


def cycle():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 0. Sincroniza com as alterações remotas
    out, ok = run("git pull origin main --no-edit -X theirs")

    if ok and out:
        # Reinicia serviço de tradução se translate_bible.py foi atualizado
        if "translate_bible.py" in out:
            print(f"[{now}] translate_bible.py atualizado remotamente! Reiniciando serviço...")
            run("sudo systemctl restart translate_bible")

        # Auto-reload: reinicia vm_autopush.py se ele próprio foi atualizado
        if "vm_autopush.py" in out:
            print(f"[{now}] vm_autopush.py atualizado remotamente! Reiniciando autopush...")
            # Flush logs e reinicia o processo atual com o novo código
            sys.stdout.flush()
            sys.stderr.flush()
            os.execv(sys.executable, [sys.executable, os.path.join(REPO, "vm_autopush.py")])

    # 1. Gera arquivos de progresso
    run("python3 generate_progress.py")
    run("python3 generate_readme.py")

    # 2. Garante que transliterate.py está rodando em background
    maybe_start_transliteration()

    # 3. Adiciona tudo
    run("git add -A")

    # 4. Verifica se há mudanças
    status, _ = run("git status --porcelain")
    if not status:
        print(f"[{now}] Sem alterações. Aguardando...")
        return

    n = len(status.splitlines())

    # 5. Commit
    msg = f"Auto-push VM: {now} ({n} arquivos)"
    _, ok = run(f'git commit -m "{msg}"')
    if not ok:
        print(f"[{now}] Commit falhou.")
        return

    # 6. Push
    _, pushed = run("git push")
    status_str = "OK" if pushed else "FALHOU"
    print(f"[{now}] Push {status_str} — {n} arquivos atualizados")


def main():
    print("=" * 50)
    print("VM AutoPush ativo — ciclos de 5 minutos")
    print(f"Repositório: {REPO}")
    print("=" * 50)

    while True:
        try:
            cycle()
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro: {e}")
        time.sleep(300)


if __name__ == "__main__":
    main()
