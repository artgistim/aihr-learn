---
title: "9 HR Analytics Terms You Should Know"
source: "https://www.aihr.com/blog/9-hr-analytics-terms-know/"
author: "Erik van Vulpen"
published: "2016-06-29T09:29:09+00:00"
modified: "2023-09-27T12:59:17+00:00"
downloaded_at: "2026-09-11T04:03:37.937512+00:00"
usage: 個人學習；內容版權屬原作者與 AIHR
---

> 原文：https://www.aihr.com/blog/9-hr-analytics-terms-know/
> 本地副本僅供個人學習；引用與分享請回到原文並遵守網站條款。
When we talk about HR data analytics, we use words such as machine learning, algorithms and data mining. However, do we actually know the meaning of these terms? To be honest, the first time I heard them, I didn’t… This blog goes into some commonly used HR analytics terms.

### 1. Data mining

Data mining is like digging for gold. Gold-diggers sift through piles of dirt and stone in the hope of discovering a piece of shiny gold. Data mining is the process of discovering patterns in piles of raw data and turning them into tangible information, which, in turn, can be used to make predictions about real life behavior or events. Remarkably, 99.5% of all data in the world has never been analyzed.

A technique that is used in data mining is called machine learning.

### 2. Machine learning

Machine learning is a technique that is commonly used in the data mining process. Through this technique, a machine (computer) will learn from your data by analyzing it and identifying patterns. This means that machine learning can be considered as a form of artificial intelligence (AI) as it provides computers with the necessary tools they need in order to absorb new information.

### 3. Decision tree

As I explained in a previous blog, a decision tree is a model that looks like a tree and consists of decisions and their possible consequences. This is a useful tool to make predictions about the (near) future. A decision tree allows you to predict what might happen by learning from existing data. This is very much like the way everyone learns from their past experiences. In a decision tree, every decision is represented as a node and every outcome option as a branch.

In my previous blog on predictive analytics in HR, I explained the concept of a decision tree by means of an example: I tried to predict whether kids would play outside based on fourteen days of weather data. That decision tree looked like as follows:

This tree shows that kids are likely to play outside when the outlook is sunny (yes). When the outlook is rainy, kids are not likely to play outside (no). This decision tree was produced using Weka, a free data-mining application, and it has a predictive accuracy of 71%.

Related: Learn more about Recruiting Metrics

### 4. R

Many HR practitioners often use Excel. However, most predictive HR analysists use R. R is arguably the most popular tool for data scientists . R is a (free) open-source system for statistical computation and visualization. It also enables you to work with massive data sets that would be too big to handle in Excel.

### 5. Structured vs. unstructured data

We talk about data a lot. There are two distinctions in data. When it is neatly organized in a spreadsheet or database it is called structured data. For instance, HR knows the names of its employees, their age, where they live, in which department they work, how they perform, et cetera. All this data is structured: by looking up a name or ID, you can easily find a person’s details.

Unstructured data is the opposite. Its lack of structure makes ordering this data a time and energy consuming necessity. Take emails, for instance. It is impossible to accurately order emails on subject or content (hence unstructured). This data most likely needs to be structured before it can be analyzed.

### 6. Supervised vs. unsupervised learning

In supervised machine learning the output data is provided, meaning that the computer has data it can learn from. An example: when you want to predict voluntary turnover the easiest way is to let a computer learn from the past. In a supervised model the computer analyzes the data of the people who left the company voluntarily. It then compares this data with the people who remained at the company at that same period of time. This information tells the computer who left the company and who did not and enables it to make a predictive model of the employees that are likely to leave. This is an example of supervised machine learning.

There is no output data in unsupervised learning. A computer can still make predictions based on this data by clustering sets of related points of data. In the next example you will see how (supervised) clustering works.

Related: An overview of Human Resources metrics

### 7. Clustering

Clustering is a type of machine learning that makes predictions by clustering data.

Clustering data means that the computer looks for groups that share some similarities. The following example shows 1,000 data points divided in three clusters. This is a supervised example because you know which data point belongs to which cluster.

Machine learning makes it is possible to make estimations of the different clusters. Additionally, when a new point of data is introduced, the algorithm is able to predict in which cluster it most likely belongs. A point of data in the bottom right is more likely to be part of cluster 1, and a data point in the top right is more likely to belong to cluster 2. This is, of course, a relatively simple example. Reality is usually a bit more complex.

### 8. Training data vs. test data

When you have a data set, you can build a predictive algorithm. But how do you know if the predictions are accurate? In order to find out you need a second set of data. This is a test set.

Usually test data and training data are created by splitting one full data set (see the picture below). The first part of this set is for training purposes. This will be used to create your predictive algorithm. The second set of data is test data. This (unknown) data will be used once the algorithm is created in order to test how accurate your algorithm’s predictions are.

If you do not separate these two data sets, you will test the accuracy of your algorithms on the same data you used to create the algorithm in the first place. This is a fundamental flaw and could lead to something called ‘overfitting’.

Related: the HR dashboard , how to create it?

### 9. Overfitting

Not all predictive models are equal.

Machine learning is a complex technique and it can provide very detailed analyses. Because of this level of detail, it is at risk of ‘overfitting’. This means that anyone can create an algorithm that has the ability to predict his/her data with an (almost) perfect accuracy! Take the 14-day weather data example we mentioned earlier.

This graphic shows a decision tree that can predict whether or not kids would play outside in the past 14 days with a 100% accuracy. This model is obviously very detailed because it is tailored to our specific data set.

Compare this model to the model below. The model below is simple and self-explanatory. When the outlook is sunny, kids are likely to be present at the playground. When the outlook is rainy, kids are unlikely to be present at the playground. This model is simple and understandable with our current knowledge.

The model above is unrealistically complex. We used 14 days (rows) of data to build this model. However, our model has 19(!) possible outcomes. This means that there are more possible outcomes than we put in data. In other words: this model is way too complex.

The problem with overfitting is that the model perfectly ‘fits’ to the data we used to build it. However, it has no application in practice. When we would add new data to this model, the accuracy would drop immediately. The accuracy of the much simpler model below would most likely remain consistent.

So, do not be fooled when people say they have a predictive model that can make highly accurate predictions! Under the hood this model might not have that much value after all.

The 9 terms covered in this article obviously do not cover everything you need to know when it comes to HR Analytics. I do hope they will help you better understand what your data-scientist or consultant is talking about. If you know of any terms that should be on this list, feel free to add them by posting a comment.

### Erik van Vulpen

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
