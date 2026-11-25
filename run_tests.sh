#!/usr/bin/env bash

# Interrompe lo script se un comando fallisce
set -e

# Si posiziona nella directory del progetto
cd "$(dirname "$0")"

# Utilizza Python dell'ambiente virtuale, se presente
if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

echo "=================================="
echo " VirtualSquare - Test automatici"
echo "=================================="

# Esegue tutti i test presenti nella cartella tests
"$PYTHON" -m pytest tests/ -v
