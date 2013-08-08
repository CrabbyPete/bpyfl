bpyfl
=====

Because you are a web developer, people often ask me to develop a website for them, and of course they don't want to pay 
for it. Our local football league asked me to develop a web site. I don't mind doing it, but I hate having to maintain it.
So I create this web site, that uses no database. It runs on Google App Engine, and uses email and Google docs to keep it up
to date. 

Because you have to upload everything to AppEngine, I have included all the necessary libraries. It uses Django as the framework.
To update the news feed, users simple send an email. To update scores and schedules, coaches update a spreadsheet on Google Docs
It works great, and I don't have to keep maintaining it
