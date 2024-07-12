from pandasai.llm import OpenAI
from pandasai import SmartDataframe


class PandasAiQuestion:

    def __init__(self, df):
        llm = OpenAI(api_token="")
        self.smart_df = SmartDataframe(df, config = {'llm': llm})

    def run(self, query):
        response = self.smart_df.chat(query)
        return response