# matteklubbenfibonacci
Simple static website for a local math club. Live at https://matteklubbenfibonacci.se.

## After reboot
Enter the `mattevenv` environment:

    source mattevenv/bin/activate

Run `gunicorn`:

    gunicorn app:app
