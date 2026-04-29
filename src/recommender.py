from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv
import logging


logging.basicConfig(level=logging.INFO)


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []

        for song in self.songs:
            score = 0.0

            if song.genre == user.favorite_genre:
                score += 2.0

            if song.mood == user.favorite_mood:
                score += 1.0

            score += 1.0 - abs(song.energy - user.target_energy)

            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []

        if song.genre == user.favorite_genre:
            reasons.append("genre matches your preference")

        if song.mood == user.favorite_mood:
            reasons.append("mood matches your preference")

        reasons.append("energy level is close to your target")

        return "Recommended because " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    songs = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            songs.append({
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "popularity": float(row.get("popularity", 50)),
                "detailed_mood": row.get("detailed_mood", ""),
                "release_decade": row.get("release_decade", ""),
                "bpm_category": row.get("bpm_category", ""),
            })

    logging.info(f"Loaded {len(songs)} songs from {csv_path}")
    return songs


def explain_recommendation(song: Dict, score: float, reasons: str) -> str:
    title = song.get("title", "Unknown song")
    artist = song.get("artist", "Unknown artist")
    genre = song.get("genre", "unknown genre")
    mood = song.get("mood", "unknown mood")
    energy = song.get("energy", "unknown energy")

    return (
        f"{title} by {artist} was recommended with a score of {score}. "
        f"It matches the user's preferences because it has genre '{genre}', "
        f"mood '{mood}', and energy level {energy}. "
        f"Scoring details: {reasons}."
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    logging.info("Starting recommendation process")

    if not songs:
        logging.warning("No songs were provided to the recommender.")
        return []

    scored = []

    for song in songs:
        logging.info(f"Scoring song: {song.get('title', 'Unknown song')}")

        score = 0.0
        reasons = []

        if song["genre"] == user_prefs.get("genre"):
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song["mood"] == user_prefs.get("mood"):
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_gap = abs(song["energy"] - user_prefs.get("energy", 0.5))
        energy_score = round(1.0 - energy_gap, 2)
        score += energy_score
        reasons.append(f"energy score (+{energy_score})")

        pop_score = round(song["popularity"] / 100, 2)
        score += pop_score
        reasons.append(f"popularity (+{pop_score})")

        if song["detailed_mood"] == user_prefs.get("detailed_mood", ""):
            score += 0.5
            reasons.append("detailed mood match (+0.5)")

        final_score = round(score, 2)
        reason_text = ", ".join(reasons)
        explanation = explain_recommendation(song, final_score, reason_text)

        scored.append((song, final_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    logging.info(f"Recommendation process complete. Returning top {k} songs.")

    return scored[:k]