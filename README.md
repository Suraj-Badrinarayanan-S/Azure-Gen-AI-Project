# Azure-Gen-AI-Project

An intelligent FAQ-style assistant powered by Azure OpenAI and Azure AI Search, integrated with Azure Table Storage and a personally curated Q&A dataset.

This project leverages a private knowledge base feature to answer questions using natural language input from users — perfect for internal tools, documentation bots, or Azure course support.

---

# Architecture
<img width="1032" alt="Screenshot 2025-04-12 at 4 13 20 PM" src="https://github.com/user-attachments/assets/d0226af0-5c11-493e-9959-892fc5b151c6" />


### Workflow

1. **User Input (App UX):** Users enter a question through the app interface.
2. **App Server & Orchestrator:** Handles the prompt and routes it through the system.
3. **Azure AI Search:** Queries knowledge sources like Azure Table Storage, SQL, or Cosmos DB to retrieve relevant context.
4. **Azure OpenAI (ChatGPT/GPT):** Combines the prompt and retrieved knowledge to generate a natural, accurate answer.
5. **Response Displayed to User.**

---

## Tech Stack Used

| Component            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Azure AI Foundry**     | Used for building the AI assistant flow with prompt chaining              |
| **Azure OpenAI (ChatGPT)** | Handles natural language understanding and generation                  |
| **Azure AI Search**      | Retrieves relevant knowledge chunks from curated sources                 |
| **Azure Table Storage**  | Stores structured Q&A dataset as entities                                |
| **Python (Azure SDK)**   | Script used for loading and updating Table data from CSV                 |
| **CSV (Dataset)**        | Manually created list of questions and answers for data engineering use |

---

## 📁 Dataset Example

```csv
id,question,answer
id,question,answer
1,What is your background?,Suraj Badrinarayanan S, currently pursuing B.Tech in Artificial Intelligence and Data Science at Shiv Nadar University, Chennai with a CGPA of 7.9.
2,What are your areas of interest?,Cloud Data Engineering, Azure ecosystem, AWS services, DevOps lifecycle, and scalable data solutions.
```
## Output
<img width="984" alt="Screenshot 2025-04-12 at 4 08 06 PM" src="https://github.com/user-attachments/assets/60a2fe63-c15f-4a7b-ab37-00b87fe1c7d1" />

