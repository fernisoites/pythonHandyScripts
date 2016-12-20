import gmail
username, password = "whudai", "!Dch199939112"

g = gmail.login(username, password)
print g.logged_in
emails = g.inbox().mail()

for email in emails:
	try:
		email.fetch()
		if not email.attachments: continue
		name, size = "", 0
		for attachment in email.attachments:
			name += str(attachment.name)
			size += attachment.size/1000
		if size < 1: continue
		print "{}, att: {}, size: {}".format(email.subject, name, size)
	except:
		continue

g.logout()
