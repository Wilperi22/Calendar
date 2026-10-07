# Calendar payroll estimate

This is an ongoing project for estimating my girlfriend's monthly pay from her work shifts.

The application:

1. Pulls shift data from the Google Calendar API.
2. Transforms and cleans the data with pandas.
3. Calculates an estimated monthly wage, including applicable additions.
4. Uploads the shifts and wage estimate to a PostgreSQL database running in Docker.

## Setup

1. Create a `.env` file based on `env_example`.
2. Make sure the Google Calendar OAuth files, `credentials.json` and `token.json`, are available.
3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start PostgreSQL:

   ```bash
   docker compose up -d
   ```

5. Run the application:

   ```bash
   python main.py
   ```

The result is an estimate for personal use, not an official payroll calculation. Keep `.env`, `credentials.json`, and `token.json` private.
