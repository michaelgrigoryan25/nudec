import os
from nudenet import NudeDetector
from flask import Flask, request, jsonify, json

# Flask instance
app = Flask(__name__)
# NudeNet instance
detector = NudeDetector()
# Setting the config parameter
app.config["UPLOAD_FOLDER"] = "./upload"

# The main route for analyzing the images/videos
@app.route("/analyze", methods=["POST"])
def AnalyzeImage():
    # Creating a state that will change based on the validity of the images/videos
    valid = True

    # Looping through each field in the request
    for field in request.files:
        # Getting the file
        file = request.files.get(field)
        # Getting the mimetype of the file
        type = file.mimetype.split("/")

        # Checking for type validity
        if type[0] == "video" or type[0] == "image":
            # Creating a path to temporarily save the file
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            # Saving the file
            file.save(path)

            if type[0] == "video":
                # Checking if there are nudes in a video
                is_nude = detector.detect_video(path, mode="fast")
                # If there are
                if is_nude.get("preds") != {}:
                    # Invalidating all the fields
                    valid = False

            elif type[0] == "image":
                # Checking if the image contains any nudes
                is_nude = detector.detect(path, mode="fast")
                # Checking the array of detections
                # If it has detected any stuff
                if len(is_nude) > 0:
                    # Invalidating all the fields
                    valid = False

            # Removing the temporary file
            os.unlink(path)

        # If the file doesn't pass mimetype checks
        else:
            # Pass to the other files
            pass

    return jsonify(valid)

if __name__ == "__main__":
    app.run()
