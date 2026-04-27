import asyncio
from app.services.extractor import ExtractionService

async def main():
    extractor = ExtractionService()
    res = await extractor.extract("Can you delete interaction with Dr. Gandhi", {})
    print(res.model_dump(exclude_none=True))
    
    res2 = await extractor.extract("Can you delete interactions from 23rd April", {})
    print(res2.model_dump(exclude_none=True))

asyncio.run(main())
