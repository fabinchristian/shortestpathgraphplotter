FROM python
ENV PYTHONUNBUFFERED 1
RUN pip install Flask werkzeug matplotlib
RUN mkdir shortestpathgraphplotter
COPY . /shortestpathgraphplotter/
COPY flask_file.py flask_file.py
COPY static /static/
COPY templates /templates/
CMD python flask_file.py
EXPOSE 5000
