import subprocess

subprocess.Popen(["python", "recognition/camera_recognition.py", "--name", "chornovola", "--camera", "http://vs7.videoprobki.com.ua/streams/cam673stream_"], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
subprocess.Popen(["python", "recognition/camera_recognition.py", "--name", "sovhos", "--camera", "http://vs6.videoprobki.com.ua/streams/cam189stream_"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)