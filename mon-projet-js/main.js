import fs from 'node:fs';
import path from 'node:path';
import dotenv from 'dotenv';
import { RodiumAI } from 'rodiumai';

dotenv.config();

const apiKey = process.env.RODIUMAI_API_KEY;
if (!apiKey) {
  throw new Error('Erreur : RODIUMAI_API_KEY manquant dans le fichier .env');
}

const client = new RodiumAI({
  apiKey,
  baseURL: 'https://api.rodiumai.io/v1',
  timeout: 60000,
  streamTimeout: 600000,
  maxRetries: 3,
  defaultModel: 'google/gemini-3.1-flash-lite',
});

const CHAT_MODEL = 'google/gemini-3.1-flash-lite';
const IMAGE_MODEL = 'openai/gpt-image-1-mini';
const VIDEO_MODEL = 'google/veo-3.1-lite';

async function stepChat() {
  const question = await promptUser('Votre question : ');
  if (!question) {
    console.log('Question vide.');
    return false;
  }

  const response = await client.chat(
    [{ role: 'user', content: question }],
    { model: CHAT_MODEL }
  );

  console.log(response.choices[0].message.content);
  console.log(`Coût : ${response.cost_rodi ?? 0} RODI`);
  return true;
}

async function stepImage() {
  const prompt = await promptUser('Décrivez l\'image : ');
  if (!prompt) {
    console.log('Description vide.');
    return false;
  }

  const response = await client.images.generate({
    model: IMAGE_MODEL,
    prompt,
    size: '1024x1024',
    timeout: 120000,
  });

  const first = response.data[0];
  if (first?.b64_json) {
    const buffer = Buffer.from(first.b64_json, 'base64');
    fs.writeFileSync(path.resolve('image.png'), buffer);
    console.log('Image enregistrée : image.png');
    return true;
  }

  if (first?.url) {
    const data = await fetch(first.url);
    const bytes = Buffer.from(await data.arrayBuffer());
    fs.writeFileSync(path.resolve('image.png'), bytes);
    console.log('Image enregistrée : image.png');
    return true;
  }

  console.log('Aucune image reçue.');
  return false;
}

async function stepVideo() {
  const prompt = await promptUser('Décrivez la vidéo : ');
  if (!prompt) {
    console.log('Description vide.');
    return false;
  }

  const rawDuration = await promptUser('Durée en secondes (Entrée pour 4) : ');
  const durationSeconds = rawDuration && Number.isInteger(Number(rawDuration)) && Number(rawDuration) > 0
    ? Number(rawDuration)
    : 4;

  const response = await client.videos({
    model: VIDEO_MODEL,
    prompt,
    duration_seconds: durationSeconds,
    timeout: 150000,
  });

  const first = response.data[0];
  if (first?.url) {
    const data = await fetch(first.url);
    const bytes = Buffer.from(await data.arrayBuffer());
    fs.writeFileSync(path.resolve('video.mp4'), bytes);
    console.log('Vidéo enregistrée : video.mp4');
    return true;
  }

  if (first?.b64_json) {
    const buffer = Buffer.from(first.b64_json, 'base64');
    fs.writeFileSync(path.resolve('video.mp4'), buffer);
    console.log('Vidéo enregistrée : video.mp4');
    return true;
  }

  console.log('Aucune vidéo reçue.');
  return false;
}

async function promptUser(label) {
  const readline = await import('node:readline/promises');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  const answer = await rl.question(label);
  rl.close();
  return answer;
}

async function main() {
  let step = 1;

  while (true) {
    if (step === 1) {
      console.log('\n=== Étape 1 : Chat ===');
      await stepChat();
      while (true) {
        const choice = (await promptUser("Rester sur cette étape (r) ou passer à la suivante (s) ? ")).trim().toLowerCase();
        if (choice === 'r') break;
        if (choice === 's') { step = 2; break; }
        console.log("Choix invalide. Saisir 'r' ou 's'.");
      }
    } else if (step === 2) {
      console.log('\n=== Étape 2 : Image ===');
      await stepImage();
      while (true) {
        const choice = (await promptUser("Revenir en arrière (b), rester (r) ou passer à la suivante (s) ? ")).trim().toLowerCase();
        if (choice === 'b') { step = 1; break; }
        if (choice === 'r') break;
        if (choice === 's') { step = 3; break; }
        console.log("Choix invalide. Saisir 'b', 'r' ou 's'.");
      }
    } else {
      console.log('\n=== Étape 3 : Vidéo ===');
      await stepVideo();
      while (true) {
        const choice = (await promptUser("Revenir en arrière (b), rester (r) ou quitter (q) ? ")).trim().toLowerCase();
        if (choice === 'b') { step = 2; break; }
        if (choice === 'r') break;
        if (choice === 'q') { console.log('Fin du programme.'); return; }
        console.log("Choix invalide. Saisir 'b', 'r' ou 'q'.");
      }
    }
  }
}

main().catch((error) => {
  console.error('Erreur JavaScript SDK :', error.message || error);
  process.exit(1);
});
