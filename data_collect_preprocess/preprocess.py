import pandas as pd
from openai import OpenAI
import json

scrape = pd.read_csv('scrape.csv')\
           .rename(columns={'Unnamed: 0': 'id'})\
           .fillna(value={'Body': ""})
scrape['text'] = scrape.apply(lambda df: 'Title: ' + df['Title'] + '\nBody: ' + df['Body'], axis=1)\
                       .str.slice(0, 2000)
scrape_len = len(scrape)
scrape["is_political"] = [None for _ in range(scrape_len)]
scrape["is_politician_related"] = [None for _ in range(scrape_len)]
scrape["is_doom_posting"] = [None for _ in range(scrape_len)]
scrape["is_sensational"] = [None for _ in range(scrape_len)]
print(scrape)

key = open("text.txt", "r").readlines()[2]
client = OpenAI(api_key=key)



for i in range(int(scrape_len / 10)):
    posts = ""
    for j in range(10):
        loc = i*10 + j
        if loc < scrape_len:
            posts += f"<{loc}>{scrape['text'][loc]}</{loc}>\n"
    response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a helpful assistant. Your task is to indicate whether text is political, whether it is \"politician-related\", whether it is \"doomer\", and finally whether it is \"sensational\".\n\n\"Political\" text is text that describes or opines on public policy and the operation of the government. It may also concern \"bigger-picture\" topics such as structures of government and structures of power.\n\n\"Politician-related\" text is text concerning politicians, their personal character, and their everyday interpersonal drama.\n\n\"Doomer\" text is defined as text where the author has become very pessimistic about life or the world. Doomer text may express a sense of despair and futility about the state of life or the world. It may also make irrationally catastrophic predictions. Sometimes Doomer text may be angry, sometimes it may be sad.\n\n\"Sensational\" text is text that is written in such a way as to intrigue the reader in otherwise fickle content. Sensational text may appeal to the reader's sense of morbid curiosity or outrage or otherwise \"clickbait\" the reader.\n\nThe user will now input a list of texts"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"<input>\n{posts}</input>"
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
    "type": "json_schema",
    "json_schema": {
      "name": "classification_resonse",
      "strict": True,
      "schema": {
        "type": "object",
        "required": [
          "items"
        ],
        "additionalProperties": False,
        "properties": {
          "items": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "index": {
                  "type": "integer"
                },
                "classification": {
                  "type": "object",
                  "properties": {
                    "is_political": {
                      "type": "boolean"
                    },
                    "is_politician_related": {
                      "type": "boolean"
                    },
                    "is_doom_posting": {
                      "type": "boolean"
                    },
                    "is_sensational": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "is_political",
                    "is_politician_related",
                    "is_doom_posting",
                    "is_sensational"
                  ],
                  "additionalProperties": False
                }
              },
              "required": [
                "index",
                "classification"
              ],
              "additionalProperties": False
            }
          }
        }
      }
    }
  }
)
    j = json.loads(response.to_json())
    messages = json.loads(j["choices"][0]["message"]["content"])["items"]
    for item in messages:
        print(item)
        index = item["index"]
        scrape["is_political"][index] = item["classification"]["is_political"]
        scrape["is_politician_related"][index] = item["classification"]["is_politician_related"]
        scrape["is_doom_posting"][index] = item["classification"]["is_doom_posting"]
        scrape["is_sensational"][index] = item["classification"]["is_sensational"]
scrape.to_csv("preprocessed.csv")

