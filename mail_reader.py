import re

import gmail as gmail_module
from flask import render_template

import analysis
import email_config
import data
import deck_reader
import deck as deck_module

base_subject = "Deck analysis"

def read_mail():
# get all cards for reference
# read deck
# analyze deck
# return analysis information
    all_cards = deck_reader.get_all_cards()
    full_card_map = deck_reader.get_card_map_of_all_cards()
    full_card_map_lower = deck_reader.get_card_map_of_all_cards(lower=True)

    gmail = gmail_module.login(email_config.email, email_config.password)
    unread = gmail.inbox().mail(unread=True, prefetch=True)
    print len(unread), "new messages"
    for email in unread:
        match = re.search(r"<([A-Za-z0-9_!@#$%^&*.]+)>", email.fr)
        if match and match.group(1) not in email_config.valid_senders:
            print "Sender:", match.group(1)
            print "Not a valid sender. Skipping."
            continue
        if base_subject in email.subject:
            print "Found an analysis email. Skipping."
            continue

        if 'deck' not in email.subject.lower() or 'netrunner' not in email.subject.lower():
            print "No word 'deck' in subject line. Skipping."
            continue
        deck_data = email.body
        print deck_data
        deck = deck_module.Deck.build_deck_from_text(deck_data, full_card_map_lower)
        if not deck:
            "Deck is empty. Skipping."
            continue
        if not deck.cards:
            print "Deck has no cards. Skipping."
            continue



        #flaws = deck_reader.find_flaws(deck, full_card_map)
        flaws = []

        print '&'*20
        print deck
        print '&'*20
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
        msg['Subject'] = "{} - {}".format(base_subject, email.subject)
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
        email.read()

        #print html

read_mail()
