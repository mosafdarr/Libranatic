import logging
import sys
from logging.handlers import RotatingFileHandler, SMTPHandler

# Create a logger for general application logging
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all types of logs

# Create a logger specifically for error logging
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

# Define a common formatter for both loggers
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create and configure stream handler to output logs to stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Create and configure rotating file handler to output logs to a file
rotating_file_handler = RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=5)
rotating_file_handler.setFormatter(formatter)

# Create and configure SMTP handler for sending error logs via email
smtp_handler = SMTPHandler(
    mailhost=("smtp.example.com", 587),
    fromaddr="error-logger@example.com",
    toaddrs=["admin@example.com"],
    subject="Application Error",
    credentials=("user", "password"),
    secure=()
)
smtp_handler.setLevel(logging.ERROR)
smtp_handler.setFormatter(formatter)

# Add handlers to the general application logger
logger.addHandler(stream_handler)
logger.addHandler(rotating_file_handler)

# Add handlers to the error logger
error_logger.addHandler(stream_handler)
error_logger.addHandler(rotating_file_handler)
error_logger.addHandler(smtp_handler)

# Set the logging level for the 'bcrypt' library to ERROR
logging.getLogger('bcrypt').setLevel(logging.ERROR)
