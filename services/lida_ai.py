import base64
from lida import Manager, TextGenerationConfig , llm 
from io import BytesIO
from PIL import Image


class LidaAi:
    
    def __init__(self, df):
        self.library = "seaborn"
        self.df = df
        self.manager = Manager(text_gen = llm("openai"))
        self.textgen_config = TextGenerationConfig(n=1, temperature=0.3, model="gpt-4-turbo", use_cache=True)

    def run(self):
        print("inside run")
        summary = self.get_summary()
        print("summary")
        goals = self.set_goals(5, summary)
        print("goals")
        goals_converted = self.convert_goals(goals)
        print("goals_converted")
        # charts = self.get_charts(summary, goals)
        print("charts")
        # images = self.convert_charts(charts)
        return {
            "summary": summary,
            "goals": goals_converted,
            # "images": images
        }

    def get_summary(self):
        summary = self.manager.summarize(self.df, summary_method="default", textgen_config=self.textgen_config)
        return summary
    
    def set_goals(self, n, summary):
        goals = self.manager.goals(summary, n=n, textgen_config=self.textgen_config)
        return goals
    
    def get_charts(self, summary, goals):
        liste = []
        for goal in goals:
            chart = self.manager.visualize(summary=summary, goal=goal, textgen_config=self.textgen_config, library=self.library)[0]
            liste.append(chart)
        return liste
    
    def convert_charts(self, charts):
        liste = []
        for chart in charts:
            img = self.base64_to_image(chart.raster)
            liste.append(img)
        return liste

    def base64_to_image(base64_string):
        # Decode the base64 string
        byte_data = base64.b64decode(base64_string)
        # Use BytesIO to convert the byte data to image
        return Image.open(BytesIO(byte_data))
    
    def convert_goals(self, goals):
        liste = []
        for goal in goals:
            data = {
                "question": goal.question,
                "visualization": goal.visualization,
                "rationale": goal.rationale,
            }
            liste.append(data)
        return liste