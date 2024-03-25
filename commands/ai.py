from commands.base import Command
from models import GPT, GPTVision, TTS
import os
import base64


class VisionCommand(Command):
    def init(self):
        self.name = "vision"
        self.model = GPTVision()
        self.screenshots_folder = "/Users/joey/screenshots"

    def _execute(self, *args):
        if len(args) > 1:
            filepath = args[1]
            self.prompt_with_image(prompt, filepath)
        else:
            # defaults to screenshot listener if no files given
            initial_screenshots = self.get_screenshots()
            try:
                print("Listening for new screenshots. Press ctrl-C to stop listening.")
                while True:
                    current_screenshots = self.get_screenshots()
                    new_screenshots = [
                        f for f in current_screenshots if f not in initial_screenshots
                    ]
                    if len(new_screenshots) > 0:
                        last_screenshot = new_screenshots[-1]
                        user_input = input(
                            f"New screenshot detected: {last_screenshot}! Prompt GPT4? (y/n): "
                        ).strip()
                        if user_input == "y" or user_input == "yes":
                            prompt = input(f"Prompt: ").strip()
                            self.prompt_with_image(prompt, last_screenshot)
                        initial_screenshots = current_screenshots
            except KeyboardInterrupt:
                print("No longer listening for screenshots.")

    # Get the list of absolute file paths in the screenshots directory
    def get_screenshots(self):
        return [
            os.path.join(self.screenshots_folder, f)
            for f in os.listdir(self.screenshots_folder)
            if os.path.isfile(os.path.join(self.screenshots_folder, f))
            and not os.path.basename(f).startswith(".")
        ]

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def prompt_with_image(self, prompt, image_path):
        base64_image = self.encode_image(image_path)
        response = self.model(prompt, base64_image=base64_image)
        self.logger(response)


class GPTCommand(Command):
    def init(self):
        self.name = "gpt"
        self.min_args = 1
        self.model = GPT()

    def _execute(self, *args):
        prompt = " ".join(args[1:])
        response = self.model(prompt)
        self.logger(response)


class TTSCommand(Command):
    def init(self):
        self.name = "tts"
        self.min_args = 1
        self.model = TTS()

    def _execute(self, *args):
        prompt = " ".join(args[1:])
        self.model(prompt)
