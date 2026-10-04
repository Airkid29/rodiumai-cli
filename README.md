# RodiumAI - Lynxium (Exercice 2)

Programme interactif en ligne de commande enchaînant trois étapes (Chat, Génération d'image et Vidéo) via l'API RodiumAI sans SDK tiers.
L'utilisateur peut naviguer librement entre les étapes pour recommencer, avancer ou revenir en arrière.

## Prérequis et installation des dépendances

Le projet utilise **Python 3.12** (compatible Python 3.10+).

Pour installer les dépendances nécessaires (`requests` et `python-dotenv`) :

```bash
pip install -r requirements.txt
```

## Configuration du fichier .env

Copiez le modèle d'environnement `.env.example` vers un fichier `.env` :

```bash
cp .env.example .env
```

Puis ouvrez le fichier `.env` et remplacez la valeur par votre clé d'API RodiumAI :

```env
RODIUMAI_API_KEY=rd_sk_votre_cle_reelle
```

## Lancement du script

Exécutez le script interactif :

```bash
python lynxium.py
```
*(ou `python main.py`)*
