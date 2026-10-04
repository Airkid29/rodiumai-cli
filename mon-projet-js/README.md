# RodiumAI SDK JavaScript

Petit projet JavaScript qui reproduit l’exercice 2 avec le SDK `rodiumai`.

## Ce que fait le script

- Étape 1 : chat avec un modèle de conversation
- Étape 2 : génération d’une image et sauvegarde dans `image.png`
- Étape 3 : génération d’une vidéo et sauvegarde dans `video.mp4`
- Le programme permet de rester, revenir en arrière ou passer à la suite

## Prérequis

- Node.js 18+

## Installation

```bash
npm install
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
npm start
```
