import requests
import json
from google import genai
from google.genai import types
from openai import OpenAI
import assemblyai as aai


def extract_command_from_text(textInput):
    
    PROMPT = """
        The received text contains a user request.
        You must extract the command from the text and output it in the following format rules:

        1. If the request says to turn the ESP32 board light (or onboard LED) ON or OFF, return:
        {"action":"flash_on"} → for turning ON
        {"action":"flash_off"} → for turning OFF

        2. If the request says to turn LED 1, 2, or 3 ON or OFF, return:
        {"action":"flash#_on"} → for turning ON
        {"action":"flash#_off"} → for turning OFF
        (Replace # with the LED number.)

        3. If the request says that ALL lights or ALL LEDs should be turned ON, return all of the following actions as plain text lines:
        {"action":"flash_on"}
        {"action":"flash1_on"}
        {"action":"flash2_on"}
        {"action":"flash3_on"}

        If the request says that ALL lights or ALL LEDs should be turned OFF, return all of the following actions as plain text lines:
        {"action":"flash_off"}
        {"action":"flash1_off"}
        {"action":"flash2_off"}
        {"action":"flash3_off"}

        4. If the request specifies MULTIPLE specific LEDs (for example LED 1 and LED 3, or LED 2 and LED 3) to be turned ON or OFF,
        you must return ONLY the corresponding actions for the mentioned LEDs as separate plain text lines.
        Do NOT include LEDs that were not mentioned.

        Examples:
        - Turn on LED 1 and LED 3:
        {"action":"flash1_on"}
        {"action":"flash3_on"}

        - Turn off LED 2 and LED 3:
        {"action":"flash2_off"}
        {"action":"flash3_off"}

        5. If the request is about capturing an image and includes instructions such as brightness, contrast, quality, or using flash:
        Return:
        {"action":"capture","quality":10,"brightness":0,"contrast":0,"flash":"off"}

        Image parameter rules:
        - quality ranges from 10 (highest quality) to 63 (lowest quality)
        - brightness ranges from -2 to 2
        - contrast ranges from -2 to 2
        - flash must be "on" only if explicitly mentioned

        Default values if not mentioned:
        quality = 10
        brightness = 0
        contrast = 0
        flash = off

        Additional instruction:
        The input text may be noisy, broken, or contain strange characters.
        This text comes from Persian voice transcription and may not be perfectly converted.
        You must intelligently interpret and normalize the text, infer the closest possible intended command, and then apply all the rules above.

        Important:
        - Output must be plain text only
        - Do NOT format the output as a JSON code block
        """


    client = OpenAI(
        api_key="API_KEY",
        base_url="https://api.metisai.ir/openai/v1"
    )


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": textInput}
        ],
        max_tokens=1000
    )
    
    return response


def extract_command_from_voice(voiceInput):

    aai.settings.api_key = "API_KEY"

    audio_file = voiceInput

    config = aai.TranscriptionConfig(speech_models=["universal-3-pro", "universal-2"], language_detection=True)

    transcript = aai.Transcriber(config=config).transcribe(audio_file)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    command = extract_command_from_text(transcript.text)
    return command
    
    
def extranct_command_from_picture(imageInput):
    client = genai.Client(
        api_key="API_KEY", http_options={"base_url": "https://api.avalai.ir"}
    )

    prompt = """You are given an image that contains a hand.
        You must decide which command to return based on the number and position of raised fingers:

        1. If ONE finger is raised, return:
        {"action":"flash_on"}

        2. If TWO fingers are raised, return:
        {"action":"flash1_on"}

        3. If THREE fingers are raised, return:
        {"action":"flash2_on"}

        4. If FOUR fingers are raised, return:
        {"action":"flash3_on"}

        5. If ALL fingers are open (open hand), return the following commands as separate plain text lines:
        {"action":"flash_on"}
        {"action":"flash1_on"}
        {"action":"flash2_on"}
        {"action":"flash3_on"}

        6. If the hand is a CLOSED fist, return the following commands as separate plain text lines:
        {"action":"flash_off"}
        {"action":"flash1_off"}
        {"action":"flash2_off"}
        {"action":"flash3_off"}

        Important:
        - Output must be plain text only
        - Do NOT format the output as JSON code blocks
        - Return ONLY the commands listed above, nothing else
        """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
            data=imageInput,
            mime_type='image/jpeg',
            ),
            prompt
        ]
    )
    return response.text