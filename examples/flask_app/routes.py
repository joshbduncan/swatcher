import json
import os
import secrets
import swatcher

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from . import app
from .forms import UploadImage, ResampleImage
from io import BytesIO
from PIL import Image


def reset_session_vars():
    """
    resets all image flask session variables
    """

    session.pop("id", None)
    session.pop("filename", None)
    session.pop("image_path", None)
    session.pop("colors", None)
    session.pop("palette", None)
    session["max_colors"] = 8
    session["sensitivity"] = 75


def prepare_pil_image(image: object) -> object:
    """
    Temporarily save a PIL Image object so it can be sent to the client

    :param `image`: PIL Image object
    :returns: temporary file object
    """
    img_io = BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)
    return img_io


@app.route("/", methods=["GET", "POST"])
def index():
    # setup forms objects
    upload_form = UploadImage()
    resample_form = ResampleImage()

    if request.method == "GET":
        reset_session_vars()
        return render_template("upload.html", upload_form=upload_form)

    # if upload_form was submitted
    if upload_form.upload.data:
        if upload_form.validate_on_submit():

            # reset all session vars for new upload
            reset_session_vars()

            # grab the user uploaded image
            submitted_img = upload_form.image.data

            # generate a random id for this image
            random_hex = secrets.token_hex(8)
            # _, f_ext = os.path.splitext(submitted_img.filename)
            filename = random_hex + ".jpg"

            # process the uploaded image
            image = swatcher.Swatcher(submitted_img)

            # save it locally in static folder
            filepath = os.path.join(current_app.root_path, "static/images", filename)
            image.processed_image.save(filepath, "JPEG", quality=100, subsampling=0)
            image_path = url_for("static", filename="images/" + filename)

            # reduce sampled colors to using defaults
            image.max_colors = session.get("max_colors")
            image.sensitivity = session.get("sensitivity")
            colors = image.palette

            # setup each sampled color as a dict for use in jinja template
            # including the RGB values, Hex code, and CMYK values
            colors = swatcher.color.colors_2_dicts(colors)

            # set session values
            session["id"] = random_hex
            session["filename"] = filename
            session["image_path"] = image_path
            session["colors"] = json.dumps(image._colors)
            session["palette"] = json.dumps(colors)

            return render_template(
                "colors.html",
                resample_form=resample_form,
                colors=colors,
            )
        else:
            # if validation error start over
            reset_session_vars()
            flash("Please upload image files only!", "danger")
            return render_template("upload.html", upload_form=upload_form)

    # if resample_form was submitted instead
    elif resample_form.resample.data:
        if resample_form.validate_on_submit():

            # get update sampling values from user and save them
            max_colors = int(resample_form.colors.data)
            sensitivity = int(resample_form.sensitivity.data)

            # get stored image colors and resample them using new settings
            colors = json.loads(session.get("colors"))
            colors = swatcher.palette.sample(
                colors=colors, max_colors=max_colors, sensitivity=sensitivity
            )

            # setup each sampled color as a dict for use in jinja template
            # including the RGB values, Hex code, and CMYK values
            colors = swatcher.color.colors_2_dicts(colors)

            # update session values
            session["max_colors"] = max_colors
            session["sensitivity"] = sensitivity
            session["palette"] = json.dumps(colors)

            return render_template(
                "colors.html",
                resample_form=resample_form,
                colors=colors,
            )

    # if session has expired then start over from scratch
    if "id" not in session:
        reset_session_vars()
        flash("Sorry, your session has expired! Reupload.", "warning")
        return render_template("upload.html", upload_form=upload_form)

    # if any validation errors start over
    reset_session_vars()
    flash("Whoops, something went wrong! Reupload to try again.", "warning")
    return render_template("upload.html", upload_form=upload_form)


@app.route("/palette")
def palette():
    if "id" in session:
        # grab session information
        id = session.get("id")
        colors = [tuple(color["rgb"]) for color in json.loads(session.get("palette"))]
        # create adobe ase swatch file
        file = swatcher.export.write_ase_file(colors)
        # return the file as a download
        return send_file(file, download_name=f"SWATCHER-{id}.ase", as_attachment=True)
    else:
        abort(410)


@app.route("/image")
def image():
    if "id" in session:
        # grab session information
        id = session.get("id")
        # get all RGB vales from the sampled colors
        colors = [tuple(color["rgb"]) for color in json.loads(session.get("palette"))]
        # create swatch palette image
        file = swatcher.palette.draw_swatches(colors)
        # create a temporary file and return it to the user as a download
        return send_file(
            prepare_pil_image(file),
            mimetype="image/jpeg",
            download_name=f"SWATCHER-{id}.png",
            as_attachment=True,
        )
    else:
        abort(410)
