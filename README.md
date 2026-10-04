# RodiumAI CLI (Exercice 2 · Partie B)

Programme interactif en ligne de commande enchaînant trois étapes (Chat, génération d'image et vidéo) via l'API RodiumAI sans SDK tiers.
L'utilisateur peut naviguer librement entre les étapes pour recommencer, avancer ou revenir en arrière.

---

## Informations sur le projet

- **Formation** : Module 03 – *Utilisez les API IA avec RodiumAi* (Exercice 2 · Partie B : Script Python interactif).
- **Instructeur du module** : Jean Pierre AÏGBEDE, CTO de RodiumAi.
- **Auteur** : Projet personnel / script de travail.
- **Environnement de développement** : Écrit et testé sous **Windows 11** avec **PowerShell / Git Bash**.

---

## Prérequis et environnement virtuel (venv)

Le projet utilise **Python 3.12** (compatible Python 3.10+).

Il est fortement recommandé d'isoler les dépendances dans un environnement virtuel `venv` avant de lancer le programme.

### 1. Créer l'environnement virtuel

Depuis la racine du projet (`rodiumai_btcp`) :

```bash
python3 -m venv venv
```

### 2. Activer l'environnement virtuel

Sur Linux / macOS :

```bash
source venv/bin/activate
```

*(Sur Windows avec PowerShell : `.\venv\Scripts\Activate.ps1`)*

### 3. Installer les dépendances

Une fois l'environnement activé, installez les paquets requis (`requests` et `python-dotenv`) :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration du fichier .env

Copiez le fichier d'exemple `.env.example` vers un nouveau fichier `.env` :

```bash
cp .env.example .env
```

Éditez le fichier `.env` et renseignez votre clé secrète RodiumAi :

```env
RODIUMAI_API_KEY=rd_sk_votre_cle_reelle
```

> **Note** : Le fichier `.env` réel contenant votre clé secrète est automatiquement ignoré par git via `.gitignore`.

---

## Lancement du script

Assurez-vous que votre environnement virtuel est bien activé, puis lancez le programme interactif :

```bash
python main.py
```

*(Ou via `python rodiumai_cli.py`)*

---

## Fonctionnement et modèles utilisés

1. **Étape 1 - Chat** :
   - Modèle : `google/gemini-3.1-flash-lite` (Google Gemini, rapide et économique).
   - Envoie la question de l'utilisateur, affiche la réponse générée ainsi que le coût réel de la requête en RODI.
   - Options de navigation : Rester sur l'étape (`r`) ou passer à la suivante (`s`).

2. **Étape 2 - Image** :
   - Modèle : `openai/gpt-image-1-mini` (OpenAI).
   - Demande une description textuelle et propose optionnellement de renseigner un média ou dossier de référence pour guider la génération.
   - Décode la réponse `b64_json` et enregistre le fichier `image.png`.
   - Options de navigation : Revenir en arrière (`b`), rester (`r`) ou passer à la suivante (`s`).

3. **Étape 3 - Vidéo** :
   - Modèle : `google/veo-3.1-lite` (le modèle vidéo le moins coûteux du catalogue RodiumAi).
   - Demande une description, une durée en secondes (4s par défaut) et un média de référence optionnel.
   - Applique un timeout réseau de 150 secondes (2 min 30) et enregistre le fichier `video.mp4`.
   - Options de navigation : Revenir en arrière (`b`), rester (`r`) ou quitter (`q`).
