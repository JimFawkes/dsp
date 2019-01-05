# Statistics

# Table of Contents

[1. Introduction](#section-a)  
[2. Why We Are Using Think Stats](#section-b)  
[3. Instructions for Cloning the Repo](#section-c)  
[4. Required Exercises](#section-d)  
[5. Optional Exercises](#section-e)  
[6. Recommended Reading](#section-f)  
[7. Resources](#section-g)

## <a name="section-a"></a>1.  Introduction

[<img src="img/think_stats.jpg" title="Think Stats"/>](http://greenteapress.com/thinkstats2/)

Use Allen Downey's [Think Stats (second edition)](http://greenteapress.com/thinkstats2/) book for getting up to speed with core ideas in statistics and how to approach them programmatically. This book is available online, or you can buy a paper copy if you would like.

Use this book as a reference when answering the 6 required statistics questions below.  The Think Stats book is approximately 200 pages in length.  **It is recommended that you read the entire book, particularly if you are less familiar with introductory statistical concepts.**

Complete the following exercises along with the questions in this file. Some can be solved using code provided with the book. The preface of Think Stats [explains](http://greenteapress.com/thinkstats2/html/thinkstats2001.html#toc2) how to use the code.  

Communicate the problem, how you solved it, and the solution, within each of the following [markdown](https://guides.github.com/features/mastering-markdown/) files. (You can include code blocks and images within markdown.)

## <a name="section-b"></a>2.  Why We Are Using Think Stats 

The stats exercises have been chosen to introduce/solidify some relevant statistical concepts related to data science.  The solutions for these exercises are available in the [ThinkStats repository on GitHub](https://github.com/AllenDowney/ThinkStats2).  You should focus on understanding the statistical concepts, python programming and interpreting the results.  If you are stuck, review the solutions and recode the python in a way that is more understandable to you. 

For example, in the first exercise, the author has already written a function to compute Cohen's D.  **You could import it, or you could write your own code to practice python and develop a deeper understanding of the concept.** 

Think Stats uses a higher degree of python complexity from the python tutorials and introductions to python concepts, and that is intentional to prepare you for the bootcamp.  

**One of the skills to learn here is to understand other people’s code.  And this author is quite experienced, so it’s good to learn how functions and imports work.**

---

## <a name="section-c"></a>3.  Instructions for Cloning the Repo 
Using the [code referenced in the book](https://github.com/AllenDowney/ThinkStats2), follow the step-by-step instructions below.  

**Step 1. Create a directory on your computer where you will do the prework.  Below is an example:**

```
(Mac):      /Users/yourname/ds/metis/metisgh/prework  
(Windows):  C:/ds/metis/metisgh/prework
```

**Step 2. cd into the prework directory.  Use GitHub to pull this repo to your computer.**

```
$ git clone https://github.com/AllenDowney/ThinkStats2.git
```

**Step 3.  Put your ipython notebook or python code files in this directory (that way, it can pull the needed dependencies):**

```
(Mac):     /Users/yourname/ds/metis/metisgh/prework/ThinkStats2/code  
(Windows):  C:/ds/metis/metisgh/prework/ThinkStats2/code
```

---


## <a name="section-d"></a>4.  Required Exercises

*Include your Python code, results and explanation (where applicable).*

***Note: I re-wrote, refactored or copied all of the code that is necessary for these exercises.
The code can be found in the directory `custom_code`.***

### Q1. [Think Stats Chapter 2 Exercise 4](statistics/2-4-cohens_d.md) (effect size of Cohen's d)  
Cohen's D is an example of effect size.  Other examples of effect size are:  correlation between two variables, mean difference, regression coefficients and standardized test statistics such as: t, Z, F, etc. In this example, you will compute Cohen's D to quantify (or measure) the difference between two groups of data.   

You will see effect size again and again in results of algorithms that are run in data science.  For instance, in the bootcamp, when you run a regression analysis, you will recognize the t-statistic as an example of effect size.

---
Results: *You can find a working jupyter notebook with the solution for this exercise [here](custom_code/chap02_ex_4.ipynb).*

The question in this exercise is: Are first Babies heavier or lighter than other babies.

The first step is to read clean and filter the necessary data. In this case we are only interested in the total weight `totalwgt_lb` of live births. We then split the dataframe into first borns `first` and all others `other`.

```python
df = ts2.read_fem_preg(clean=True)
live = df[df['outcome'] == 1]
first = live[live['birthord'] == 1]
other = live[live['birthord'] != 1]
```

I then wrote a class to calculate a histogram and other interesting statistics. The next step is to create a histogram for the `totalwgt_lb` column both for `first` and `other`.

```python
first_totalwgt_lb_hist = Hist(first.totalwgt_lb)
other_totalwgt_lb_hist = Hist(other.totalwgt_lb)
```
We can then compare the results for both histograms.

```
# first
first_totalwgt_lb_hist.print_stats()

Column Name: 	 totalwgt_lb
Mean: 		 7.201
Median: 	 7.312
Variance: 	 2.018
Std Dev.: 	 1.42
Outliers: 	 [(0.125, 1), (0.3125, 1), (0.4375, 1), (0.625, 1), (0.9375, 1)]


# other
other_totalwgt_lb_hist.print_stats()

Column Name: 	 totalwgt_lb
Mean: 		 7.326
Median: 	 7.375
Variance: 	 1.943
Std Dev.: 	 1.394
Outliers: 	 [(0.5625, 1), (0.625, 1), (1.125, 1), (1.25, 1), (1.3125, 1)]
```

When comparing these two results, we can see that the mean values are very close to each other which suggests that there is no significant difference in the total birth weight of first-borns vs others.

Next we calculate `Cohen's d` to further compare the two data sets.

```python
d = first_totalwgt_lb_hist.cohens_d(other_totalwgt_lb_hist)
print(f"The absolute value of `Cohen's d` is: {abs(d)}")

The absolute value of `Cohen's d` is: 0.08868218237434661
```

**Conclusion:**
The difference in the mean value between first borns (`7.201`) and others (`7.326`) is very low (`0.125`) and therefore not significant.
When looking at the absolute value of the 'effect size' using `Cohens's d` when comparing first borns and others, we can see, that with an absolute value of `0.089` the difference is very small and below the value of `0.2`. This result reinfoces the assumption, that there is no significant difference in the birth weight of first borns and others.


### Q2. [Think Stats Chapter 3 Exercise 1](statistics/3-1-actual_biased.md) (actual vs. biased)
This problem presents a robust example of actual vs biased data.  As a data scientist, it will be important to examine not only the data that is available, but also the data that may be missing but highly relevant.  You will see how the absence of this relevant data will bias a dataset, its distribution, and ultimately, its statistical interpretation.

---
Results: *You can find a working jupyter notebook with the solution for this exercise [here](custom_code/chap03_ex_1.ipynb).*

In this exercise we compare unbiased with biased data. We will compare the actual number of siblings in a family with the biased observation made by the kids within those families.

The first step is again to read all the necessary data. In this case we will use the respondents data set.
```python
respondents = ts2.read_female_respondents_data(clean=False)
```

Next we calculate the histogram for the column numkdhh which lists the number of kids in the household.
*Note: all cases with 5 or more kids in the household are grouped together and counted as 5 kids.*

First the unbiased data along with the bar graph:

```python
# Unbiased Distribution
children_hist = Hist(respondents.numkdhh)
_ = children_hist.plot(dict_name=children_hist.pmf.pmf, label='Children Count')
```

## #TODO: Copy missing plots

Then the biased data along with the bar graph:
```python
# Biased Distribution
children_biased_hist = BiasedHist(respondents.numkdhh)
_ = children_biased_hist.plot(dict_name=children_biased_hist.pmf.pmf, label='Children Count')
```

## #TODO: Copy missing plots

Finally we compare the mean and other statistics of both distributions:

```
# Unbiased Distribution
children_hist.print_stats()

Column Name: 	 numkdhh
Mean: 		 1.024
Median: 	 1
Variance: 	 1.413
Std Dev.: 	 1.189
Outliers: 	 [(1, 1636), (2, 1500), (3, 666), (4, 196), (5, 82)]


# Biased Distribution
children_biased_hist.print_stats()
Column Name: 	 numkdhh
Mean: 		 2.404
Median: 	 1
Variance: 	 1.202
Std Dev.: 	 1.096
Outliers: 	 [(0, 0), (1, 1636), (3, 1998), (4, 784), (5, 410)]
```

**Conclusion:**
We can observe a significant shift in the mean when comparing these two distributions.

### Q3. [Think Stats Chapter 4 Exercise 2](statistics/4-2-random_dist.md) (random distribution)  
This questions asks you to examine the function that produces random numbers.  Is it really random?  A good way to test that is to examine the pmf and cdf of the list of random numbers and visualize the distribution.  If you're not sure what pmf is, read more about it in Chapter 3.

---
Results: *You can find a working jupyter notebook with the solution for this exercise [here](custom_code/chap04_ex_2.ipynb).*

In this exercise we generate 1000 random numbers using the `random` package in the python standard library. We then use the cdf to test the assumption that the random numbers generated are uniformly distributed.

First we need to generate the random number:

```python
ml = [random.random() for x in range(1000)]
```

Next we instantiate the histogram for this list.
```python
random_hist = Hist(ml)
```

Finally we examine the different statistics and plots for this distribution.
If the random values are uniformly distributed, we expect to see a mean of 0.5.

```python
random_hist.mean

0.4865046795783088
```

Alternatively we can look at the quantiles of the distribution. Here we would expect to see the step length to be very close to the percentile.
```python

random_hist.cdf.quantile(10)

((0, 0.0006756584518546882),
 (0.1, 0.09466907914454925),
 (0.2, 0.18832014960311283),
 (0.3, 0.2919395618934151),
 (0.4, 0.38940385463982574),
 (0.5, 0.4893812370232884),
 (0.6, 0.5721238362516025),
 (0.7, 0.6637160028523832),
 (0.8, 0.7757201627797841),
 (0.9, 0.8827352274093908))
```

We can also look at the plots of the pmf and cdf functions.

## #TODO: Copy missing plots

**Conclusion:**
We are looking at a small set of random numbers, but the distribution is still very close to what we expect from a uniform distribution.



### Q4. [Think Stats Chapter 5 Exercise 1](statistics/5-1-blue_men.md) (normal distribution of blue men)
This is a classic example of hypothesis testing using the normal distribution.  The effect size used here is the Z-statistic. 


---
Results: *You can find a working jupyter notebook with the solution for this exercise [here](custom_code/chap05_ex_1.ipynb).*

In this exercise we calculate the percentage of the US male population which is in the specific hight range required by the Blue Man Group.

The goal is to use the normal distribution with the parameters µ = 178 cm and σ = 7.7 cm as a model instead of using an actual data set.

The first step is to get the hight range in centimeters:
```python
lower_hight_limit = round(convs.us_hight2m(feet=5, inches=10) * 100, 1)
upper_hight_limit = round(convs.us_hight2m(feet=6, inches=1) * 100, 1)
lower_hight_limit, upper_hight_limit

(177.8, 185.4)
```
Next we set the parameters for the normal distribution:
```python
mu = 178
sigma = 7.7
dist = scipy.stats.norm(loc=mu, scale=sigma)
```

We can then calculate the cdf for these values:

```python
low, high, diff = dist.cdf(lower_hight_limit), dist.cdf(upper_hight_limit), dist.cdf(upper_hight_limit) - dist.cdf(lower_hight_limit)
low, high, diff

(0.48963902786483265, 0.8317337108107857, 0.3420946829459531)
```
**Results:**
About 34.2% of the US male population is within the range of 177.8 cm and 185.4 cm


*Note: in [this notebook](custom_code/chap05_ex_1.ipynb) there is a comparisson to the same results taken from the BRFS data set.*


### Q5. Bayesian (Elvis Presley twin) 

Bayes' Theorem is an important tool in understanding what we really know, given evidence of other information we have, in a quantitative way.  It helps incorporate conditional probabilities into our conclusions.

Elvis Presley had a twin brother who died at birth.  What is the probability that Elvis was an identical twin? Assume we observe the following probabilities in the population: fraternal twin is 1/125 and identical twin is 1/300.  


---
Results: *You can find a working jupyter notebook with the solution for this exercise [here](custom_code/baysian_elvis_twins.ipynb).*

The question here is, given the fact that Elvis had a twin, what is the probability, that it was an identical twin.

With the Bayesian Theorem we can calculate the probability of an event if we have knowlege of the condition which is in our case the fact that Elvis had a twin.

To calculate the probability we first need to define the events and probabilities:

```
Bayes Theorem:
P(A|B) = (P(B|A) * P(A))/ P(B)

In this case the Variables describe the following events:
    A: Brother is an identical twin
    B: Elvis has a twin
    
The probabilities are:
    P(B|A)=1 -> Given the fact that the brother is an identical twin, how high is the chance that the brother is a twin.
    P(A) = 1/300 -> Chance of a person having an identical twin.
    P(B) = 1/125 + 1/300 -> Chance of a person being a twin.
```

If we now calculate:
```python
p_fraternal = 1/125
p_identical = 1/300
p_twin = p_fraternal + p_identical

p = (1*p_identical)/p_twin
print(f"The probability that Elvis was an identical twin, if the fact that elvis had a twin is true, is {round(p, 3) * 100}%")
```
We get: **The probability that Elvis was an identical twin, if the fact that elvis had a twin is true, is 29.4%**

### Q6. Bayesian &amp; Frequentist Comparison  
How do frequentist and Bayesian statistics compare?

---
Frequentist and Bayesian probability are different interpretations of probability. They are also called the Frequentist or Bayesian School.

Frequentist probability:


Bayesian probability:



---

## <a name="section-e"></a>5.  Optional Exercises

The following exercises are optional, but we highly encourage you to complete them if you have the time.

### Q7. [Think Stats Chapter 7 Exercise 1](statistics/7-1-weight_vs_age.md) (correlation of weight vs. age)
In this exercise, you will compute the effect size of correlation.  Correlation measures the relationship of two variables, and data science is about exploring relationships in data.    

### Q8. [Think Stats Chapter 8 Exercise 2](statistics/8-2-sampling_dist.md) (sampling distribution)
In the theoretical world, all data related to an experiment or a scientific problem would be available.  In the real world, some subset of that data is available.  This exercise asks you to take samples from an exponential distribution and examine how the standard error and confidence intervals vary with the sample size.

### Q9. [Think Stats Chapter 6 Exercise 1](statistics/6-1-household_income.md) (skewness of household income)
### Q10. [Think Stats Chapter 8 Exercise 3](statistics/8-3-scoring.md) (scoring)
### Q11. [Think Stats Chapter 9 Exercise 2](statistics/9-2-resampling.md) (resampling)

---

## <a name="section-f"></a>6.  Recommended Reading

Read Allen Downey's [Think Bayes](http://greenteapress.com/thinkbayes/) book.  It is available online for free, or you can buy a paper copy if you would like.

[<img src="img/think_bayes.png" title="Think Bayes"/>](http://greenteapress.com/thinkbayes/) 

---

## <a name="section-g"></a>7.  More Resources

Some people enjoy video content such as Khan Academy's [Probability and Statistics](https://www.khanacademy.org/math/probability) or the much longer and more in-depth Harvard [Statistics 110](https://www.youtube.com/playlist?list=PL2SOU6wwxB0uwwH80KTQ6ht66KWxbzTIo). You might also be interested in the book [Statistics Done Wrong](http://www.statisticsdonewrong.com/) or a very short [overview](http://schoolofdata.org/handbook/courses/the-math-you-need-to-start/) from School of Data.
