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
        if quantity == 0:
            logging.info(f"Skipping 0 qty stocks - {symbol}")
            continue
        logging.info(f"Checking for stock - {symbol}")
        try:
            data = yf.download(f"{symbol}.NS", start=str(DATE))
        except Exception as e:
            logging.exception(e)
            raise e
        data = data.tail(1)
        try:
            close_price = round(data['Close'][0], 2)
        except Exception as e:
            logging.exception("Most probably delisted stock...")
            continue
        amount_now = close_price * quantity
        percent_diff = ((close_price - avg_price) / avg_price) * 100
        percent_diff = round(percent_diff, 2)
        total_profit = amount_now - amount_invested
        if total_profit < 0:
            deductions = 0
            final_profit = 0
            profit_percentage = 0
        else:
            # 15% tax + 1.01% broker charges
            deductions = round((0.1601 * total_profit), 2)
            final_profit = round((total_profit - deductions), 2)
            profit_percentage = round(((final_profit/amount_now) * 100), 2)

        final_list_.append({"Stocks": symbol,
                            "Quantity": quantity,
                            "Avg Price": avg_price,
                            "Current Price": close_price,
                            "% Change": percent_diff,
                            "Total Profit": total_profit, "Deductions": deductions,
                            "Final Profit": final_profit,
                            "Profit %": profit_percentage})
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
    df.sort_values(by='% Change', inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df.index = df.index + 1
    send_mail(df.to_html())
    logging.info("Success")
