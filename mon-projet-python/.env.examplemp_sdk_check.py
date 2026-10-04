import os
import asyncio
from rodiumai import RodiumAI

async def main():
    client = RodiumAI(api_key=os.environ['RODIUMAI_API_KEY'])
    resp = await client.chat.completions.create(
        model='google/gemini-3.1-flash-lite',
        messages=[{'role': 'user', 'content': 'Réponds en une phrase.'}],
    )
    print(resp.choices[0].message.content[:200])
    print('COST', resp.cost_rodi)

asyncio.run(main())