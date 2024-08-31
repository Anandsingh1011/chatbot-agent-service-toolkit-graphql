import math
import numexpr
import requests
import re
from langchain_core.tools import tool, BaseTool
from langchain_community.tools import DuckDuckGoSearchResults, ArxivQueryRun
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import Tool

web_search = DuckDuckGoSearchResults(name="WebSearch")

# Kinda busted since it doesn't return links
arxiv_search = ArxivQueryRun(name="ArxivSearch")

def calculator_func(expression: str) -> str:
    """Calculates a math expression using numexpr.
    
    Useful for when you need to answer questions about math using numexpr.
    This tool is only for math questions and nothing else. Only input
    math expressions.

    Args:
        expression (str): A valid numexpr formatted math expression.

    Returns:
        str: The result of the math expression.
    """
    print('Anand')
    
    #print(expression)
    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
        return re.sub(r"^\[|\]$", "", output)
    except Exception as e:
        raise ValueError(
            f'calculator("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )

calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"




def generate_query_parameters(user_question: str) -> str:
    """
    Extracts movie search parameters from a user's question and returns a string containing the query parameters.

    **Input:**
    - `user_question` (str): A natural language question asked by the user about movies. Example: "Find all documentaries released between 2010 and 2015 sorted by release date."

    **Output:**
    - A str that contains the search parameters based on the user's question. The structure of the string is as follows:
        
            "searchMovie": {
                "title": String,
                "year": String,
                "yearStart": String,
                "yearEnd": String,
                "id": String,
                "type": String
            },
            "sortBy": String,
            "subTitle": Boolean,
            "match": [String],
            "size": Int,
            "page": Int
        

    **Usage:**
    This tool is used to generate structured query parameters for a GraphQL API call to fetch movie details. It interprets the user's natural language question and extracts relevant search parameters.

    **Example:**
    Input: "Tell me about the movie 'Inception'."
    Output: 
    
        searchMovie: {
            "title": "Inception"
        }

    
    """
    # Define the prompt template
    prompt_template = f"""
    You are an AI assistant that helps to extract movie search parameters from user queries. Given a user's question about movies, generate a string with the following structure:
    
    
        searchMovie: {{
            title: String,
            year: String,
            yearStart: String,
            yearEnd: String,
            id: String,
            type: String
        }},
        sortBy: String
        
    
    
    Fill in only the relevant fields based on the user's question. Do not add any extra formatting like JSON or quotes around the field names.

    
    ### Example Inputs and Outputs:
    
    **User Input:** "Tell me about the movie 'Inception'."
    **Output:**
    
        searchMovie: {{
            title: "Inception"
        }}
    
    
    **User Input:** "What movies were released between 2010 and 2015?"
    **Output:**
    
        searchMovie: {{
            yearStart: "2010",
            yearEnd: "2015"
        }}
    
    
    **User Input:** "Show me all movies that were banned."
    **Output:**
    
        match: ["BANNED"]
    
    
    Now, process the following user input:
    
    **User Input:** {user_question}
    **Output:**
    """
    #print(prompt_template)
    # Initialize the ChatOpenAI model
    chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, streaming=True)

    # Create a HumanMessage with the prompt
    messages = [HumanMessage(content=prompt_template)]

    # Get the response from the model
    response = chat(messages)

    # Extract the String response
    query_params = response.content.strip()
    print('===================================')
    print(query_params)
    return query_params


generate_movie_query_parameters: BaseTool = tool(calculator_func)
generate_movie_query_parameters.name = "generate_movie_query_parameters"

def call_graphql_api(user_input: str) -> dict:
    """
    Calls a GraphQL API to fetch movie details based on user input.

    **Input:**
    - `user_input` (str): A natural language question about movies. Example: "Tell me about the movie 'Inception'."

    **Output:**
    - A JSON object (dict) containing the details of the movies matching the user's query. The structure of the response will typically include fields like `id`, `plot`, `title`, and `year`.

    **Usage:**
    This tool is used to query a GraphQL API for movie details. It first generates the necessary query parameters using the `generate_query_parameters` tool and then sends a request to the API. The response from the API is returned as a JSON object.

    **Example:**
    Input: "Find all documentaries released between 2010 and 2015 sorted by release date."
    Output: 
    ```json
    {
        "data": {
            "movies": [
                {
                    "id": "1",
                    "title": "Documentary Title",
                    "year": "2012",
                    "plot": "A plot description."
                },
                ...
            ]
        }
    }
    ```
    """

    # Generate query parameters using the generate_query_parameters tool
    search_parameter = generate_query_parameters(user_input) 
    
    # Define the GraphQL endpoint and headers
    url = 'http://localhost:8080/movie/graphql'
    headers = {'Content-Type': 'application/json'}
    
    # Construct the GraphQL query
    query_movie = """
        query {{
            movies({search_parameter}) {{
                id
                plot
                title
                year
            }}
        }}
        """.format(search_parameter=search_parameter)
    
    print(query_movie)
    
    # Send the POST request to the GraphQL API
    response = requests.post(url, json={'query': query_movie}, headers=headers)
    
    # Return the JSON response
    return response.json()




call_graphql_api: BaseTool = tool(call_graphql_api)
call_graphql_api.name = "call_graphql_api"
call_graphql_api.description = "Calls a GraphQL API to fetch movie details based on user input and returns the results in JSON format."