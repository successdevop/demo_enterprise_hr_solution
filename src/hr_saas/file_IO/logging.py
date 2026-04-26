import datetime


class Logger:
    @staticmethod
    def success(message, log_file):
        try:
            with open(log_file, mode="w", encoding="utf-8") as success_writer:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                success_writer.write(f"[{timestamp}]: {message} \n")
        except Exception as e:
            print(f"Error writing to log file {log_file} | {e}")

    @staticmethod
    def error(message, log_file):
        try:
            with open(log_file, mode="w", encoding="utf-8") as success_writer:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                success_writer.write(f"[{timestamp}]: {message} \n")
        except Exception as e:
            print(f"Error writing to log file {log_file} | {e}")

    @staticmethod
    def info(message, log_file):
        try:
            with open(log_file, mode="w", encoding="utf-8") as success_writer:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                success_writer.write(f"[{timestamp}]: {message} \n")
        except Exception as e:
            print(f"Error writing to log file {log_file} | {e}")
