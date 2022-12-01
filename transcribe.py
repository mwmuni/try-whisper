import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "5"
import warnings
warnings.simplefilter("ignore")
# import tensorflow as tf
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import whisper

# Time the function call
# from time import perf_counter

def run_whisper():
    # start = perf_counter()
    model = whisper.load_model("base", device="cuda")
    result = model.transcribe("file.mp3", language="english")
    # end = perf_counter()
    print(result["text"])
    # print(f"Time: {end - start}")

if __name__ == "__main__":
    run_whisper()
