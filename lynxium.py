import os
import base64
from pathlib import Path
import requests
from dotenv import load_dotenv

# Chargement de la configuration
load_dotenv()

RODIUMAI_API_KEY = os.getenv("RODIUMAI_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.rodiumai.io/v1").rstrip("/")

if not RODIUMAI_API_KEY:
    raise SystemExit("Erreur : RODIUMAI_API_KEY est manquante dans les variables d'environnement ou le fichier .env")

# Modèles
CHAT_MODEL = "google/gemini-2.5-flash-lite"
IMAGE_MODEL = "openai/gpt-image-1-mini"
VIDEO_MODEL = "google/veo-3.1-lite"

VIDEO_TIMEOUT = 150
VIDEO_DURATION = 4

HEADERS = {
    "Authorization": f"Bearer {RODIUMAI_API_KEY}",
    "Content-Type": "application/json",
}


def print_http_error(response: requests.Response) -> None:
    """Affiche un message clair avec l'error_code lors d'un échec HTTP."""
    try:
        data = response.json()
        err = data.get("error", {})
        error_code = err.get("code") or f"HTTP_{response.status_code}"
        message = err.get("message") or response.text
    except Exception:
        error_code = f"HTTP_{response.status_code}"
        message = response.text
    print(f"Erreur HTTP {response.status_code} [error_code: {error_code}] : {message}")


def encode_image(path: Path) -> str:
    """Encode une image locale en base64 pour l'API."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_reference_media() -> str | None:
    """Permet de fournir optionnellement un média (image ou dossier) pour s'inspirer."""
    entry = input("Média de référence (chemin image/dossier, Entrée pour ignorer) : ").strip()
    if not entry:
        return None

    path = Path(entry).expanduser().resolve()
    if path.is_file() and path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        return encode_image(path)
    elif path.is_dir():
        files = [f for f in path.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
        if files:
            print(f"Image de référence sélectionnée : {files[0].name}")
            return encode_image(files[0])
        print("Aucun fichier image compatible trouvé dans le dossier.")
    else:
        print("Chemin introuvable ou non valide, continuation sans média.")
    return None


def get_wallet_balance() -> float | None:
    """Récupère le solde actuel du wallet en RODI."""
    try:
        res = requests.get(f"{BASE_URL}/wallet", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return float(res.json().get("balance_rodi", 0.0))
    except Exception:
        pass
    return None


def step_chat() -> bool:
    """Étape 1 : Chat avec le modèle Gemini."""
    question = input("Votre question : ").strip()
    if not question:
        print("Question vide.")
        return False

    balance_before = get_wallet_balance()

    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"Erreur de connexion : {e}")
        return False

    if response.status_code != 200:
        print_http_error(response)
        return False

    data = response.json()
    reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(reply)

    # Récupération du coût en RODI
    cost = data.get("cost_rodi") or data.get("usage", {}).get("cost_rodi")
    if cost is None:
        balance_after = get_wallet_balance()
        if balance_before is not None and balance_after is not None:
            cost = max(0.0, round(balance_before - balance_after, 4))
        else:
            cost = 0.0

    print(f"Coût : {cost} RODI")
    return True


def step_image() -> bool:
    """Étape 2 : Génération d'image avec le modèle OpenAI."""
    prompt = input("Décrivez l'image : ").strip()
    if not prompt:
        print("Description vide.")
        return False

    b64_ref = get_reference_media()

    payload = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
    }
    if b64_ref:
        payload["image"] = {"b64_json": b64_ref}

    try:
        response = requests.post(
            f"{BASE_URL}/images/generations",
            headers=HEADERS,
            json=payload,
            timeout=120,
        )
    except requests.RequestException as e:
        print(f"Erreur de connexion : {e}")
        return False

    if response.status_code != 200:
        print_http_error(response)
        return False

    data = response.json()
    items = data.get("data", [])
    first_item = items[0] if items and isinstance(items[0], dict) else {}

    b64_data = first_item.get("b64_json") or data.get("b64_json")
    output_path = Path("image.png")

    if b64_data:
        if "," in b64_data and b64_data.strip().startswith("data:"):
            b64_data = b64_data.split(",", 1)[1]
        output_path.write_bytes(base64.b64decode(b64_data))
        print(f"Image enregistrée : {output_path.name}")
        return True
    elif first_item.get("url"):
        img_url = first_item["url"]
        img_res = requests.get(img_url, timeout=60)
        output_path.write_bytes(img_res.content)
        print(f"Image enregistrée : {output_path.name}")
        return True
    else:
        print("Aucune donnée d'image reçue dans la réponse de l'API.")
        return False


def step_video() -> bool:
    """Étape 3 : Génération d'une courte vidéo avec Veo 3.1 Lite."""
    prompt = input("Décrivez la vidéo : ").strip()
    if not prompt:
        print("Description vide.")
        return False

    b64_ref = get_reference_media()

    payload = {
        "model": VIDEO_MODEL,
        "prompt": prompt,
        "duration_seconds": VIDEO_DURATION,
        "aspect_ratio": "16:9",
    }
    if b64_ref:
        payload["image"] = {"b64_json": b64_ref}

    try:
        response = requests.post(
            f"{BASE_URL}/videos/generations",
            headers=HEADERS,
            json=payload,
            timeout=VIDEO_TIMEOUT,
        )
    except requests.RequestException as e:
        print(f"Erreur de connexion : {e}")
        return False

    if response.status_code != 200:
        print_http_error(response)
        return False

    data = response.json()
    items = data.get("data", [])
    first_item = items[0] if items and isinstance(items[0], dict) else {}

    video_url = first_item.get("url") or first_item.get("video_url") or data.get("url")
    b64_video = first_item.get("b64_json") or first_item.get("b64") or data.get("b64_json")

    output_path = Path("video.mp4")

    if video_url:
        res = requests.get(video_url, timeout=120)
        output_path.write_bytes(res.content)
        print(f"Vidéo enregistrée : {output_path.name}")
        return True
    elif b64_video:
        if "," in b64_video and b64_video.strip().startswith("data:"):
            b64_video = b64_video.split(",", 1)[1]
        output_path.write_bytes(base64.b64decode(b64_video))
        print(f"Vidéo enregistrée : {output_path.name}")
        return True
    else:
        print("Aucun contenu vidéo trouvé dans la réponse.")
        return False


def main():
    step = 1

    while True:
        if step == 1:
            print("\n=== Étape 1 : Chat ===")
            step_chat()
            while True:
                choice = input("Rester sur cette étape (r) ou passer à la suivante (s) ? ").strip().lower()
                if choice == "r":
                    break
                elif choice == "s":
                    step = 2
                    break
                print("Choix invalide. Saisir 'r' ou 's'.")

        elif step == 2:
            print("\n=== Étape 2 : Image ===")
            step_image()
            while True:
                choice = input("Revenir en arrière (b), rester (r) ou passer à la suivante (s) ? ").strip().lower()
                if choice == "b":
                    step = 1
                    break
                elif choice == "r":
                    break
                elif choice == "s":
                    step = 3
                    break
                print("Choix invalide. Saisir 'b', 'r' ou 's'.")

        elif step == 3:
            print("\n=== Étape 3 : Vidéo ===")
            step_video()
            while True:
                choice = input("Revenir en arrière (b), rester (r) ou quitter (q) ? ").strip().lower()
                if choice == "b":
                    step = 2
                    break
                elif choice == "r":
                    break
                elif choice == "q":
                    print("Fin du programme.")
                    return
                print("Choix invalide. Saisir 'b', 'r' ou 'q'.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterruption demandée. Au revoir !")
