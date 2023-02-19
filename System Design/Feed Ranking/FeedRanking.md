# Feed Ranking

## 1. Question
Design a personalized LinkedIn feed to maximize long-term user engagement. There are different activities which have very different click through rate (CTR).

On the LinkedIn feed, there are five major activity types:
| Activity Type   | Example    |
| :---:   |  :---: |
| Connections (A connects with B) | User connector follows user/company, user joins group   |
| Informational | User or company shares article/picture/message   |
| Profile | User updates profile, i.e., picture, job-change, etc.   |
| Opinion | User likes or comments on articles, pictures, job-changes, etc.   |
| Site-specific | User endorses user, etc. |

## 2. Metrics design and requirements
**Offline Metric:**

* The Click Through Rate (CTR) for one specific feed is the number of clicks that feed receives, divided by the number of times the feed is shown.
$\frac{no. of clicks}{no. of shown times}$ 

**Online Metric:**
Online metric, such as conversion rate, must represent the degree of involvement from users after the model has been deployed (ratio of clicks with number of feeds)

## 3. Requirements
 **Training**
 * Need to handle large volumes of data during training. Data distribution is changed frequently. [One way to solve this problem is to incrementally multiple times per day.]
 * It should support high level of personalization since different users have different interests and styles for consuming their feed.
 * Data freshness i.e. avoid showing repetitive feed on the user's home feed.

  **Inference**
  * The volume of users activiites are large and the system needs to handle approx. 300 million users. So, it should be highly scalable.
  * Low Latency: When a user goes to LinkedIn, there are multiple pipelines and services that will pull data from multiple sources before feeding activities into the ranking model. All of these steps need to be done within 200 ms. As a result, the Feed Ranking needs to return within 50ms.
  * Data freshness: Feed Ranking needs to be fully aware of whether or not a user has already seen any particular activity. 

### Summary:
* Metrics: Resonable normalized cross-entropy. 
* Training: High throughput with the ability to retrain many times per day.
** Inference: Supports high level of personalization, Latency from 100ms to 200ms, provides a high level of data freshness and avoids showing the same feeds multiple times.

