# Additional checks to add to the current tests
    - For title check test case, right now the validation is just to check whether the title exists or not. The test case can be further improved by testing the title relevance and whether it matches with the content.
    - For the grade visibility test case, enhance the test case to check if the grade is below or equal to 5 and read the text under the review (i.e Sehr gut) and assess it.
    - for the 2 start filter test case, enhance the test case to check the count of reviews as well (i.e 2 star has 55 reviews).

# Further possible test cases
    - Check all the links are properly working (such as link on the logo of trustedshops & Jalousiescout, infomation, profile logo etc..)
    - Check if the login works (for private or business customers)
    - Validation of user input fields (such as search boxes)
    - check if all the filter dropdown values are properly navigating to relevant reviews filtering
    - Check if the sorting works (such as newest or relevance)
    - Check if all the positive or critical reviews displayed upon the click on respective links
    - Check if the report review opens the reporting modal dialog page
    - Check if the click on helpful shows the number 1 in green color next to it
    - Check if the link "So stellen wir sicher" is properly navigating to the relevant information.
    - Check if the link "Nach oben" navigates to the top
    - Check the page behavior for all the above testcases on different devices such as tablets or mobiles
    - Check the webpage on different browsers (such as Edge/Firefox etc.)

# Non functional requirements
    - Performance
        - Check the load time of the page on different devices and network conditions by using different tools(JMeter) and assess them if they are not as per requirements.
    - Security
        - Test using certain security attacks and assess.
    - Compatibility
        - Test on different browsers/devices/OperatingSystems and check the page renderings and proper data.
    - Usability
        - Get the feedback from usability experts for the user friendlyness or ease of use and assess.
    - Scalability
        - Use certain load test tools and assess if all the requests get the response and assess the response time with increased number of requests.
