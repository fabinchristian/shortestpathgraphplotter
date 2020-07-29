FROM python
ENV PYTHONUNBUFFERED 1
RUN pip install Flask werkzeug matplotlib
RUN mkdir shortestpathgraphplotter
COPY . /shortestpathgraphplotter/
WORKDIR shortestpathgraphplotter
CMD python flask_file.py
EXPOSE 5000
