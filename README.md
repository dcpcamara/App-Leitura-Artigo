# Paper summarizer app for busy scientists

Just upload a pdf with the paper that you want to summarize, click the button and wait a few seconds. Since my background is on public health, epidemiology and medical entomology, the AI assistant is programed to be an expert on those areas. It can probably be helpful to work with any health related paper though. Test at your own risk. The AI assistant will do its best to summarize the paper into bullet points with Introduction, Methodology, Results, Discussion, and Conclusion, as well as the most cited references in the paper. You will get a summary with the full abstract at the beginning also. It requires you to have an OpenAI API to run. Costs may apply (fractions of a cent, it’s really inexpensive). Future updates may include open-source models with no embedded costs."

## Configure OpenAI API Key
You need to securely store your OpenAI API key. Log in to your OpenAI account at platform.openai.com and navigate to the API keys section. Follow the instructions to create your API key. When done, update the **credentials.yml** file.

```
openai: 'YOUR_OPENAI_API_KEY'
```