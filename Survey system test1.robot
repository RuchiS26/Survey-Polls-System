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
	Input Text  id=id_username  st121345
	Input Text  id=id_password  TWg2@NS3

3.Click login
	Click Element  name=login


4.Click on polls
	Click Link  id=id_polls

5.Click on Participate
	Click Link 	 xpath=//a[@class="btn btn-outline-primary" and @id="pollpart"]

6.Select option
	Click Link  xpath=//a[contains(text(),'needed')]
	Click Link  id=home

7.Create survey 
	Click Link  id=create_survey

8.Input details
	Input Text  id=id_title  water supply
	Input Text  id=id_description  shortage of water supply
	Click Element  id=id_next

9.Adding Questions
	Input Text  id=question  Do we need more water tanks to be installed ?
	Select From List By Value  xpath=//select[@id="selType"]  2
	Click Link  id=questionbtn
	Input Text  id=optionsform  Yes
	Click Link  id=optionbtn
	Input Text  id=optionsform  No
	Click Link  id=optionbtn
	Click Link  id=donebtn
	Input Text  id=question  Any other suggestions ?
	Select From List By Value  xpath=//select[@id="selType"]  1
	Click Link  id=preview

10.Publish the survey 
	Click Link  id=id_publish

11.Close survey
	Click Link  id=id_close

12.Discard survey
	Click Link  //a[contains(text(),'Discard')]

13.Create Polls
	Click Link  id=create_polls

14.Input details
	Input Text  id=id_title  gym needs
	Input Text  id=id_question  Do we need new gym equipments ?
	Click Element  id=id_next

15.Add options
	Input Text  id=option  yes
	Click Link  id=option
	Input Text  id=option  no
	Click Link  id=option
	Click Link  id=id_preview
16.Publish survey
	Click Link  id=id_publish


17.Close browser
	Close Browser