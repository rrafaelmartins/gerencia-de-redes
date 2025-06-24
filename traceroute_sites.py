import subprocess
import json
import time
import re
import os

sites = [
    "google.com", "wikipedia.org", "bbc.com", "cnn.com", "nytimes.com",
    "uol.com.br", "g1.globo.com", "clarin.com", "emol.com", "elcomercio.pe",
    "elpais.com", "spiegel.de", "lemonde.fr", "ansa.it", "rfi.fr",
    "japantimes.co.jp", "asahi.com", "thehindu.com", "straitstimes.com", "baidu.com",
    "aljazeera.com", "arabnews.com", "haaretz.com", "iranintl.com", "gulftoday.ae",
    "abc.net.au", "smh.com.au", "news.com.au", "nzherald.co.nz", "stuff.co.nz",
    "news24.com", "mg.co.za", "iol.co.za", "sowetanlive.co.za", "vanguardngr.com",
    "openai.com", "stackoverflow.com", "github.com", "linkedin.com", "youtube.com",
    "gov.br", "camara.leg.br", "senado.leg.br", "gov.uk", "whitehouse.gov",
    "un.org", "who.int", "unesco.org", "europa.eu", "data.gov",
    # Redes sociais e comunicação
    "facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com",
    "snapchat.com", "discord.com", "telegram.org", "whatsapp.com", "pinterest.com",
    "reddit.com", "tumblr.com", "vk.com", "weibo.com", "wechat.com",
    # Streaming e entretenimento
    "netflix.com", "disney.com", "hulu.com", "amazon.com", "primevideo.com",
    "hbo.com", "paramount.com", "apple.com", "applemusic.com", "spotify.com",
    "soundcloud.com", "twitch.tv", "tiktok.com", "vimeo.com", "dailymotion.com",
    # E-commerce
    "alibaba.com", "ebay.com", "etsy.com", "walmart.com", "target.com",
    "bestbuy.com", "shopify.com", "mercadolivre.com.br", "americanas.com.br", "magazineluiza.com.br",
    "casasbahia.com.br", "submarino.com.br", "extra.com.br", "carrefour.com.br", "pontofrio.com.br",
    # Tecnologia
    "microsoft.com", "apple.com", "ibm.com", "oracle.com", "salesforce.com",
    "adobe.com", "nvidia.com", "intel.com", "amd.com", "qualcomm.com",
    "samsung.com", "sony.com", "lg.com", "huawei.com", "xiaomi.com",
    # Educação e pesquisa
    "mit.edu", "harvard.edu", "stanford.edu", "berkeley.edu", "cambridge.org",
    "oxford.ac.uk", "nature.com", "sciencedirect.com", "ieee.org", "acm.org",
    # Bancos e finanças
    "itau.com.br", "bradesco.com.br", "bancodobrasil.com.br", "santander.com.br", "caixa.gov.br",
    "paypal.com", "visa.com", "mastercard.com", "nubank.com.br", "inter.co",
    # Notícias internacionais
    "theguardian.com", "reuters.com", "ap.org", "bloomberg.com", "wsj.com",
    "ft.com", "economist.com", "time.com", "newsweek.com", "usatoday.com",
    "washingtonpost.com", "latimes.com", "telegraph.co.uk", "independent.co.uk", "dailymail.co.uk",
    # Tecnologia e desenvolvimento
    "gitlab.com", "bitbucket.org", "docker.com", "kubernetes.io", "aws.amazon.com",
    "azure.microsoft.com", "cloud.google.com", "digitalocean.com", "heroku.com", "netlify.com",
    # Mídia e entretenimento brasileiro
    "globo.com", "folha.uol.com.br", "estadao.com.br", "veja.abril.com.br", "terra.com.br",
    "ig.com.br", "r7.com", "band.uol.com.br", "sbt.com.br", "record.com.br"
]

# Carrega progresso anterior se existir
if os.path.exists("rotas.json"):
    with open("rotas.json", "r") as f:
        resultados = json.load(f)
else:
    resultados = {}

for site in sites:
    if site in resultados:
        print(f"\n>>> PULANDO (já coletado): {site}")
        continue

    print(f"\n>>> RODANDO: {site}")
    try:
        proc = subprocess.Popen(
            ["traceroute", "-m", "20", site],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        rota = []
        for line in proc.stdout:
            print(line.strip())
            found = re.findall(r"(?:\d{1,3}\.){3}\d{1,3}", line)
            if found:
                rota.append(found[0])
        proc.wait()
        resultados[site] = rota

    except Exception as e:
        print(f"ERRO em {site}: {e}")
        resultados[site] = []

    # Salva progresso a cada site
    with open("rotas.json", "w") as f:
        json.dump(resultados, f, indent=2)

    time.sleep(1)

print("\n✅ Finalizado. Progresso completo salvo em rotas.json")