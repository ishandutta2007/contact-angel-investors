# contact-angel-investors

This is a repo which collects mail id of angel investors and VCs from linkedin and automatically mails them the startup pitch.

### To Setup:

On how to setup gmail API follow [this](https://github.com/shankarj67/python-gmail-api/blob/563c7bf722c69be4fed2204e2829d0ab843d8729/README.md#install)

### To crawl email data and augment exsisting set in email-list.csv

1. `python3 linkedin-crawler.py`

2. The above script will append or create email-list.csv with all email details.

### To send email

1. Modify the templates `first_touch_mail.html` or `followup_mail.html` as per need. If you need to rename or recreate new html template feel free to do so, just make sure you update name of it in `send_main.py`(as of now hardcoded)

2. `python3 send_mail.py`

### Support:

If you want the good work to continue please support us on

* [PAYPAL](https://www.paypal.me/ishandutta2007)
* [BITCOIN ADDRESS: 3LZazKXG18Hxa3LLNAeKYZNtLzCxpv1LyD](https://www.coinbase.com/join/5a8e4a045b02c403bc3a9c0c)
