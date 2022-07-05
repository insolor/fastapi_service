FROM python:3.8

RUN useradd -ms /bin/bash user
USER user

WORKDIR /home/user

COPY dist/inside-0.1.0-py3-none-any.whl .

RUN pip install inside-0.1.0-py3-none-any.whl && rm inside-0.1.0-py3-none-any.whl

EXPOSE 10000

ENTRYPOINT [ "python", "-m", "inside" ]
