FROM python:3.12.2

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y imagemagick ffmpeg \
    && export MAGICK_HOME="$HOME/ImageMagick-7.1.1" \
    && export PATH="$MAGICK_HOME/bin:$PATH" \
    && export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$MAGICK_HOME/lib" \
    && cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g' > /etc/ImageMagick-6/policy.xml

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./audio /code/audio
COPY ./font /code/font
COPY ./image /code/image
COPY ./video /code/video
COPY ./src /code/src

CMD ["python3", "./src/main.py"]
