import pyaudio
import numpy as np
import pvporcupine

porcupine = pvporcupine.create(
        keyword_paths=["C:/Users/DUBEM/Desktop/New Horizon/Dictionary/AIStudio/dictionary_en_windows_v3_0_0.ppn"],
        access_key="YrtzfYGr5aV7QzkuVNw34IchpvH2O/ldejj3dcPn40T1KtvvDobs4w==",
)

record = pyaudio.PyAudio()
audio_stream = record.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

def wakeword():
    print("listening for wake word ...")
    while True:
        data = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        # data = struct.unpack_from("h" * porcupine.frame_length, data)
        data = np.frombuffer(data, dtype=np.int16)
        # data = np.abs(data)
        # print(data)
        process = porcupine.process(data)

        # print(data[:10])

        # Camera types for esp32
        #   ov2640
        #   ov5640

        if process >= 0:
            return True


def close():
    audio_stream.stop_stream()
    audio_stream.close()
    record.terminate()
    porcupine.delete()
