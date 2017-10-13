from amazon.api import AmazonAPI
from twilio.rest import TwilioRestClient
amazon_in=AmazonAPI("Your Amazon Access Key","Your Amazon Secret Key","your Amazon Associate Tag,"Your Region")
# Region_options= ['US', 'FR', 'CN', 'UK', 'IN', 'CA', 'DE', 'JP', 'IT', 'ES']
product=amazon_in.lookup(ItemId='B00FEQ6TVO')
def message(msg):
    account_sid = "Your Twilio account id"
    auth_token  = "Your Twilio Auth Token"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body=msg,
    to="+999999",    # Replace with your phone number
    from_="+9999999") # Replace with your Twilio number
    print message.sid
def send_email(title,price):
            import smtplib
            gmail_user = "your gmail id"
            gmail_pwd = "your gmail password"
            FROM = 'Sender email id'
            TO = ['Receiver email id'] #must be a list
            SUBJECT = "Price drops"
            TEXT = "Your product is ready for the purchase"
            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp. gmail. com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                server.quit()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"
print product.title
price = product.price_and_currency[0]
print price
expected_price =7000 # Enter your expected price
if price<=expected_price:
    message(product.title)
    send_email(product.title,price)
