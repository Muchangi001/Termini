#!/usr/bin/env python3

import subprocess
import requests
import datetime
import os
import sys

# Configurable paths
LOG_FOLDER_PATH = os.getenv("TERMINI_LOG_PATH", os.path.expanduser("~/Termini/log"))
MD_LOG_FILE_PATH = f"{LOG_FOLDER_PATH}/Termini_log.md"

def get_timestamp() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d        %H:%M:%S")

def fetch_ai_response(prompt, apikey):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={apikey}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url=url, headers=headers, json=payload)
    return response

def parse_response(response, prompt):
    if response.status_code == 200:
        response_data = response.json()
        candidates = response_data.get("candidates", [])
        if candidates and "content" in candidates[0]:
            if "your name" in prompt.lower() or "who are you" in prompt.lower():
                return "**My name is Termini, an AI assistant chatbot that runs in the terminal 😊.**"
            return candidates[0]["content"].get("parts", [{}])[0].get("text", "**Sorry! I can't answer that.**<br>")
    return f"An unexpected error occurred -> {response.status_code}: {response.reason}"

def get_response():
    apikey = os.getenv("GEMINI_API_KEY") # Replace with your actual apikey
    if not apikey:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    prompt = ""
    while prompt.lower() != "bye":
        try:
            prompt = input("\nPrompt  : ")
            if prompt.lower() == "bye":
                print("Termini ↓")
                subprocess.run(["glow"], input="**Byeee!!! Have a good time 😊.**<br>", text=True)
                break

            response = fetch_ai_response(prompt, apikey)
            md_output = parse_response(response, prompt)
            print(f"Termini ↓")
            subprocess.run(["glow"], input=md_output, text=True)
            write_logs(f"**Timestamp **: {get_timestamp()}<br>\n **Prompt  **: {prompt}<br>\n **Termini **↓<br>\n {md_output}<br><br>\n\n---\n\n")
            print(f"Log updated at {MD_LOG_FILE_PATH}")
        except Exception as e:
            print(f"An error occurred: {e}")

def check_log_file():
    if not os.path.exists(LOG_FOLDER_PATH):
        print(f"Creating log folder at {LOG_FOLDER_PATH}")
        os.makedirs(LOG_FOLDER_PATH)
    if not os.path.exists(MD_LOG_FILE_PATH):
        open(MD_LOG_FILE_PATH, "a").close()

def write_logs(data):
    # Read the old log data
    with open(MD_LOG_FILE_PATH, "r") as old_log_file:
        old_data = old_log_file.readlines()

    # Prepend the new log entry to the file
    with open(MD_LOG_FILE_PATH, mode="w") as log_file:
        log_file.write(data)  # Write new data first
        log_file.writelines(old_data)  # Append old data after new entry

def main():
    check_log_file()
    get_response()

if __name__ == "__main__":
    main()
