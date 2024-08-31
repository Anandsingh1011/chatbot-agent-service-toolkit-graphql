# 🧰 chatbot service graphql API call AI Agent



## Overview

### Quickstart

Run directly in python

```sh
echo 'OPENAI_API_KEY=your_openai_api_key' >> .env
pip install -r requirements.txt
python run_service.py

# In another shell
streamlit run streamlit_app.py
```

Run with docker

```sh
echo 'OPENAI_API_KEY=your_openai_api_key' >> .env
docker compose watch
```

### Architecture Diagram



### Key Features

1. **LangGraph Agent**: A customizable agent built using the LangGraph framework.
2. **FastAPI Service**: Serves the agent with both streaming and non-streaming endpoints.
3. **Advanced Streaming**: A novel approach to support both token-based and message-based streaming.
4. **Streamlit Interface**: Provides a user-friendly chat interface for interacting with the agent.
5. **Asynchronous Design**: Utilizes async/await for efficient handling of concurrent requests.
6. **(WIP) Content Moderation**: Implements LlamaGuard for content moderation.
7. **Feedback Mechanism**: Includes a star-based feedback system integrated with LangSmith.
8. **Docker Support**: Includes Dockerfiles and a docker compose file for easy development and deployment.

### Key Files

The repository is structured as follows:

- `agent/agent.py`: Defines the LangGraph agent
- `schema/__init__.py`: Defines the service schema
- `service/service.py`: FastAPI service to serve the agent
- `client/__init__.py`: Client to interact with the agent service
- `streamlit_app.py`: Streamlit app providing a chat interface


## Setup and Usage

1. Clone the repository:
   ```
   git clone https://github.com/Anandsingh1011/chatbot-agent-service-toolkit-graphql.git
   cd agent-service-toolkit
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key

   # Optional, to enable simple header-based auth on the service
   AUTH_SECRET=any_string_you_choose
   
   # Optional, to enable LangSmith tracing
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   LANGCHAIN_API_KEY=your_langchain_api_key
   LANGCHAIN_PROJECT=your_project
   ```

3. You can now run the agent service and the Streamlit app locally, either with Docker or just using Python. The Docker setup is recommended for simpler environment setup and immediate reloading of the services when you make changes to your code.

### Docker Setup

This project includes a Docker setup for easy development and deployment. The `compose.yaml` file defines two services: `agent_service` and `streamlit_app`. The `Dockerfile` for each is in their respective directories.

For local development, we recommend using [docker compose watch](https://docs.docker.com/compose/file-watch/). This feature allows for a smoother development experience by automatically updating your containers when changes are detected in your source code.

1. Make sure you have Docker and Docker Compose (>=[2.23.0](https://docs.docker.com/compose/release-notes/#2230)) installed on your system.

2. Build and launch the services in watch mode:
   ```
   docker compose watch
   ```

3. The services will now automatically update when you make changes to your code:
   - Changes in the relevant python files and directories will trigger updates for the relevantservices.
   - NOTE: If you make changes to the `requirements.txt` file, you will need to rebuild the services by running `docker compose up --build`.

4. Access the Streamlit app by navigating to `http://localhost:8501` in your web browser.

5. The agent service API will be available at `http://localhost:80`. You can also use the OpenAPI docs at `http://localhost:80/redoc`.

6. Use `docker compose down` to stop the services.

This setup allows you to develop and test your changes in real-time without manually restarting the services.

### Local development without Docker

You can also run the agent service and the Streamlit app locally without Docker, just using a Python virtual environment.

1. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```
   python run_service.py
   ```

3. In a separate terminal, run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

4. Open your browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).



### Running Tests

Currently the tests need to be run using the local development without Docker setup. To run the tests for the agent service:

1. Ensure you're in the project root directory and have activated your virtual environment.

2. Install the test dependencies:
   ```
   pip install -r test-requirements.txt
   ```

3. Run the tests using pytest:
   ```
   pytest
   ```

## Customization

To customize the agent for your own use case:

1. Modify the `agent/research_assistant.py` file to change the agent's behavior and tools. Or, build a new agent from scratch.
2. Adjust the Streamlit interface in `streamlit_app.py` to match your agent's capabilities.

## Building other apps on the AgentClient

The repo includes a generic `client.AgentClient` that can be used to interact with the agent service. This client is designed to be flexible and can be used to build other apps on top of the agent. It supports both synchronous and asynchronous invocations, and streaming and non-streaming requests.

See the `run_client.py` file for full examples of how to use the `AgentClient`. A quick example:

```python
from client import AgentClient
client = AgentClient()

response = client.invoke("Tell me a brief joke?")
response.pretty_print()
# ================================== Ai Message ==================================
#
# A man walked into a library and asked the librarian, "Do you have any books on Pavlov's dogs and Schrödinger's cat?"
# The librarian replied, "It rings a bell, but I'm not sure if it's here or not."

```


## License

This project is licensed under the MIT License - see the LICENSE file for details.
