# 🎵 Music Recommender Simulation

## Project Summary

This project extends the original "Music Recommender Simulation" from earlier modules by adding explanation generation, logging, and reliability testing.

This recommender uses content-based filtering to suggest songs
based on a user's genre, mood, and energy preferences. It scores
each song and returns the top matches.

---

## How The System Works

This recommender uses content-based filtering. It compares each
song's genre, mood, energy, and tempo to the user's preferences.

**Song features used:** genre, mood, energy, tempo_bpm, valence, danceability

**UserProfile stores:** preferred_genre, preferred_mood, preferred_energy, preferred_tempo

**Scoring Rule (one song):**
- Genre match = +2.0 points
- Mood match = +1.0 point
- Energy closeness = up to +1.0 point

**Ranking Rule (all songs):** Sort all songs by score, recommend the top 3.

---

## Getting Started

### Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
python3 -m src.main
```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

**Default profile: pop, happy, energy 0.8**

Results:
- Sunrise City — Score: 3.98 — Genre match + Mood match
- Gym Hero — Score: 2.87 — Genre match only
- Rooftop Lights — Score: 1.96 — Mood match only

Genre match had the biggest impact. Songs matching both genre
and mood scored highest.

---

## Limitations and Risks

- Only works on a tiny 10-song catalog
- Does not understand lyrics or context
- May over-favor one genre if catalog is unbalanced

---

## Reflection

Building this recommender showed me that real systems like Spotify
use the same basic idea: compare user preferences to item features,
score everything, and rank the results. The main risk of bias is
that if the catalog has more pop songs, pop users always win.
Human judgment is still needed to ensure diverse and fair results.

---

## System Architecture

### Overview

The system follows a pipeline from user input to recommendation output:

User Preferences
        ↓
Recommender System (recommend_songs)
        ↓
Scoring Engine (genre, mood, energy, popularity)
        ↓
Explanation Generator (explain_recommendation)
        ↓
Final Output (Top K songs with explanations)

### Components

- **Recommender System:** Main function that processes user input and ranks songs  
- **Scoring Engine:** Computes similarity scores using features  
- **Explanation Generator:** Provides reasoning for each recommendation  
- **Logging System:** Tracks scoring and recommendation steps  
- **Testing System:** Uses pytest to ensure correctness  

### Data Flow

1. User provides preferences (genre, mood, energy)  
2. Songs are loaded from dataset  
3. Each song is scored based on similarity  
4. Top songs are selected  
5. Explanations are generated  
6. Results are displayed  

### Reliability and Testing

- Unit tests verify correctness of recommendations  
- Logging ensures transparency of the process  
- Guardrails handle edge cases (e.g., empty dataset)  

---

## Sample Interactions

### Example 1: High-Energy Pop User

Input:
- Genre: pop
- Mood: happy
- Energy: 0.9

Output:
- Sunrise City — Score: 4.77  
  Because: genre match (+2.0), mood match (+1.0), energy score (+0.87)

---

### Example 2: Chill Lofi User

Input:
- Genre: lofi
- Mood: chill
- Energy: 0.35

Output:
- Calm Nights — Score: 4.10  
  Because: genre match (+2.0), mood match (+1.0), energy score (+0.95)

---

## Design Decisions

- Used a rule-based scoring system instead of machine learning for simplicity and interpretability  
- Weighted genre highest (+2.0) because it is the strongest signal  
- Added explanation generation to improve transparency of recommendations  
- Included logging to track how scores are computed  

Trade-offs:
- Simpler system is easier to debug and understand  
- But less flexible compared to learning-based recommender systems  

---

## Testing Summary

- Unit tests verify recommendation logic using pytest  
- System tested on multiple user profiles  
- All tests pass successfully  

What worked:
- Ranking system produces reasonable recommendations  
- Explanation feature improves user understanding  

What didn’t:
- Small dataset limits diversity and realism of recommendations  

---

## Reliability and Evaluation

The system’s reliability was tested using automated unit tests and manual evaluation.

### Automated Testing

- All unit tests pass successfully using pytest  
- Tests verify that recommendations are generated correctly  
- Tests ensure the output format (song, score, explanation) is consistent  

### Logging and Guardrails

- Logging tracks the recommendation process and scoring steps  
- The system handles edge cases such as empty song lists safely  

### Manual Evaluation

We tested the system with multiple user profiles:

- High-energy users received energetic songs  
- Chill users received low-energy songs  
- Genre preference had the strongest influence  

### Summary

- All tests passed successfully  
- The system behaves consistently across different inputs  
- Reliability is limited by the small dataset size  

---

## Reflection and Ethics

### Limitations and Bias

The system has several limitations. It relies on a small dataset, which can lead to biased recommendations if certain genres are overrepresented. The scoring system also heavily favors genre matching, which may reduce diversity in recommendations.

---

### Potential Misuse and Prevention

The system could be misused by over-relying on popularity scores, which may reinforce mainstream trends and reduce exposure to less popular content. To prevent this, future improvements could include diversity constraints or fairness adjustments in scoring.

---

### What Surprised Me

During testing, I was surprised by how strongly genre weighting influenced results. Even when energy scores were close, genre matches dominated the ranking more than expected.

---

### Collaboration with AI

AI assistance was helpful in structuring the project and debugging issues, especially when resolving import errors and designing the scoring system.

However, one flawed suggestion was attempting to run Python import statements directly in the terminal, which caused confusion. This showed that AI suggestions still need to be carefully interpreted and verified.

Overall, AI acted as a useful assistant, but human judgment was necessary to ensure correctness.

<video controls src="Screen Recording 2026-04-29 at 02.55.51.mov" title="Title"></video>