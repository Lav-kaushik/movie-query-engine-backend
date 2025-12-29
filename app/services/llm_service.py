import os
import json
from groq import Groq
from string import Template
from schemas.intent import SearchIntent


GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

PROMPT_TEMPLATE = Template(r"""
You are a movie intent parser for a TMDB-based search system. Your job is to analyze the user's query and extract structured information that can be used to search TMDB's API.

The user query may be:
- A direct movie title ("The Dark Knight")
- A descriptive request ("mind-bending sci-fi like Inception")
- A mood/tone request ("light romantic comedy for date night")
- A combination request ("Tom Cruise action movies directed by Christopher McQuarrie")

Extraction rules:
1. If the query contains explicit movie titles, list them in 'titles'
2. If NO explicit title is present, provide ONE well-known movie title that exemplifies the query intent
3. Fill other fields (genres, actors, directors) only when explicitly mentioned or strongly implied
4. Keywords should capture plot elements, themes, or mood not covered by other fields

User query: "$query"

Return ONLY a JSON object with this exact structure:
{
  "titles": [],       // Explicit movie titles from query OR one recommended title if none provided
  "keywords": [],     // Searchable keywords (plot elements, themes, mood descriptors)
  "actors": [],       // Actor names mentioned
  "directors": [],    // Director names mentioned  
  "genres": []        // Genre names (use TMDB standard genres when possible)
}

Examples of expected transformations:
- "I want to watch something like Inception" → {"titles": ["Inception"], "keywords": ["mind-bending"], "genres": ["Science Fiction", "Thriller"]}
- "Tom Hanks drama about space" → {"titles": ["Apollo 13"], "actors": ["Tom Hanks"], "keywords": ["space", "NASA"], "genres": ["Drama"]}
- "1980s sci-fi with robots" → {"titles": ["The Terminator"], "keywords": ["1980s", "robots", "cyborgs"], "genres": ["Science Fiction"]}
- "Christopher Nolan movie with time travel" → {"titles": ["Interstellar"], "directors": ["Christopher Nolan"], "keywords": ["time travel"], "genres": ["Science Fiction"]}

Critical guidelines:
• Return ONLY valid JSON - no additional text, markdown, or explanations
• For genre names, prefer standard TMDB genres: Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Mystery, Romance, Science Fiction, TV Movie, Thriller, War, Western
• When adding a recommended title, choose the most iconic/well-known example
• Keep arrays empty when no relevant information is extracted
• Do not include above given Examples in Response
""")


def extract_intent(query: str) -> dict:
    prompt = PROMPT_TEMPLATE.substitute(query=query)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a movie intent parser. Return only JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        timeout=10,
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON returned by LLM: {raw_text}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("LLM output must be a JSON object")

    return SearchIntent.model_validate(parsed)

        
