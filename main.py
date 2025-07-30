import os
import subprocess
import re


def download_youtube_content():
    """
    Since the recent changes in YouTube now it's necessary to use cookies to download videos, so you may need to provide cookies from your browser in some way.
    You can choose to extract cookies from a browser or use a cookies file.
    You still can choose not to use cookies, but in that case, you may not be able to download some videos or playlists.

    Make sure to use cookies from a browser that has access to the content you want to download and is logged in on a YouTube account.
    """
    while True:
        youtube_link = input(
            "Insert a YouTube video or playlist link (or type 'q' to exit): "
        ).strip()

        if youtube_link.lower() == "q":
            break

        # Basic validation of the YouTube link using a regular expression.
        if not re.match(
            r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$", youtube_link
        ):
            print("Invalid link. Please enter a valid YouTube link.")
            continue

        # Cookie options
        cookie_choice = input(
            "Do you want to use cookies? (1: browser, 2: file, 3: do not use): "
        ).strip()
        cookie_arg = []

        if cookie_choice == "1":
            browser_name = (
                input(
                    "Which browser do you want to extract cookies from? (e.g., Chrome, Firefox): "
                )
                .strip()
                .lower()
            )
            if browser_name:
                cookie_arg = ["--cookies-from-browser", browser_name]
                print(f"Using cookies from browser: {browser_name}")
            else:
                print(
                    "Invalid browser name. Continuing without browser cookies."
                )
        elif cookie_choice == "2":
            cookie_file = input(
                "Path to the cookies file (e.g., cookies.txt): "
            ).strip()
            if os.path.exists(cookie_file):
                cookie_arg = ["--cookies", cookie_file]
                print(f"Using cookies from file: {cookie_file}")
            else:
                print("Cookies file not found. Continuing without cookies.")
        elif cookie_choice == "3":
            print("Continuing without cookies.")
        else:
            print("Invalid cookie option. Continuing without cookies.")


        download_dir = "SavedVideos"
        os.makedirs(download_dir, exist_ok=True)

        print(f"Trying to download content to: {download_dir}/")

        try:
            command = [
                "yt-dlp",
                "-o",
                os.path.join(download_dir, "%(title)s.%(ext)s"),
                youtube_link,
                "--ignore-errors",
                "--restrict-filenames",
                "--no-warnings",
                "--progress",
                "--add-metadata",
                "--embed-thumbnail",
                "--yes-playlist",
            ]
            command.extend(cookie_arg)

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            print("\n--- Download started ---")
            # Logging the output of the command in real-time.
            for line in process.stdout:
                print(
                    line, end=""
                )

            process.wait()

            if process.returncode != 0:
                error_output = process.stderr.read()
                print(
                    f"\nError downloading content: The command returned a non-zero exit code ({process.returncode})."
                )
                print(f"yt-dlp error output:\n{error_output}")
            else:
                print("\n--- Download Completed ---")

        except FileNotFoundError:
            print("\nError: 'yt-dlp' not found.")
            print("\nMake sure you have 'yt-dlp' installed and accessible in your PATH variables.")

        except Exception as e:
            print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    download_youtube_content()
