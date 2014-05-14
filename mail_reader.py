import re

import gmail as gmail_module
from flask import render_template

import analysis
import email_config
import data
import deck_reader
import deck as deck_module

def read_mail():
# get all cards for reference
# read deck
# analyze deck
# return analysis information
    all_cards = deck_reader.get_all_cards()
    full_card_map = deck_reader.get_card_map_of_all_cards()
    full_card_map_lower = deck_reader.get_card_map_of_all_cards(lower=True)

    gmail = gmail_module.login(email_config.email, email_config.password)
    print gmail.logged_in
    unread = gmail.inbox().mail(unread=True, prefetch=True)
    #print unread
    #print unread[0].body
    print len(unread), "new messages"
    for email in unread:
        print email.fr
        match = re.search(r"<([A-Za-z0-9_!@#$%^&*.]+)>", email.fr)
        print match.group(1)
        if match.group(1) not in email_config.valid_senders:
            print "Not a valid sender. Skipping."
            continue

        deck_data = email.body
        print deck_data
        deck = deck_module.Deck.build_deck_from_text(deck_data, full_card_map_lower)
        print '*'*20
        #print deck
        print '*'*20
        if deck:
            pass
            # email back sender



        #flaws = deck_reader.find_flaws(deck, full_card_map)
        flaws = []

        print '%'*20
        print deck
        print '%'*20
        analysis_blocks = analysis.build_analysis_blocks(deck)

        from jinja2 import Environment, PackageLoader
        env = Environment(loader=PackageLoader('netrunner', 'templates'))
        template = env.get_template('email_stats.html')
        html = template.render(
            deck=deck,
            shuffled_deck=deck.shuffle,
            identity=deck.identity, 
            cards=deck.cards, 
            side=deck.side,
            cat_cards=deck.cat_cards, 
            flaws=flaws,
            analysis=analysis_blocks,
        )

        # return to sender with stats
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Deck analysis - {}".format(email.subject)
        msg['From'] = email_config.email
        msg['To'] = email.fr
        text = "---Deck analysis for submitted deck---"
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email_config.email, email_config.password)
        """
        message = "\r\n".join([
            "From: {}".format(email_config.email),
            "To: {}".format(email.fr),
            "Subject: Deck analysis - {}".format(email.subject),
            "",
            html,
        ])
        """
        server.sendmail(email_config.email, email.fr, msg.as_string())
        server.quit()
        #email.read()

        #print html
        exit()

read_mail()
