import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def process_with_llm(results):
    output = []

    for result in results:
        # Ensure 'snippet' exists in the result
        snippet = result.get('snippet', 'No snippet available')
        if not snippet:
            print(f"Missing 'snippet' in result: {result}")  # Debugging
            continue  # Skip this result if 'snippet' is missing

        try:
            # Call the LLM API with the snippet
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Extract email from the following text: {snippet}",
                max_tokens=50
            )
            extracted_info = response['choices'][0]['text'].strip()
            output.append({
                "entity": result.get('entity', 'Unknown'),
                "query": result.get('query', ''),
                "extracted_info": extracted_info
            })
        except Exception as e:
            print(f"Error processing with LLM: {e}")
            output.append({
                "entity": result.get('entity', 'Unknown'),
                "query": result.get('query', ''),
                "error": str(e)
            })

    return output
