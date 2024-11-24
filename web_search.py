import requests
import pandas as pd
import os

SERP_API_KEY = os.getenv("9161637e169904291")

def perform_web_search(data, query_template):
    results = []

    # Ensure the DataFrame has a selected column
    if 'selected_column' not in data or data['selected_column'].empty:
        raise ValueError("No valid column selected in data.")

    # Replace placeholder in template dynamically
    for entity in data['selected_column']:
        try:
            # Replace the placeholder (e.g., {company})
            query = query_template.format(company=entity)
        except KeyError as e:
            raise ValueError(f"Invalid placeholder in query template: {e}")

        try:
            # Perform the web search
            response = requests.get('https://serpapi.com/search', params={
                "q": query,
                "api_key": SERP_API_KEY
            })

            # Check the response status
            if response.status_code == 200:
                search_results = response.json()
                organic_results = search_results.get('organic_results', [])
                if organic_results:
                    for result in organic_results:
                        results.append({
                            "entity": entity,
                            "query": query,
                            "title": result.get('title', ''),
                            "link": result.get('link', ''),
                            "snippet": result.get('snippet', '')
                        })
                else:
                    results.append({
                        "entity": entity,
                        "query": query,
                        "error": "No organic results found"
                    })
            else:
                results.append({
                    "entity": entity,
                    "query": query,
                    "error": f"Failed to retrieve results. Status code: {response.status_code}"
                })
        except requests.exceptions.RequestException as e:
            results.append({
                "entity": entity,
                "query": query,
                "error": f"Request failed: {str(e)}"
            })

    # Return the results as a DataFrame
    return pd.DataFrame(results)