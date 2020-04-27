** Settings *** 
Library  Selenium2Library 

*** Variables *** 
${browser}  chrome 
${url}  http://127.0.0.1:8000/
${Delay}  5 

*** Keywords *** 
Open Browser for Test Website
	Open Browser  ${url}  ${browser} 
	Set Selenium Speed  ${Delay} 

*** Test Cases *** 
1. Open Website Ope.
	Open Browser for Test Website

2.Enter inputs
	Input Text  id=id_username  shasha
	Input Text  id=id_password  shashank

3.Click login
	Click Element  name=login


7.Click on polls
	Click Link  id=id_polls

8.View Reports/Results
	Click Link 	id=id_result

9.Back to homepage
	Click Link  id=home

4.Click on edit profile
	Click Link  //a[contains(text(),'Edit Profile')]

5.Edit Profile
	Input Text  id=id_first_name  beem
	Input Text  id=id_last_name  sinha
	Choose File  id=id_image  C://Users/malli/OneDrive/Desktop/d.jpg 
	Input Text  id=id_contact  007

6.Click Update
	Click Element  id=updateon

10.Close browser
	Close Browser
	