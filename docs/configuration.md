# Configuration

The app uses a file named .env to store private settings.

## What is a .env file?

A .env file is a simple text file that stores settings for an application. It is useful because you can keep private values such as API keys out of your source code.

## Create your .env file

In the project root, create a file named .env.

Example:

```env
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX=reviews-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
OPENAI_EMBED_MODEL=text-embedding-3-small
OPENAI_MODEL=gpt-4.1-mini
BUSINESS_NAME=Example Restaurant
BUSINESS_LOCATION=Example City
REVIEW_SOURCE=google
```

## Environment variables

| Name | Required | Description |
| --- | --- | --- |
| OPENAI_API_KEY | Yes | Allows the system to call OpenAI models. |
| PINECONE_API_KEY | Yes | Allows the system to connect to Pinecone. |
| PINECONE_INDEX | No | Names the Pinecone index to use. |
| PINECONE_CLOUD | No | Sets the Pinecone cloud provider. |
| PINECONE_REGION | No | Sets the Pinecone region. |
| OPENAI_EMBED_MODEL | No | Chooses the embedding model. |
| OPENAI_MODEL | No | Chooses the chat model. |
| BUSINESS_NAME | No | Used when cleaning and labeling review data. |
| BUSINESS_LOCATION | No | Used when cleaning and labeling review data. |
| REVIEW_SOURCE | No | Used as metadata for the review source. |

## Tips

- Keep your .env file private.
- Do not share your API keys in chat or public code repositories.
- If you change the .env file, restart the app so it can read the updated values.
