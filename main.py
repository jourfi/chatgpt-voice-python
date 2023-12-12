import speech_recognition as sr
from elevenlabs import generate, play
import openai
from elevenlabs import set_api_key
set_api_key("") # Eleven labs api

openai.api_key = "" # Replace this with your API key

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
      
        print("Listening...")
        audio = recognizer.listen(source, timeout=3)  # Adjust timeout as needed

    try:
        user_message = recognizer.recognize_google(audio)
        print(f"USER: {user_message}")
        return user_message
    except sr.UnknownValueError:
        print("ChatGPT: Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Error accessing Google Speech Recognition service: {e}")
        return None

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "Hi ChatGPT, You are a helpful assistant!"},
    ]

    try:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat_completion["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": "Act as ChatGPT: " + reply})

    except Exception as e:
        print(f"Error: {e}")
        exit()

    while True:
        user_input = speech_to_text()
        if user_input is None:
            continue

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "clear":
            print("\033[H\033[J")
            print("ChatGPT: How Can I Help You Today?")
            messages = [{"role": "system", "content": "ChatGPT: How Can I Help You Today?"}]
        else:
            messages.append({"role": "user", "content": user_input})
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat_completion["choices"][0]["message"]["content"]

            audio = generate(
                text=reply,
                voice="Dorothy",
                model="eleven_multilingual_v2"
            )

            print(f"ChatGPT: {reply}")
            play(audio)
            messages.append({"role": "assistant", "content": reply})
