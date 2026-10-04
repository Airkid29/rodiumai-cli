import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from rodiumai import RodiumAI

load_dotenv()

RODIUMAI_API_KEY = os.getenv("RODIUMAI_API_KEY")
if not RODIUMAI_API_KEY:
    raise SystemExit("Erreur : RODIUMAI_API_KEY manquant dans le fichier .env")

client = RodiumAI(api_key=RODIUMAI_API_KEY, timeout=60.0)

CHAT_MODEL = "google/gemini-3.1-flash-lite"
IMAGE_MODEL = "openai/gpt-image-1-mini"
VIDEO_MODEL = "google/veo-3.1-lite"


async def step_chat() -> bool:
    question = input("Votre question : ").strip()
    if not question:
        print("Question vide.")
        return False

    response = await client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": question}],
    )
    print(response.choices[0].message.content)
    print(f"Coût : {response.cost_rodi} RODI")
    return True


async def step_image() -> bool:
    prompt = input("Décrivez l'image : ").strip()
    if not prompt:
        print("Description vide.")
        return False

    response = await client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        size="1024x1024",
        timeout=120,
    )

    item = response.data[0]
    if item.b64_json:
        image_bytes = base64.b64decode(item.b64_json)
        Path("image.png").write_bytes(image_bytes)
        print("Image enregistrée : image.png")
        return True

    if item.url:
        import httpx
        img = httpx.get(item.url, timeout=60)
        Path("image.png").write_bytes(img.content)
        print("Image enregistrée : image.png")
        return True

    print("Aucune image reçue.")
    return False


async def step_video() -> bool:
    prompt = input("Décrivez la vidéo : ").strip()
    if not prompt:
        print("Description vide.")
        return False

    duration = input("Durée en secondes (Entrée pour 4) : ").strip()
    duration_seconds = int(duration) if duration.isdigit() and int(duration) > 0 else 4

    response = await client.video.generations.create(
        model=VIDEO_MODEL,
        prompt=prompt,
        duration_seconds=duration_seconds,
        timeout=150,
    )

    item = response.data[0]
    if item.url:
        import httpx
        video = httpx.get(item.url, timeout=150)
        Path("video.mp4").write_bytes(video.content)
        print("Vidéo enregistrée : video.mp4")
        return True

    if item.b64_json:
        video_bytes = base64.b64decode(item.b64_json)
        Path("video.mp4").write_bytes(video_bytes)
        print("Vidéo enregistrée : video.mp4")
        return True

    print("Aucune vidéo reçue.")
    return False


async def main():
    step = 1
    while True:
        if step == 1:
            print("\n=== Étape 1 : Chat ===")
            await step_chat()
            while True:
                choice = input("Rester sur cette étape (r) ou passer à la suivante (s) ? ").strip().lower()
                if choice == "r":
                    break
                if choice == "s":
                    step = 2
                    break
                print("Choix invalide. Saisir 'r' ou 's'.")

        elif step == 2:
            print("\n=== Étape 2 : Image ===")
            await step_image()
            while True:
                choice = input("Revenir en arrière (b), rester (r) ou passer à la suivante (s) ? ").strip().lower()
                if choice == "b":
                    step = 1
                    break
                if choice == "r":
                    break
                if choice == "s":
                    step = 3
                    break
                print("Choix invalide. Saisir 'b', 'r' ou 's'.")

        elif step == 3:
            print("\n=== Étape 3 : Vidéo ===")
            await step_video()
            while True:
                choice = input("Revenir en arrière (b), rester (r) ou quitter (q) ? ").strip().lower()
                if choice == "b":
                    step = 2
                    break
                if choice == "r":
                    break
                if choice == "q":
                    print("Fin du programme.")
                    return
                print("Choix invalide. Saisir 'b', 'r' ou 'q'.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
