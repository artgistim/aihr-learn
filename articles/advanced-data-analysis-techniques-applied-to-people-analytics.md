---
title: "5 Advanced Data Analysis Techniques Applied to People Analytics"
source: "https://www.aihr.com/blog/advanced-data-analysis-techniques-applied-to-people-analytics/"
author: "Rob van Dijk"
published: "2019-03-11T11:25:13+00:00"
modified: "2023-09-27T09:16:50+00:00"
downloaded_at: "2026-09-11T04:03:44.611487+00:00"
usage: 個人學習；內容版權屬原作者與 AIHR
---

> 原文：https://www.aihr.com/blog/advanced-data-analysis-techniques-applied-to-people-analytics/
> 本地副本僅供個人學習；引用與分享請回到原文並遵守網站條款。
In previous articles, I have given multiple examples of how employees can benefit from data analytics . In this article, I would like to explore a set of different, advanced data analysis techniques to see how they can be used to analyze people data for improved organization success.

Data science is increasingly incorporated in businesses, products, and society at large. The use cases are getting more sophisticated and widespread across sectors (as shown in the figure above).

As a people analytics practitioner, I work with organizations to gain insights into their workforce and design effective strategies to organize for success. While the use cases above are often quite advanced algorithms that use machine learning to continuously improve, the conception of such an algorithm is always one or more data science technique(s). By the way, here’s a clear explanation of the difference between data science, machine learning and –while we’re at it– AI.

Now, while HR data and metrics with basic slicing and dicing have been around for a long time, people analytics cases using advanced statistical techniques are still quite a new phenomenon and only a handful of organizations actually conduct these kinds of analyses on people data. So I thought it might be a good idea to discuss what is already being done and brainstorm together with this community of practitioners and come up with cases for people analytics using common data science techniques.

Let’s get inspired!

## Techniques

### Regression analysis

As one of the most common of statistical analyses available, regression is used to capture the relationship between one or more context variables and an outcome in a function. The goal here is to predict the future progression of the outcome based on values of the context variables.

There is a difference between linear and logistic regression in the way Logistic regression is used when the outcome variable is categorical in nature. Linear regression is used when the outcome variable is continuous. It is important to note that unlike with correlation, in regression there is an assumption of a single-way causal effect from the context variable and the outcome variable.

One common example from marketing is organizations that try to predict customer churn . Churn, or attrition, is a rate at which individuals (customers, employees) leave. The obvious goal is here to prevent them from jumping ship. Another example is dating sites that regularly use regression analysis to improve their service and provide better matches for their members.

### How can it help address business issues with people data?

An example can be found in sales effectivity. It can be very valuable to measure the relationship between scores on personality questionnaires and sales numbers.

In what way are personality traits (like Big-5 traits) linked to sales numbers? Meta-analyses show that extraversion and conscientiousness are predictive of sales success. The question is, are there differences in the markets that sales professionals operate in? Using regression analysis, you can find out if there is a relationship and to what degree personality traits predict sales effectivity for your employees.

Click the link for a more detailed explanation of the regression analysis .

### Classification analysis

Classification is one of the most applied and best-known data science methods. Simply put, in classification, for any new observation (data) we want to predict which category the observation belongs. This is done by analyzing historical observations of which the category is known.

Different models can be used for classification and one of the most well-known is a decision tree. A decision tree is a process where many yes or no questions are answered to determine the category. Using decision trees on a large scale is also known as a random forest technique and this method is often used with large datasets. It is often used in combination with logistic regression to improve the predictive performance of the statistical model in a method called ensemble learning . A bit too technical for now but you can get your additional tech on here .

An example of how classification is used is in healthcare, where historical data of patients are used to analyze symptoms in order to determine (classify) which condition a new patient might have. This is already being used to predict cancer and determine high-risk groups.

Another example is in banking, where the customer who applies for a loan may be classified as safe or risky depending on attributes like age and salary. This type of activity is also called supervised learning because it is based on previous learning and an already trained model . The constructed data model can be used to classify new input data.

### How can it help address organizational challenges with people data?

One great example would be to predict the success rate of a team based on team composition and context variables. As organizations, we tend to select project teams based on experience, availability, and past individual performance. It would be very valuable to shed some light on the impact of other factors such as role preference, leadership style, team dynamics, team size, background, and contextual factors such as assignment duration and budget. This would require a huge dataset in order to train the model. The classification technique would in this case probably be a neural network . Imagine the impact of being able to predict what team composition will have the highest success rate given a specific context!

### Clustering analysis

Clustering is a technique to describe data and to find general patterns. It is used when available data are not –or ambiguously– labeled and works by finding observations that are similar to each other. These observations are then ‘clustered’, so the groups can be labeled and categorized. Clustering, in this regard, is similar to classification; it aims to categorize specific groups of interest but it differs in the way that is unsupervised learning – meaning it doesn’t have a pre-set outcome but looks for commonalities in the data. For a short comparison between classification and clustering, see the table below.

