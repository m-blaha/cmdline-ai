#!/usr/bin/env python3

import argparse
import json
import os.path
import requests
import sys

KEY_FILE = "~/.openrouter.key"

class AIProcessor:
    def __init__(self):
        self.args = self.parse_args()
        with open(os.path.expanduser(KEY_FILE), 'r') as file:
            self.api_key = file.readline().strip()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Text processing script.")
        parser.add_argument(
            "--model",
            default="google/learnlm-1.5-pro-experimental:free",
            help="Model to use for processing."
        )
        parser.add_argument(
            "--task",
            default="proofread",
            help="Task to perform on the input text."
        )
        parser.add_argument(
            "-o", "--only-result",
            action="store_true",
            help="Print only the processed result, suppressing original input."
        )
        return parser.parse_args()

    def get_answer(self, input_text):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
        }
        response = requests.post(
            url = "https://openrouter.ai/api/v1/completions",
            headers = headers,
            data=json.dumps({
                "model": self.args.model,
                "prompt" : input_text,
            })
        )
        return response.json().get("choices")[0].get("text")

    def read_input(self) -> str:
        return sys.stdin.read()

    def process(self, input_text: str) -> str:
        task_method = getattr(self, f"task_{self.args.task}", None)
        if not callable(task_method):
            sys.stderr.write(f"Error: Unsupported task '{self.args.task}'\n")
            sys.exit(1)
        return task_method(input_text)

    def output(self, original: str, result: str):
        if self.args.only_result:
            print(result)
        else:
            print(original)
            print('-------- AI suggestion ---------')
            print(result.rstrip())
            print('-------- AI suggestion ---------')

    # Task: proofread (default)
    def task_proofread(self, input_text: str) -> str:
        prompt = """Act as a proofreader and review the following text.
Feel free to rephrase sentences or make changes to enhance clarity but maintain the overall tone and style of the original.
Try to keep the changes minimal, avoid excesive refactoring of sentences.
Only print the final corrected version, never add any reasoning to the output.
Here is the text: """
        return self.get_answer(prompt + input_text)

    # Task: translate
    def task_translate(self, input_text: str) -> str:
        prompt = """You are a translator that converts any given input text into English.  First, try to identify the language of the input.
If you are not certain about the language, assume it is Czech.
Translate the text into English as faithfully as possible, preserving the tone (e.g., formal, informal, emotional, sarcastic, etc.).
Do not add explanations or comments—just output the translated English text.
Input: """
        return self.get_answer(prompt + input_text)

    # Task: commit
    def task_commit(self, input_text: str) -> str:
        prompt = """You are an AI assistant that improves commit messages based on the provided diff.
Input:
A text block containing three parts:
1.  A commit message (may be empty).
2.  Comment lines, each starting with '#'.
3.  A diff in the standard diff format.
Task:
Analyze the provided diff to understand the changes made. Enhance the existing commit message with a concise summary of these changes. If the commit message is empty, create a new informative commit message based on the diff. The output should preserve any existing comment lines and the original diff, placing them after the (potentially enhanced or newly created) commit message.
Input: """
        return self.get_answer(prompt + input_text)

    def run(self):
        input_text = self.read_input()
        result = self.process(input_text)
        self.output(input_text, result)

if __name__ == "__main__":
    processor = AIProcessor()
    processor.run()

