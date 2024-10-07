# Batch-Email-Automation

# Expiry Notification System

This project is an automated system for sending email notifications about expiring and expired files. It uses MongoDB to store file information and sends emails at scheduled intervals to notify users about files that are approaching expiration or have already expired.

## Features

- Monthly notifications for files expiring within 30 days
- Weekly notifications for files expiring within 7 days
- Daily notifications for expired files (sent twice a day)
- Logging of all operations and errors

## Requirements

- Python 3.x
- MongoDB
- SMTP server for sending emails

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/dote7ant/Batch-Email-Automation.git
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   MONGO_URI=your_mongodb_connection_string
   DB_NAME=your_database_name
   EMAIL_PASSWORD=your_email_password
   ```

## Usage

Run the main script to start the scheduled tasks:

```
python main.py
```

The script will run continuously, executing the scheduled tasks at the specified times.

## Project Structure

- `main.py`: The main script that sets up and runs the scheduled tasks.
- `mail_logic.py`: Contains the logic for sending emails and generating email content.
- `schema_def.py`: Defines the MongoDB schema for the expiry information.
- `Mongo.py`: Handles the MongoDB connection and operations.
- `run_script.bat`: A batch file to run the script on Windows systems.

## Configuration

You can modify the schedule in `main.py` to change when notifications are sent. The current schedule is:

- Monthly notifications: Every Friday at 08:00
- Weekly notifications: Daily at 08:00
- Expired file notifications: Daily at 08:00 and 16:00

## Logging

Logs are stored in `expiry_notifications.log`. Check this file for information about script execution and any errors that occur.

## Contributing

Please feel free to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
