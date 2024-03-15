# Praxissemesterbericht - WS2023/24 - Yan Wittmann

[![Semesterbericht PDF](https://img.shields.io/badge/Latest-Semesterbericht%20PDF-blue.svg)](https://nightly.link/YanWittmann/hsma-praxissemesterbericht-WS2023-24/workflows/main/main/Semesterbericht-PDF.zip)
[![Build LaTeX Document](https://github.com/YanWittmann/hsma-praxissemesterbericht-WS2023-24/actions/workflows/main.yml/badge.svg)](https://github.com/YanWittmann/hsma-praxissemesterbericht-WS2023-24/actions/workflows/main.yml)

Dieses Projekt enthält alle LaTex-Dateien und sonstige Ressourcen für meinen Praxissemesterbericht für das
Wintersemester 2023/24 an der Hochschule Mannheim.

## Arbeitgeber

Ich legte dieses Praxissemester bei der {metæffekt} GmbH ab.

- Website: https://metaeffekt.com/
- GitHub: https://github.com/org-metaeffekt

## Bauen des Dokuments

Eine gebaute Version des Dokuments kann über den obigen Badge heruntergeladen werden.
Ansonsten kann das Dokument auch lokal gebaut werden:

```shell
sudo apt update
sudo apt install texlive-full

git clone https://github.com/rmainer/latex-listings-powershell

pdflatex praksem.tex
biber praksem
pdflatex praksem.tex
pdflatex praksem.tex
```

## IntelliJ Plugin

MiKTeX installieren und den Pfad in IntelliJ eintragen.

Das SDK liegt unter Windows unter

```
~\AppData\Local\Programs\MiKTeX
```

## Bilder

![Yan beim BSI/CSAF Workshop](res/img/2023-12-14-yan-vor-dem-ish-muenchen.jpg)

![Yan beim Forum Open Source vom bitkom](res/img/2023-10-19-yan-ak-os.png)
