from playsound import playsound

try:
    playsound(r"E:\1.wav", True)
    #playsound(r"E:\1.wav", True)


except Exception as e:
    print(f"An error occurred: {e}")
