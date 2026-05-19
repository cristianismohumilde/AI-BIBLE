import os
import time
import subprocess
from datetime import datetime

# Configurações do ambiente local
PRIVATE_KEY_PATH = r"C:\Users\venelouis\Downloads\frank-private.key"
VM_IP = "130.61.86.70"
VM_USER = "ubuntu"
VM_OUTPUT_DIR = "~/AI-BIBLE/output/"
LOCAL_REPO_DIR = r"c:\Users\venelouis\Desktop\REPOS\AI-BIBLE"
LOCAL_OUTPUT_DIR = os.path.join(LOCAL_REPO_DIR, "output")

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
        return result.stdout.strip(), True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {command}\nStderr: {e.stderr}")
        return e.stderr, False

def sync_from_vm():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando sincronização SCP da VM...")
    # Comando SCP para trazer a pasta output da VM recursivamente para o local
    # Usando barra normal para compatibilidade no comando SCP
    scp_cmd = f'scp -r -i "{PRIVATE_KEY_PATH}" -o StrictHostKeyChecking=no {VM_USER}@{VM_IP}:{VM_OUTPUT_DIR}* "{LOCAL_OUTPUT_DIR}"'
    
    # Garantir que a pasta local exista
    os.makedirs(LOCAL_OUTPUT_DIR, exist_ok=True)
    
    output, success = run_command(scp_cmd)
    if success:
        print("Sincronização SCP concluída com sucesso!")
    return success

def commit_and_push():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verificando mudanças no Git...")
    
    # 1. Adicionar arquivos novos ao git
    _, s1 = run_command("git add output/", cwd=LOCAL_REPO_DIR)
    if not s1:
        return False
        
    # 2. Verificar se há alterações reais para commit
    status_out, _ = run_command("git status --porcelain", cwd=LOCAL_REPO_DIR)
    if not status_out:
        print("Nenhuma alteração pendente nas traduções. Pulando commit/push.")
        return True
        
    print("Alterações detectadas! Criando commit...")
    # 3. Fazer commit
    commit_msg = f"Auto-sync traduções da VM - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    _, s2 = run_command(f'git commit -m "{commit_msg}"', cwd=LOCAL_REPO_DIR)
    if not s2:
        return False
        
    print("Enviando alterações para o repositório remoto no GitHub...")
    # 4. Fazer push
    _, s3 = run_command("git push", cwd=LOCAL_REPO_DIR)
    if s3:
        print("Push concluído com sucesso!")
        return True
    return False

def main():
    print("==================================================================")
    print("🚀 Script de Sincronização Automática Ativo (5 em 5 minutos) 🚀")
    print(f"Local do Repositório: {LOCAL_REPO_DIR}")
    print(f"IP da VM: {VM_IP}")
    print("==================================================================")
    
    while True:
        try:
            # 1. Trazer dados mais novos da VM
            if sync_from_vm():
                # 2. Se a sincronização deu certo, fazer commit e push
                commit_and_push()
        except Exception as e:
            print(f"Erro inesperado durante a execução do ciclo: {e}")
            
        print(f"\nAguardando 5 minutos para o próximo ciclo de sincronização...")
        time.sleep(300)  # Aguardar 5 minutos (300 segundos)

if __name__ == "__main__":
    main()
