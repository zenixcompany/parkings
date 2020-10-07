import subprocess


if __name__ == '__main__':
  subprocess.Popen(
    [
      "python3", "recognition/camera_recognition.py",
      "--name", "Chornovola st 93",
      "--camera", "http://vs7.videoprobki.com.ua/streams/cam673stream_"
    ]
  )

  # subprocess.Popen(
  #   [
  #     "python", "recognition/camera_recognition.py",
  #     "--name", "sovhos",
  #     "--camera", "http://vs6.videoprobki.com.ua/streams/cam189stream_"
  #   ],
  #   stdin=subprocess.DEVNULL,
  #   stdout=subprocess.DEVNULL
  # )

  subprocess.Popen(
    ["python3", "bot/main.py"]
  )