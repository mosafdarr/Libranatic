import logging
import sys
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

# Create loggers
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)

error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

# Define formatter
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create and configure stream handler for stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Function to get appropriate log file path
def get_log_file_path():
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        # Use /tmp directory in Lambda environment
        return "/tmp/app.log"
    return "app.log"

# Configure handlers based on environment
def setup_handlers():
    # Add stream handler to both loggers
    logger.addHandler(stream_handler)
    error_logger.addHandler(stream_handler)

    # Only add file handler if we can write to the filesystem
    try:
        log_file_path = get_log_file_path()
        rotating_file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=5*1024*1024,
            backupCount=5
        )
        rotating_file_handler.setFormatter(formatter)
        logger.addHandler(rotating_file_handler)
        error_logger.addHandler(rotating_file_handler)
    except Exception as e:
        logger.warning(f"Could not set up file logging: {str(e)}")

    # Only add SMTP handler if not in Lambda environment
    if not os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        try:
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
            error_logger.addHandler(smtp_handler)
        except Exception as e:
            logger.warning(f"Could not set up SMTP logging: {str(e)}")

# Set up the handlers
setup_handlers()

# Set the logging level for the 'bcrypt' library to ERROR
logging.getLogger('bcrypt').setLevel(logging.ERROR)