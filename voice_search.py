import speech_recognition as sr

# sections of this class have been referenced from the week 10
# code samples in the 2019 COSC2674 Programming Internet of Things
# course material
class VoiceSearch:
    def __init__(self):
        # mic_name = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"
        mic_name = "Built-in Microphone"
        # set mic id to avoid ambiguity
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if(microphone_name == mic_name):
                self.device_id = i
                break
    
    def speech_to_text(self):
        # get audio from microphone
        r = sr.Recognizer()
        with sr.Microphone(device_index=self.device_id) as source:
            # adjust for ambient noise for optimal performance
            r.adjust_for_ambient_noise(source)

            print("Say something...")
            try:
                # try get audio
                # stop listening after 2 seconds if no speech detected
                audio = r.listen(source, timeout=2)
            except sr.WaitTimeoutError:
                print("We couldn't hear anything")
                return None

        # send audio to google for processing
        try:
            speech = r.recognize_google(audio)
            print("You said '{}'".format(speech))
            return speech
        except sr.UnknownValueError:
            print("We could not understand you")
            return None
        except sr.RequestError as re:
            print("Something went wrong.")
            print(re)
            return None

if __name__ == "__main__":
    vs = VoiceSearch()
    s = vs.speech_to_text()
    print(s)
