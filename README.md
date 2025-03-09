### Goals

- Automatic swiping without being shadow banned.
    - Random and reasonable length pauses between swipes.
    - Randomly swipe left/right on users (Approx 50% or so).
- Swiping regularly when I have available likes.
    - Swiping occurring once per day at different hours. Sometimes skipping 1-3 days to avoid bot detection.
- Email or text me when I get a new match.

### Stretch Goals

- Automatic conversation (might be expensive if I use the GPT api haha).
    - Email or text me when a date is set up.
- Machine learning to help increase odds of swiping right on my type 🥺.

### TODO:
- Write better documentation on the what the differences are between the programs.

### IMPORTANT

- You will need to comment out a line in the package: In `utils.py`, you will need to comment out `"recently_active": user["recently_active"],`. Don't worry if you can't find this line yourself, as running the program will cause this error to throw and will link you to the erroneous line that needs to be commented out.

### Usage

This program is intended to be left running for long times autonomously.

To run the scripts autonomously, you can either:
- Use a Cloud-based VM
- Leave it running on your device, or a Raspberry Pi (and etc)

If you are using a Cloud-based VM or plan to close your terminal, you will need to use something like `tmux`, which allows the process to continue in the background.

Usage:

- Start a new `tmux` session:
```
tmux new -s mysession
```
- Detach from the `tmux` session by pressing `Ctrl + B` followed by `D`.
- Reattach to a `tmux` session:
```
tmux attach -t mysession
```
- View active `tmux` sessions:
```
tmux ls
```
- Delete your `tmux` session:
```
tmux kill-session -t my_session
```

### Automatic Email Notification System

You need to create an 'app password', which is a password that can be used for programmatic emailing.
`https://myaccount.google.com/apppasswords`

I would recommend you use a burner email to use to send the emails for better security (eg. even more safety when running the program on cloud services rather than using your personal email). Of course, there is no security risk to having the emails be sent to your personal account.

### Process

I knew I didn't want to use a browser automation tool like selenium if I could avoid it because Tinder is known to have a lot of pop-ups (eg. showing offers for premium) and other distractions which are very difficult to deal with. These are avoided entirely if an API is used. 

Looking for a working API was quite difficult because most of them are outdated, and Tinder keeps changing the API (eg. Using `protobuff` insteam of `json`). 

After finding a working API, it should be smooth sailing.

### Notes from later + Alternative Ideas

Need to make usage like relaunching easier through smoother processes. When the `x-auth-token` expires, this requires the bot to be reset with the 
new `x-auth-token`. Catching an expired `x-auth-token` and relaunching should be smoother. I think fully automating the `x-auth-token` regeneration 
process is a bit difficult though. 

The documentation on Tinder api endpoints (eg. `https://api.gotinder.com/v2/auth/login/facebook`) isn't very good. Theoretically, automated login without SMS should be possible with Facebook because doing it this way is an automated way to retrieve the `x-auth-token`. At the moment it is quite hard due to the little documentation and the endpoints being constantly updated. From what I could gather, the `https://api.gotinder.com/v2/auth/login/facebook` endpoint takes a `token` and `facebook_id`. The `token` is retrieved from a facebook auth endpoint (I am not sure what the endpoint URL should be). The `facebook_id` is retrieved from something like `"https://graph.facebook.com/me?access_token=" + {access_token}` where `access_token` is the same as `token` that was supposed to be retrieved earlier.

I tried to find where the `x-auth-token` is stored in responses. Maybe a way to do it would be to log in via selenium, retrieve the `x-auth-token`, and then just use the APIs from there? It is probably harder than it sounds though.

Potentially could automate re-login using Twilio or some other SMS service. Not sure how well this would work though (eg. are the phone numbers flagged?). Also, these SMS services cost money.
Could be worth a try though, but not that ideal (don't want to accidentally break something and incur fees for no reason lol).

## Testing

To run the tests:

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Run tests with coverage:
```bash
pytest tests/ --cov=.
Could be worth a try though, but not that ideal (don't want to accidentally break something and incur fees for no reason lol).
