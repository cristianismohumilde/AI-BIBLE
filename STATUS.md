# Status do Projeto: IA-BIBLE (Ponto de Restauração - Fase GPU)

Este arquivo serve para documentar exatamente onde o projeto parou em **17/05/2026** (Transição para Escalonamento GPU).

## ✅ O que já está pronto:
1. **Ambiente de Testes (ARM64)**:
   - Configurado e funcional na instância A1.Flex (4 OCPUs, 24GB RAM, 100GB HD).
   - Containers Docker (`bible-ollama` e `bible-translator`) construídos e validados.
   - Scripts de download e tradução finalizados com resiliência total.
   - Banco de manuscritos JSON baixado com sucesso na pasta `data/`.
2. **Preparação para Escalonamento GPU**:
   - Conta atualizada com sucesso para **Pay As You Go (PAYG)**, garantindo acesso à solicitação de limites e preservação dos US$ 300 de créditos.
   - **Solicitação de Limite Enviada**: Ticket de suporte enviado com sucesso para a Oracle Cloud em 17/05/2026 solicitando o limite de `1` para o recurso `gpu-a10-count` (VM.GPU.A10.1) na região `sa-saopaulo-1-AD-1`.

## 🚧 O que falta fazer (Aguardando Aprovação do Limite):
1. **Aprovação do Limite**: Aguardar o e-mail da Oracle autorizando a cota `gpu-a10-count = 1` no painel.
2. **Provisionamento GPU**: Criar a nova instância Compute `VM.GPU.A10.1` (NVIDIA A10, 24GB VRAM) com Canonical Ubuntu 22.04 e 100GB de volume de boot.
3. **Clonar e Iniciar Infraestrutura**:
   - Clonar o repositório na nova GPU.
   - Executar o `docker compose up -d --build` (o Docker utilizará a aceleração GPU da NVIDIA).
4. **Executar Tradução**:
   - Puxar o modelo gigante de 32B: `docker compose exec ollama ollama pull qwen2.5:32b`
   - Rodar o tradutor em background usando `tmux` para rodar ultra rápido (~10 horas para a Bíblia inteira).
5. **Salvar Dados e Destruir a GPU**: Baixar a pasta `output/` gerada via `scp` e deletar a instância GPU imediatamente para zerar as cobranças.

## 💡 Como retomar:
Assim que o e-mail de aprovação do limite chegar, acesse o painel da Oracle Cloud, vá em instâncias e crie a máquina com o shape `VM.GPU.A10.1` seguindo o [GPU_DEPLOYMENT_PLAN.md](file:///c:/Users/venelouis/Desktop/REPOS/AI-BIBLE/GPU_DEPLOYMENT_PLAN.md).

---
*Assinado: Antigravity (Sua IA de programação)*
