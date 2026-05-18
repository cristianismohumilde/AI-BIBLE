#!/usr/bin/env python3
"""
download_talmud_extra.py
========================
Baixa os principais tratados do Talmud Bavli via Sefaria API.
Já existem: Berakhot, Shabbat, Sanhedrin.
Este script baixa os demais tratados principais.

Sefaria API: https://www.sefaria.org/api/texts/{tractate}
"""

import os, json, requests, time

OUT_DIR = "data/Talmud"

# Todos os tratados do Talmud Bavli disponíveis no Sefaria
# Organizados por Seder (ordem)
TRACTATES = {
    # Moed (Festas)
    "Eruvin":         "Eruvin",
    "Pesachim":       "Pesachim",
    "Yoma":           "Yoma",
    "Sukkah":         "Sukkah",
    "Beitzah":        "Beitzah",
    "Rosh_Hashanah":  "Rosh Hashanah",
    "Taanit":         "Taanit",
    "Megillah":       "Megillah",
    "Moed_Katan":     "Moed Katan",
    "Chagigah":       "Chagigah",
    # Nashim (Mulheres)
    "Yevamot":        "Yevamot",
    "Ketubot":        "Ketubot",
    "Nedarim":        "Nedarim",
    "Nazir":          "Nazir",
    "Sotah":          "Sotah",
    "Gittin":         "Gittin",
    "Kiddushin":      "Kiddushin",
    # Nezikin (Danos/Direito Civil)
    "Bava_Kamma":     "Bava Kamma",
    "Bava_Metzia":    "Bava Metzia",
    "Bava_Batra":     "Bava Batra",
    "Makkot":         "Makkot",
    "Shevuot":        "Shevuot",
    "Avodah_Zarah":   "Avodah Zarah",
    "Horayot":        "Horayot",
    # Kodashim (Coisas Sagradas)
    "Zevachim":       "Zevachim",
    "Menachot":       "Menachot",
    "Chullin":        "Chullin",
    "Bekhorot":       "Bekhorot",
    "Arakhin":        "Arakhin",
    "Temurah":        "Temurah",
    "Keritot":        "Keritot",
    "Meilah":         "Meilah",
    "Tamid":          "Tamid",
    # Taharot (Pureza)
    "Niddah":         "Niddah",
}

# Já baixados
ALREADY_DONE = {"Berakhot", "Shabbat", "Sanhedrin"}


def download_tractate(key, sefaria_name):
    """Baixa um tratado completo do Talmud via Sefaria."""
    out_path = f"{OUT_DIR}/{key}.json"
    if os.path.exists(out_path):
        print(f"  Pulando {key} (já existe)")
        return True

    print(f"  Baixando {key} ({sefaria_name})...")

    # Sefaria retorna o tratado inteiro de uma vez
    url = f"https://www.sefaria.org/api/texts/{sefaria_name.replace(' ', '_')}?lang=he"
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                d = r.json()
                if "error" not in d and d.get("text"):
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(d, f, ensure_ascii=False, indent=2)
                    size = os.path.getsize(out_path) // 1024
                    print(f"    OK: {key} salvo ({size} KB)")
                    return True
                elif "error" in d:
                    print(f"    Erro Sefaria: {d['error']}")
                    return False
            elif r.status_code == 404:
                # Tenta sem lang
                r2 = requests.get(f"https://www.sefaria.org/api/texts/{sefaria_name.replace(' ', '_')}", timeout=60)
                if r2.status_code == 200:
                    d2 = r2.json()
                    if "error" not in d2:
                        with open(out_path, "w", encoding="utf-8") as f:
                            json.dump(d2, f, ensure_ascii=False, indent=2)
                        size = os.path.getsize(out_path) // 1024
                        print(f"    OK: {key} salvo ({size} KB)")
                        return True
                return False
        except Exception as e:
            print(f"    Tentativa {attempt+1} falhou: {e}")
            time.sleep(3)
    return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("\n" + "="*60)
    print("📚 BAIXANDO TRATADOS DO TALMUD BAVLI (Sefaria)")
    print("="*60)
    print(f"Tratados já existentes: {ALREADY_DONE}")
    print(f"Tratados a baixar: {len(TRACTATES)}")

    success = 0
    failed = []

    for key, sefaria_name in TRACTATES.items():
        if key.replace("_", "") in {k.replace("_","") for k in ALREADY_DONE}:
            continue
        ok = download_tractate(key, sefaria_name)
        if ok:
            success += 1
        else:
            failed.append(key)
        time.sleep(1.5)  # Respeitar rate limit

    print(f"\n  Concluido: {success}/{len(TRACTATES)} tratados baixados.")
    if failed:
        print(f"  Falharam: {failed}")

    # Verifica total
    all_files = [f for f in os.listdir(OUT_DIR) if f.endswith(".json")]
    print(f"  Total de tratados em data/Talmud/: {len(all_files)}")


if __name__ == "__main__":
    main()
