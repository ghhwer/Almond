FROM almond/spark-base

USER almond

# Install all stuff
RUN $HOME/miniconda3/bin/conda install jupyterlab py4j
RUN mkdir $HOME/work
RUN $HOME/miniconda3/bin/jupyter-lab --generate-config

COPY ./themes.jupyterlab-settings $HOME/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension/themes.jupyterlab-settings
COPY ./jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
COPY ./start_notebook.sh /start_notebook.sh

#RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/python_custom_libs:${SPARK_HOME}/python"
ENV IN_CONTAINER=yes

EXPOSE 8888 4040

ENV SHELL=/bin/bash 

CMD ["/start_notebook.sh"]