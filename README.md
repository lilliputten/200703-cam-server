# Cam flask photo receiver server, raspberry camera client

TODO: Some minimal manual required (see some info in `.projectroot`)

## React app

The project was bootstrapped with:

- [Create React App](https://github.com/facebookincubator/create-react-app),
- [Adding TypeScript](https://create-react-app.dev/docs/adding-typescript/),
- [React App Rewired](https://github.com/timarney/react-app-rewired);

## Server

Images server runs on python/flask platform. It has 3 interfaces: template-based bootstrap application, api interface (json), react spa application (overt api; in progress).

## Camera interface

Camera shots are taken using the `raspistill` program using commands like:

```shell
# Default:
raspistill -o image.jpg
# Half:
raspistill -w 1296 -h 972 -o image-half.jpg
# Half:
raspistill -w 648 -h 486 -o image-quarter.jpg
```

For commandline reference use `raspistill --help`.

- [Camera configuration - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/configuration/camera.md)


## Raspberry camera client

Use `client-make-and-upload-image.sh` script to make & upload image to server.

Use crontab to automate image capture.

### Sample crontab lines:

- Every minute: `* * * * * /home/pi/cam-client/client-make-and-upload-image.sh`
- Every 5th minute: `*/5 * * * * /home/pi/cam-client/client-make-and-upload-image.sh`

### Crontab commands:

Edit crontab:
```shell
crontab -e
```

Show crontab:
```shell
crontab -l
```

See also:

- [Scheduling tasks with Cron - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/linux/usage/cron.md)

## Crontab logging

Uncomment `# cron.*` line in `/etc/rsyslog.conf` (eg. edit with `sudo vim /etc/rsyslog.conf`).

Show crontab log:

```shell
tail -f /var/log/cron.log
```

Or use output reirect in command:

```shell
/home/pi/cam-client/client-make-and-upload-image.sh >> /home/pi/cam-client/cron.log 2>&1
python /home/pi/cam-client/client-make-image.py >>  /home/pi/cam-client/cron.log 2>&1
```


<!--
 @changed 2020.10.18, 20:24
-->
