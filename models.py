import os
from pathlib import Path
from openai import OpenAI

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import mixer


class GPT:
    def __init__(self, model="gpt-3.5-turbo", use_memory=False):
        self.model = model
        self.client = OpenAI()
        self.use_memory = use_memory
        self.memory = []

    def call(self, *args, **kwargs):
        messages = self.build_messages(*args, **kwargs)
        messages = self.memory + messages
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        if self.use_memory:
            self.memory = messages + {"role": "assistant", "content": response}
        return response.choices[0].message.content

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def build_messages(self, *args, **kwargs):
        messages = [{"role": "user", "content": [{"type": "text", "text": args[0]}]}]
        return messages


class GPTVision(GPT):
    def __init__(self, use_memory=False):
        super().__init__(use_memory=use_memory)
        self.model = "gpt-4-vision-preview"

    def build_messages(self, *args, **kwargs):
        base64_image = kwargs["base64_image"]
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": args[0]},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ]
        return messages


class TTS:
    def __init__(self, model="tts-1", voice="fable"):
        self.model = model
        self.voice = voice
        self.client = OpenAI()

    def call(self, prompt):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = self.client.audio.speech.create(
            model=self.model, voice=self.voice, input=prompt
        )
        response.stream_to_file(speech_file_path)
        mixer.init()
        mixer.music.load(speech_file_path)
        mixer.music.play()
        os.remove(speech_file_path)

    def __call__(self, prompt):
        self.call(prompt)
