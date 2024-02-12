FROM python:3.10 
 
ENV PYTHONIOENCODING UTF-8 
ENV TZ=Asia/Bishkek 
 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone 
 
WORKDIR /bot 
 
RUN pip install aiogram requests python-decouple

COPY bot/ . 
 
CMD ["python3", "bot.py"]