Examples of clustering can be found a lot in marketing where the technique is used to discover customer groups with similar needs so they can be targeted more specifically with products or services. In politics, clustering is used to identify specific clusters of voters to be able to target these groups with specific messages. This is how Barack Obama famously campaigned partly based on data analysis.

Cluster analysis is often the starting point for classification analysis as it helps define groups of interest.

### How can it help address organizational challenges with people data?

As an organization, I would like to know which employees I should match with which customers to increase customer satisfaction

Customer satisfaction is a critical business outcome for most organizations so it would be great to know which employees are a great match with which sort of customer. One insurance company I’ve dealt with actually conducted text mining on customer and employee feedback following calls in a call center as input for a factor analysis where they found clusters of preferred communication styles.

Based on this information, they developed an algorithm to patch customers through to specific call center employees based on the customer’s and employee’s communication preferences. By leveraging this, they were able to increase customer satisfaction.

### Association analysis

Association analysis or association rule mining (ARM) is a technique that enables a data scientist to find patterns within large collections of data. It creates value by discovering relevant associations between different variables in a large-scale database. The interpretation of patterns is not easy as there is a huge number of patterns possible and associations or patterns are often meaningless. It helps to limit algorithms in advance so the data ‘noise’ is reduced as much as possible.

Common examples come from retail and supermarket chains that use ARM techniques to create their floor plan following patterns found in shopping behavior:

(X% of people who bought juice from brand A also bought chocolate from brand B so let’s put those items in the same aisle at the same height).

Based on the rules generated, the store manager can strategically place the products together or in sequence leading to growth in sales and, in turn, revenue of the store. In banking, they use similar techniques to offer products to customers that follow a certain buying pattern.

### How can it help address organizational challenges with people data?

This technique could be used to identify patterns in HR practices such as onboarding, career paths, education, and talent management and next identify which patterns are associated with happy and productive employees. It could then be used to feedback to an HR system for customized content. Much like the way Amazon and Netflix offer customized content to us as consumers.

### Anomaly detection analysis

Anomaly detection is a method with a focus on recognizing unexpected or deviant patterns. These are techniques that can label new situations as ‘deviant’ based on historical data. It is all about recognizing the outliers and when you are dealing with large datasets it helps to have an algorithm to do the heavy lifting for you.

In finance, anomaly detection is widely used to identify fraud or unusual transactions. You might have received a call from a bank yourself one day to check if a certain transaction was performed with your knowledge. This was probably based on a signal coming from an anomaly detection algorithm.

Another example is the maintenance need in nuclear powerplants. As you might expect, any conditions that deviate from the normal need to be reported immediately. Analyzing the constant inflow of plant sensor data for anomalies enables that.

### How can it help address organizational challenges with people data?

Accidents at work are often the result of fatigue and long working hours. A review of 12 studies showed that employees working over 12 hours per day had a 38% higher risk of occupational injury than those working 8 hours.

Working 10 hours per day increased the risk of injury by 15% compared to working 8 hours per day. Here anomaly detection analysis could help in identifying employees who work longer than a specified threshold, especially in high-risk occupations such as construction, manufacturing, and engineering. This could help prevent accidents and injuries in the workplace.

### Concluding thoughts

I realize that discussing the data science method and linking possible HR use cases to them is kind of upside-down. Usually, you start with a business challenge and choose a useful analysis and suitable method. But it sometimes helps to look at other sectors and the challenges that are somewhat similar there and get inspired.

Data scientists tend to experiment a lot with different techniques in order to generate an accurate model (as is shown in this employee turnover analysis by Lyndon Sundmark). Often it is not possible to accurately predict which technique will be best to provide answers to a complex research question. This is why it is important for a data scientist to know a variety of different techniques. In addition, it really pays off to get inspired by analytical use cases done in other sectors, for any people analytics practitioner.

I hope this article has triggered you is some way and I challenge you to come up with new use cases that involve people data and will potentially contribute to your organization’s success.

### Rob van Dijk

## Learn more

### Related articles

### Annual HR Report: 23 HR Metrics To Include

### Employee Cost Calculator: How To Calculate the True Cost of an Employee

### Absenteeism Rate: How To Calculate It (Plus Free Calculator)

### New articles

### HR Budgeting Best Practices: How Modern HR Teams Invest for Impact

### Selection Process: 7 Steps, Criteria & Tools To Hire Top Talent

### 7 AI in the Workplace Examples: Benefits & What’s Driving AI Adoption

### Subscribe to our Weekly Newsletter?

- LinkedIn

- Facebook

- Pinterest

- WhatsApp

- Twitter

- Email
