#!/usr/bin/env bash
# Uso: verificar-http.sh <url> <regex-esperado-no-corpo|""> [argumentos extras do curl...]
#
# Espera HTTP 200 (e, se informado, o regex no corpo). Se falhar, tenta de novo
# após 3s, 6s e 12s: 1 tentativa inicial + 3 novas tentativas.
set -u

url="$1"
padrao="$2"
shift 2

esperas=(3 6 12)
total=$(( ${#esperas[@]} + 1 ))

for tentativa in $(seq 1 "$total"); do
  status=$(curl --silent --show-error --max-time 30 \
    --output resposta.txt --write-out '%{http_code}' "$@" "$url") || status="erro-de-rede"

  if [ "$status" = "200" ] && { [ -z "$padrao" ] || grep -Eq "$padrao" resposta.txt; }; then
    echo "OK na tentativa $tentativa/$total (HTTP $status)."
    exit 0
  fi

  echo "::warning::Tentativa $tentativa/$total falhou (HTTP $status)."
  if [ "$tentativa" -lt "$total" ]; then
    espera="${esperas[$((tentativa - 1))]}"
    echo "Nova tentativa em ${espera}s..."
    sleep "$espera"
  fi
done

echo "::error::Falhou nas $total tentativas (último status: $status)."
cat resposta.txt 2>/dev/null; echo
exit 1
