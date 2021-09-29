# dropbox-upload

## Dependencies

```
pip3 install dropbox python-dotenv
```

## Installation

```
git clone https://github.com/tomwilson2/dropbox-upload.git
cd dropbox-upload
cp .env.sample .env
```

## Configuration

Create a Dropbox app here: https://www.dropbox.com/developers/apps

Add the app key and secret to `.env`.

Run `python3 dropbox-auth.py`

Add the access token to `.env`.

## Usage

Run `python3 dropbox-upload.py path-to-file`
