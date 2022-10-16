
def email_alert(subject, body, to):
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = 'nir.pysend@gmail.com'
    
    user = 'nir.pysend@gmail.com'
    password = 'ryuuxiuiwoqxhqrj'

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()
    server.login(user, password)

    server.send_message(msg)
    server.quit()