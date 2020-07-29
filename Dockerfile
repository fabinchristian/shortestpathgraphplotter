FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir shortestpathgraphplotter
COPY . /shortestpathgraphplotter/
WORKDIR shortestpathgraphplotter
RUN pip install -r requirement.txt
CMD python flask_file.py
EXPOSE 5000
