from pathlib import Path
# audiopath = "audiofiles/splits"
# dataset_name = "test-dataset"
import os
import subprocess
import soundfile as sf
import pyloudnorm as pyln
import sys
import glob
import tempfile
import argparse

rnn = "tools/rnnoise/examples/rnnoise_demo"


def remove_noise(source, destination):
    paths = glob.glob(os.path.join(source, '*.wav'))

    tempdir = tempfile.TemporaryDirectory()

    for filepath in paths:
        base = os.path.basename(filepath)
        tp_s = destination + "/" + "wavs" + "/"
        tf_s = destination + "/" + "wavs" + "/" + base
        target_path = Path(tp_s)
        target_file = Path(tf_s)
        print("From: " + str(filepath))
        print("To: " + str(target_file))

        subprocess.run(
            ["sox", "-G", "-v", "0.95", filepath, os.path.join(tempdir.name, "48k.wav"), "remix", "-", "rate", "48000"])
        subprocess.run(["sox", os.path.join(tempdir.name, "48k.wav"), "-c", "1", "-r", "48000", "-b", "16",
                        "-e", "signed-integer", "-t", "raw",
                        os.path.join(tempdir.name, "temp.raw")])  # convert wav to raw
        subprocess.run(
            [rnn, os.path.join(tempdir.name, "temp.raw"), os.path.join(tempdir.name, "rnn.raw")])  # apply rnnoise
        subprocess.run(["sox", "-G", "-v", "0.95", "-r", "48k", "-b", "16",
                        "-e", "signed-integer", os.path.join(tempdir.name, "rnn.raw"), "-t", "wav",
                        os.path.join(tempdir.name, "rnn.wav")])  # convert raw back to wav

        subprocess.run(["mkdir", "-p", str(target_path)])
        subprocess.run(["sox", os.path.join(tempdir.name, "rnn.wav"), str(target_file), "remix", "-", "highpass",
                        "100", "lowpass", "7000", "rate",
                        "22050"])  # apply high/low pass filter and change sr to 22050Hz
        data, rate = sf.read(target_file)

        # peak normalize audio to -1 dB
        peak_normalized_audio = pyln.normalize.peak(data, -1.0)

        # measure the loudness first
        meter = pyln.Meter(rate)  # create BS.1770 meter
        loudness = meter.integrated_loudness(data)

        # loudness normalize audio to -25 dB LUFS
        loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -25.0)
        sf.write(target_file, data=loudness_normalized_audio, samplerate=22050)
        print("")

    tempdir.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Denoiser',
        description='Denoises given sound samples using rnnoise, then places in <destination>'
    )
    parser.add_argument('-s', '--source', action='store', dest='source',
                        default='audiofiles/splits', help='Path to source samples. Default: audiofiles/splits.')
    parser.add_argument('-d', '--destination', action='store', dest='destination',
                        default='audiofiles/datasets/dataset', help='Destination dataset name. Default: dataset.')

    result = parser.parse_args()

    remove_noise(result.source, result.destination)
