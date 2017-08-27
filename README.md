# annoy_Trump
Sends Donald Trump a tweet every hour telling him to delete his account and what we really think of him.

# Setup
To setup this script, you'll need to allow the Python script to post tweets automatically from your computer. Follow the steps below:

For this script to work, a user must go to Twitter.com, log in and following the below steps:
  * Navigate your browser to apps.twitter.com
  * Click the 'Create New App' button
  * Fill out the details and agree to the developer agreement.
  * Go to the Keys and Access Tokens tab.
  * Copy the Consumer Key and Consumer Secret into the constants below.
  * At the bottom of the browser window, create access tokens. Copy the Access token and Access Token Secret into the constants below too.
  * Run the script in your favorite IDE or from the command line with ```python -m annoy_trump.main``` You'll need 
    the dependent library TwitterAPI in order to run it. Install TwitterAPI with the command ```pip install TwitterAPI```
