from pathlib import Path

def save_chat_to_txt(chat_history, filename):
  """Saves the chat history string to a .txt file using pathlib.

  Args:
    chat_history: The string containing the chat history.
    filename: The desired name for the .txt file.
  """
  file_path = Path(filename)
  file_path.write_text(chat_history, encoding='utf-8')
