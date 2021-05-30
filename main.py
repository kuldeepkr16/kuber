import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import yfinance as yf

logging.basicConfig(level=logging.INFO)
stocks_details = pd.read_csv('my_stocks.csv')
DATE = datetime.now() - timedelta(days=3)
DATE = DATE.strftime("%Y-%m-%d")
sender = os.environ['GMAIL_APP_S_USER']
receiver = os.environ['GMAIL_APP_R_USER']
passcode = os.environ['GMAIL_APP_PASSWORD']


def get_stock_details():
    """
    get stocks details from yahoo finance(yfinance) package
    :return: a list of details dict
    """
    final_list_ = list()
    for i, config in stocks_details.iterrows():
        symbol = config.get('Instrument')
        avg_price = config.get('Avg. cost')
        quantity = config.get('Qty.')
        amount_invested = avg_price * quantity
        logging.info(f"Checking for stock - {symbol}")
        try:
            data = yf.download(f"{symbol}.NS", start=str(DATE))
        except Exception as e:
            logging.exception(e)
            raise e
        sign = '+'
        data = data.tail(1)
        close_price = round(data['Close'][0], 2)
        amount_now = close_price * quantity
        nume = close_price
        deno = avg_price
        if close_price < avg_price:
            sign = '-'
            nume = avg_price
            deno = close_price
        percent_diff = ((nume - deno) / deno) * 100
        percent_diff = round(percent_diff, 2)
        if sign == '-':
            percent_diff *= -1
            profit = 0
            deductions = 0
            final_profit = 0
        else:
            profit = amount_now - amount_invested
            # 15% tax + 1.01% broker charges
            deductions = round((0.1601 * profit), 2)
            final_profit = round((profit - deductions), 2)

        final_list_.append({"stocks": symbol,
                            "Average Price": avg_price,
                            "Current Price": close_price,
                            "Percentage Change": percent_diff,
                            "profit": profit, "deductions": deductions,
                            "final_profit": final_profit})
    return final_list_


def send_mail(html):
    """
    send mail to receiver's emailID
    :param html: final details df to html
    """
    logging.info(f"Sending mail to {receiver}")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your stocks details"
    msg['From'] = sender
    msg['To'] = receiver

    part = MIMEText(html, 'html')
    msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(sender, passcode)
        server.sendmail(sender, receiver, msg.as_string())
        logging.info(f'sent mail to the user {receiver}')


if __name__ == '__main__':
    final_list = get_stock_details()
    df = pd.DataFrame(final_list)
    df.sort_values(by='Percentage Change', inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df.index = df.index + 1
    send_mail(df.to_html())
    logging.info("Success")
