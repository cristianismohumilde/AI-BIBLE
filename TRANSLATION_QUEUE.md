# Translation Queue — Prioritized Sources

Este arquivo lista a ordem priorizada de tradução e o status atual das fontes no repositório.

| Ordem | Fonte | Status | Localização |
|---:|---|---|---|
| 1 | Septuaginta (LXX) — Isaías, Salmos, Deuterocanônicos | Present | [data/LXX](data/LXX)
| 2 | Ge'ez (Ge'ez clássico) — Deuterocanônicos + NT | Present | [data/ancient_versions/geez_extracted](data/ancient_versions/geez_extracted)
| 3 | Manuscritos do Mar Morto (DSS) — tradução do inglês | Present (verificar cobertura) | [data/DSS](data/DSS)
| 4 | Targum Onkelos (Torá) | Present | [data/ancient_versions/targum_onkelos_genesis.json](data/ancient_versions/targum_onkelos_genesis.json)
| 5 | Texto Bizantino (BYZ) — NT | Present | [data/BYZ](data/BYZ)
| 6 | Peshitta Siríaca — NT | Present | [data/ancient_versions/peshitta_syriac.json](data/ancient_versions/peshitta_syriac.json)
| 7 | Copta Saídico — NT | Present | [data/ancient_versions/coptic_sahidic.json](data/ancient_versions/coptic_sahidic.json)
| 8 | Armênio Oriental — NT | Present | [data/ancient_versions/armenian_eastern.json](data/ancient_versions/armenian_eastern.json)

## Observações
- `Vulgata` e outras coleções (WLC, TR, SBLGNT, Talmud) foram marcadas como "fora dos recursos" para esta fase; há material de Vulgata em `data/VUL/` e uma captura de `4 Esdras` em `data/apocrypha/4_esdras_vulgate.json`.
- Para cada item "Present (verificar cobertura)", recomendo rodar uma verificação rápida de completude (ex.: contar capítulos/arquivos esperados) antes de enfileirar para tradução.

## Próximo passo sugerido
- Confirmar completude dos livros prioritários (scripts de verificação automatizados podem ser acrescentados em `tools/`) e então marcar capítulos em `TRANSLATION_QUEUE.md` como `Queued` por capítulo.
