FROM python:3.11-slim
WORKDIR /app
RUN useradd -m defuser
COPY project-audit.py /app/
RUN chown -R defuser:defuser /app
USER defuser
CMD ["python","project-audit.py"]
