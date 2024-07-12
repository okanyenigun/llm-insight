from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

class PandasAgentDescription:

    PREFIX = """
            You are an expert data analyst with a specialization in banking and financial sectors. You will be given a dataset, and you need to analzye it, understand it, extract insights about it. You will be asked to describe the data, provide insights, and answer questions about the data.

            # AUDIENCE #
            You are talking to a C-LEVEL manager (CEO, CFO) in a bank.

            # TONE #
            Professional, formal, and informative.

            """
    
    DEFAULT_QUESTIONS= {
        "Description": "Given the dataset provided, describe the types of data it contains, the structure of the table, and the key metrics and parameters represented. Explain how the data is organized and any identifiable categories or groupings within the data.",

        "Trends": "For each parameter in the dataset, analyze the trends over the available time periods. Identify whether the trends are increasing, decreasing, or stable. Highlight any notable fluctuations and periodic patterns observed in the data.",
        
        "Relationships": "Examine the relationships between different parameters in the dataset. Identify any correlations or inverse relationships, such as one parameter trending upwards while another trends downwards. Discuss the possible implications of these relationships and what they might indicate about the underlying factors influencing the data.",
        
        "Insights": "Beyond basic descriptions and trend analysis, delve into deeper insights from the data. Identify any anomalies, outliers, or unexpected patterns. Discuss potential causal factors and the broader implications these insights might have on understanding the data’s context or impact.",

        "Forecasts": "Based on the historical data and identified trends, predict future developments for the key parameters in the dataset. Utilize any identified patterns, relationships between parameters, and external factors that might influence future data points. Provide scenarios or forecasts for what the data might look like in the upcoming periods."
    }

    def __init__(self, df, temperature=0.1):
        self.df = df
        self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=temperature, model="gpt-4-turbo-2024-04-09"),
            df,
            verbose=True,
            agent_type="openai-tools",
            prefix=self.PREFIX,
            allow_dangerous_code=True,
            max_iterations=3,
        )

    def get_default_answers(self):
        responses = {}
        for key, value in self.DEFAULT_QUESTIONS.items():
            print(key)
            responses[key] = self.run(value)
        return responses

    def run(self, query):
        response = self.agent.invoke(query)
        return response["output"]