# RodiumAI SDK Python

Petit projet Python qui reproduit l’exercice 2 avec le SDK `rodiumai`.

## Ce que fait le script

- Étape 1 : chat avec un modèle de conversation
- Étape 2 : génération d’une image et sauvegarde dans `image.png`
- Étape 3 : génération d’une vidéo et sauvegarde dans `video.mp4`
- Le programme permet de rester, revenir en arrière ou passer à la suite

## Prérequis

- Python 3.10+

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# ou .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
```

## Configuration

Copiez le fichier d’exemple et ajoutez votre clé RodiumAI :

```bash
cp .env.example .env
```

Dans le fichier `.env` :

```env
RODIUMAI_API_KEY=rd_sk_votre_cle
```

## Lancement

```bash
python main.py
```
