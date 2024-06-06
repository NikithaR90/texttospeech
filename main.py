import requests
import PyPDF2
import pygame,base64

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def convert_text_to_speech(text,output_file, language='en-US', voice='en-US-Wavenet-D'):
    api_key = 'AIzaSyCY__xwvkuHUWNjMu8jh26PbJ6sb64wMuA'
    url = 'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + api_key
    request_data = {
        "input": {"text": text},
        "voice": {"languageCode": language, "name": voice},
        "audioConfig": {"audioEncoding": "MP3"}
    }
    headers={'Content-Type':'application/json'}
    response = requests.post(url, json=request_data,headers=headers)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            audio_data=response.json()['audioContent'].encode('utf-8')
            f.write(audio_data)
        print(f"Speech saved to {output_file}")
        save_mp3(audio_data,"output1.mp3")
    else:
        print("Failed to convert text to speech. Status code:", response.status_code)


def save_mp3(data, filename):
    # Decode the base64 encoded data
    audio_data = base64.b64decode(data)

    # Write the binary audio data to a file
    with open(filename, 'wb') as audio_file:
        audio_file.write(audio_data)
def play_mp3(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Limit the while loop to 10 ticks per second to save resources

if __name__ == "__main__":
    pdf_file = 'example.pdf'
    output_file = 'output.mp3'

    text = extract_text_from_pdf(pdf_file)
    # text = "Hello, how are you?"
    convert_text_to_speech(text, output_file)
    play_mp3("output1.mp3")
