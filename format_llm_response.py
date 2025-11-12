import re 
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_llm_response(llm_response: str, strict: bool = True) -> dict:
    """
    Parse an LLM response into a Python dict with robust error handling.
    
    Uses multiple strategies:
    1. Direct JSON parsing
    2. Markdown fence removal + JSON extraction
    3. Aggressive cleaning (comments, trailing commas, quote fixes)
    4. Character-by-character quote escaping for malformed strings
    
    Parameters:
        llm_response (str): Raw text from the LLM
        strict (bool): If True, raises exception on parse failure.
                       If False, returns fallback dict with raw text & error info.
                       
    Returns:
        dict: Parsed JSON or fallback dict.
    """
    
    def remove_markdown_fences(text: str) -> str:
        """Remove markdown code fences like ```json or ```"""
        text = text.strip()
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        return text.strip()
    
    def extract_json_block(text: str) -> str:
        """Extract JSON object or array from text"""
        # Try object first
        start_obj = text.find("{")
        end_obj = text.rfind("}")
        
        # Try array
        start_arr = text.find("[")
        end_arr = text.rfind("]")
        
        # Prefer object over array if both exist
        if start_obj != -1 and end_obj != -1 and (start_arr == -1 or start_obj < start_arr):
            return text[start_obj:end_obj + 1]
        elif start_arr != -1 and end_arr != -1:
            return text[start_arr:end_arr + 1]
        else:
            raise ValueError("No JSON object or array found in LLM response.")
    
    def fix_unescaped_quotes(text: str) -> str:
        """
        Fix unescaped quotes inside JSON string values.
        This handles cases like: "command": "grep "ERROR""
        """
        result = []
        in_string = False
        escape_next = False
        i = 0
        
        while i < len(text):
            char = text[i]
            
            if escape_next:
                result.append(char)
                escape_next = False
                i += 1
                continue
            
            if char == '\\':
                result.append(char)
                escape_next = True
                i += 1
                continue
            
            if char == '"':
                if not in_string:
                    # Starting a string
                    result.append(char)
                    in_string = True
                else:
                    # Check if this is the closing quote or an inner quote
                    # Look ahead to see if we're at a valid closing position
                    next_chars = text[i+1:i+10].lstrip()
                    
                    # Valid closing quote if followed by: comma, }, ], or end of string
                    if next_chars and next_chars[0] in ',}]' or i == len(text) - 1:
                        result.append(char)
                        in_string = False
                    else:
                        # This is an inner quote, escape it
                        result.append('\\"')
                i += 1
                continue
            
            result.append(char)
            i += 1
        
        return ''.join(result)
    
    def aggressive_clean(text: str) -> str:
        """Apply aggressive cleaning strategies"""
        # Remove single-line comments (// ...)
        text = re.sub(r'//[^\n]*', '', text)
        
        # Remove multi-line comments (/* ... */)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        
        # Remove trailing commas before } or ]
        text = re.sub(r',\s*([}\]])', r'\1', text)
        
        # Convert Python literals to JSON
        text = re.sub(r'\bTrue\b', 'true', text)
        text = re.sub(r'\bFalse\b', 'false', text)
        text = re.sub(r'\bNone\b', 'null', text)
        
        return text
    
    # Strategy 1: Try direct parsing
    try:
        return json.loads(llm_response)
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Remove markdown fences and extract JSON block
    try:
        clean_str = remove_markdown_fences(llm_response)
        clean_str = extract_json_block(clean_str)
        return json.loads(clean_str)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Strategy 3: Apply aggressive cleaning
    try:
        clean_str = remove_markdown_fences(llm_response)
        clean_str = extract_json_block(clean_str)
        clean_str = aggressive_clean(clean_str)
        return json.loads(clean_str)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Strategy 4: Fix unescaped quotes (most aggressive)
    try:
        clean_str = remove_markdown_fences(llm_response)
        clean_str = extract_json_block(clean_str)
        clean_str = aggressive_clean(clean_str)
        clean_str = fix_unescaped_quotes(clean_str)
        return json.loads(clean_str)
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Failed to parse LLM response as JSON after all strategies: {e}")
        
        if strict:
            raise ValueError(
                f"Response could not be parsed as JSON after multiple attempts.\n"
                f"Error: {e}\n"
                f"Cleaned attempt:\n{clean_str if 'clean_str' in locals() else llm_response}"
            )
        else:
            # Fallback: return original text plus error info
            return {
                "raw_text": llm_response,
                "error": str(e),
                "clean_attempt": clean_str if 'clean_str' in locals() else llm_response
            }
        

llm_response = """json
{
  "document_type": "Bank Statement",
  "confidence": 0.9,
  "reasoning": "The document contains a detailed account summary with opening and closing balances, withdrawals, deposits, and transaction details, which are characteristic of a bank statement. The presence of an account number and a transaction table further supports this classification.",
  "key_indicators": [
    "Account Summary",
    "Opening Balance",
    "Withdrawals",
    "Deposits",
    "Closing Balance",
    "Transaction Details"
  ],
  "negative_indicators": [
    "Employee ID",
    "Basic Pay",
    "Gross Salary",
    "Net Pay",
    "Deductions",
    "Bill Number",
    "Units Consumed",
    "Amount Due",
    "Billing Period",
    "Consumer ID",
    "Pay to the order of",
    "amount written in words",
    "signature line"
  ]
}
"""
#response = parse_llm_response(llm_response=llm_response)
#print("Respone After formating", response.get("document_type"))