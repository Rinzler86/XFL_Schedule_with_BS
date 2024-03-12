import smtplib as emailM
from ignore_file import GENERATED_PASSWORD, EMAIL, NUMBER

class EmailSystem:
    """sends email using message and games variables passed from main and sends to email or texts based on the addresses
       in send_email_address field(can send to multiple addresses"""
    def __init__(self, message, games):
        self.message = message
        self.games = games

        # test email application login (required for sending emails/texts)
        self.generated_g_password = f"{GENERATED_PASSWORD}"
        self.my_email_gmail = f"{EMAIL}"

        # enter emails as tuple or using cell provider text format (AT&T - @txt.att.net, T-Mobile -  @tmomail.net , Verizon - @vtext.com)
        self.send_email_address = (f"{NUMBER}")

        with emailM.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=self.my_email_gmail, password=self.generated_g_password)
            connection.sendmail(from_addr=self.my_email_gmail,
                                to_addrs=self.send_email_address,
                                msg=f"Subject: {games} XFL Games Today!\n\n{message}")
