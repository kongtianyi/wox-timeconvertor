# wox-timeconvertor
An wox plugin that do time convert, including i18n features.

You can just download it use wpm.
```
wpm install Time Convertor
```

## Input Format
```
ts (now|<timestamp>|<datetime>[#<timezone>]) [<timezone>]...
# timestamp support second and milisecond
# datetime's format is yyyy-MM-dd hh:mm:ss
# timezone's format is utc[\+|\-][0-9]+(utc, utc8, utc-12 etc.)
```

## Examples
### Basic Features
1. get timestamp and local datetime for now
 ![image](https://user-images.githubusercontent.com/15275771/206887026-e313ff5b-025b-4d1a-984e-9ff91b0b3d8b.png)
2. convert timestamp to local datetime
 ![image](https://user-images.githubusercontent.com/15275771/206887042-3aff9e7c-5ec4-4d3a-8ff1-1f06f71f941e.png)
3. convert local datetime to timestamp
 
### I18N Features
1. get timestamp certain timezones' datetime for now
 ![image](https://user-images.githubusercontent.com/15275771/206887081-1977d264-4102-47ff-b5de-e96b3cfc3a2a.png)
2. convert timestamp to certain timezones' datetime 
 ![image](https://user-images.githubusercontent.com/15275771/206887095-4a851704-8b40-4cd4-813a-ea455937c592.png)
3. convert local timezone datetime to other timezones' datetime
 
4. convert certain timezone datetime to timestamp
 
5. convert certain timezone datetime to other timezones' datetime
 

## Appendix

* mac version: https://github.com/kongtianyi/alfred-timeconvertor