from flask import Flask, render_template, Response
from camera import VideoCamera
from collections import defaultdict
from imutils.video import VideoStream
import os
app =  Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def gen(camera):
	(model, face_detector, open_eyes_detector,left_eye_detector,right_eye_detector, video_capture, images) = camera.init()
	data = camera.process_and_encode(images)
	eyes_detected = defaultdict(str)
	while True:
		frame = camera.detect_and_display(model, video_capture, face_detector, open_eyes_detector,left_eye_detector,right_eye_detector, data, eyes_detected)
		#frame = camera.get_frame()
		yield(b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame
			+ b'\r\n\r\n')

@app.route('/video_feed', methods=['POST'])
def video_feed():
	return Response(gen(VideoCamera()),
		mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	#port = int(os.environ.get("PORT", 5000))
	#port = int(os.environ.get("PORT", 33507))
	app.run()
