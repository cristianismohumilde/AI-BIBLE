#!/usr/bin/env python3
"""
vm_autopush.py
==============
Roda na VM Oracle Cloud. A cada 5 minutos:
  1. Gera PROGRESS.md e README.md atualizados
  2. Faz git add + commit + push de tudo que mudou
  3. Se translate_bible.py foi atualizado remotamente, reinicia o serviço
  4. Se todas as traduções concluíram, aciona transliterate.py automaticamente

Uso: nohup python3 vm_autopush.py > autopush.log 2>&1 &
"""

import subprocess
import time
import os
from datetime import datetime

REPO = "/home/ubuntu/AI-BIBLE"
OUTPUT_DIR = os.path.join(REPO, "output")
TRANSLIT_FLAG = os.path.join(REPO, "translit_started.flag")


def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode == 0


def all_translations_done():
    """Verifica se todas as coleções ativas terminaram de traduzir."""
    try:
        # Importa as funções de contagem do generate_progress
        import sys
        sys.path.insert(0, REPO)
        import importlib.util
        spec = importlib.util.spec_from_file_location("gp", os.path.join(REPO, "generate_progress.py"))
        gp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gp)

        # Coleções ativas na fila (excluindo as pausadas)
        active_collections = ["Targum_Onkelos", "DSS", "BYZ", "Peshitta_Syriac", "Coptic_Sahidic", "Armenian_Eastern"]
        for col in active_collections:
            data = gp.count_data_files(col)
            out  = gp.count_output_files(col)
            if data > 0 and out < data:
                return False
        return True
    except Exception as e:
        print(f"  [translit-check] Erro ao verificar conclusão: {e}")
        return False


def maybe_start_transliteration():
    """Aciona transliterate.py se todas as traduções terminaram e ele ainda não foi iniciado."""
    if os.path.exists(TRANSLIT_FLAG):
        return  # Já foi acionado antes

    if not all_translations_done():
        return  # Ainda há traduções pendentes

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] ✅ Todas as traduções concluídas! Iniciando Fase de Transliteração...")

    # Cria flag para não re-acionar
    with open(TRANSLIT_FLAG, "w") as f:
        f.write(f"iniciado em {now}")

    # Inicia transliterate.py em background (sem bloquear o autopush)
    subprocess.Popen(
        ["python3", "transliterate.py"],
        cwd=REPO,
        stdout=open(os.path.join(REPO, "transliterate.log"), "a"),
        stderr=subprocess.STDOUT
    )
    print(f"[{now}] 🔤 transliterate.py iniciado em background. Log: transliterate.log")


def cycle():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 0. Sincroniza com as alterações remotas
    out, ok = run("git pull origin main --no-edit -X theirs")
    if ok and "translate_bible.py" in out:
        print(f"[{now}] translate_bible.py foi atualizado remotamente! Reiniciando o serviço...")
        run("sudo systemctl restart translate_bible")

    # 1. Gera arquivos de progresso
    run("python3 generate_progress.py")
    run("python3 generate_readme.py")

    # 2. Verifica se deve iniciar transliteração
    maybe_start_transliteration()

    # 3. Adiciona tudo
    run("git add -A")

    # 4. Verifica se ha mudancas
    status, _ = run("git status --porcelain")
    if not status:
        print(f"[{now}] Sem alteracoes. Aguardando...")
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
