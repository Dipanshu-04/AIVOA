"""
Assumptions:
- Using `langchain-groq` for Groq LLM integration.
- `ChatGroq` with `with_structured_output` is used to enforce deterministic extraction.
- We extend `ExtractionResult` to include `uncertain_fields` as required by the extraction logic.
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.chat import ExtractionResult as BaseExtractionResult
from app.prompts.extraction_prompt import EXTRACTION_SYSTEM_PROMPT

class EnhancedExtractionResult(BaseExtractionResult):
    """Extends the base ExtractionResult with uncertain_fields as requested by the extraction requirements."""
    uncertain_fields: Optional[List[str]] = Field(None, description="List of field names that need clarification or are ambiguous")

class ExtractionService:
    def __init__(self, model_name: str = "openai/gpt-oss-120b", temperature: float = 0.1):
        """
        Initializes the extraction service using ChatGroq.
        """
        # We assume GROQ_API_KEY is available in the environment
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=1024,
        )
        
        # Use structured output to ensure deterministic JSON that maps directly to our Pydantic schema
        self.structured_llm = self.llm.with_structured_output(EnhancedExtractionResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", EXTRACTION_SYSTEM_PROMPT),
            ("human", "Current Draft Context: {draft}\n\nNew Input: {input}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    async def extract(self, user_input: str, current_draft: Optional[Dict[str, Any]] = None) -> EnhancedExtractionResult:
        """
        Extracts entities from the user's natural language input, taking into account
        any existing draft state to contextualize the extraction.
        """
        if current_draft is None:
            current_draft = {}
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        enhanced_input = f"[System Note: Today's date is {current_date}] {user_input}"
            
        result = await self.chain.ainvoke({
            "draft": str(current_draft),
            "input": enhanced_input
        })
        
        return result

# ---
# Explanation:
# The `extractor.py` service wraps the Groq LLM invocation. It uses LangChain's 
# `with_structured_output` paired with the `EXTRACTION_SYSTEM_PROMPT` to reliably parse 
# unstructured chat text into our Pydantic schema (`EnhancedExtractionResult`), preventing 
# hallucinations and tracking uncertain fields explicitly.
