## Chatbot setup
- create a environment
```
conda create -p wp_chatbot python=3.9 -y
```
- in python
```
python -m venv wp_chatbot
```

- activate environment
```
conda activate wp_chatbot/
```
- in python 
```
wp_chatbot\Scripts\activate
```

- install dependencies
```
pip install -r requirements.txt
```

- convert env_file/ in .env file and update the GROQ_API_KEY

- to run the web app
```
flask run
```