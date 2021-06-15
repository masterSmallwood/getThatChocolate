import os, time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=2000,4000")

print str(datetime.datetime.now())

#check if text file for storing lastest update content exists
if not os.path.isfile('./latestPost.txt'):
	print 'Creating text file for latest post content...'
	open('latestPost.txt', 'a').close()

browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.Chrome()

 # Sign in
browser.get('https://linkedin.com/uas/login')
emailElement = browser.find_element_by_id('username')
emailElement.send_keys('yourEmail.example.com')
passElement = browser.find_element_by_id('password')
passElement.send_keys('yourSuperSecretPassword')
passElement.submit()

print 'Signing in...'
# time.sleep(3)

browser.get("https://www.linkedin.com/company/coconut-software/")

soup = BeautifulSoup(browser.page_source, 'html.parser')

browser.save_screenshot('scrshot.png')

print 'finding feed divs...'
feedDivs = soup.findAll("div", {"class": "feed-shared-update-v2"})
print 'reading description...'
description = feedDivs[0].find("div", {"class": "feed-shared-update-v2__description"})
print 'finding share button...'
shareButtonId = feedDivs[0].find("span", {"class": "share-reshare-button ember-view"}).get("id")
#shareAsPostButtonId = feedDivs[0].find("ul", {"class": "artdeco-list"}).findAll("li")[0].find("artdeco-dropdown-item").get("id")

latestPost = description.get_text().encode('utf-8')

# Check file if its visited already.
with open('latestPost.txt', 'r') as myfile:
  data = myfile.read()

if data == latestPost:
	print "No new posts... so sorry."
	browser.close()

#write the latest post content to text file and click share on the post
else:
	print "New post found!"

	with open('latestPost.txt', "w") as myfile:
		print "Saving post content to file..."
		myfile.write(latestPost)
	print "Sharing new post..."

	# scroll to reshare button and click it
	reshareButton = browser.find_element_by_id(shareButtonId)
	actions = ActionChains(browser)
	actions.move_to_element(reshareButton).perform()
	reshareButton.click()

	# click the stupid 'Share as Post' button
	#shareAsPostButton = browser.find_element_by_id(shareAsPostButtonId)
	#actions = ActionChains(browser)
	#actions.move_to_element(shareAsPostButton).perform()
	#shareAsPostButton.click()

	#scroll to post button and click it
	postButton = browser.find_element_by_class_name('share-actions__primary-action')
	actions = ActionChains(browser)
	actions.move_to_element(postButton).perform()
	postButton.click()

	browser.close()
	print "Get that chocolate :)"
