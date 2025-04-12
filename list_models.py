import google.generativeai as genai

genai.configure(api_key="AIzaSyDQAPO-LgFQNwHz8rKe9WqfwoImw2DtRGk")

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
