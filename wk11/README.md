### Homework 11: Robotics and Deep Reinforcement Learning
#### Vaibhav K Beohar - June 2020

<br>

*  What parameters did you change?

  I mostly stuck with changing the density layers of the Neural Network, batch size and epsilon_min parameters to try to make the model converge to an average score of 200 in as little iterations as possible.

* What values did you try?

  Since there was no such "set rule" with the parameters, I felt inclined to test various combinations to converge the model with various rounds of training combinations.

  As such, I changed values in different combinations of parameters across 6 rounds of training (spread across multiple days):

  ```
  | Round | density_first_layer | density_second_layer | epsilon_min | batch_size |
  |-------|---------------------|----------------------|-------------|------------|
  | 1st   | default (32)        | default (16)         | 64          | 0.01       |
  | 2nd   | 144                 | 264                  | 128         | 0.01       |
  | 3rd   | 264                 | 144                  | 128         | 0.001      |
  | 4th   | 200                 | 100                  | 72          | 0.01       |
  | 5th   | 64                  | 32                   | 64          | 0.01       |
  | 6th   | 256                 | 200                  | 128         | 0.001      |
  ```
  <u>Example of a successful training landing</u>  
  <img src="submission_files/ezgif.com-video-to-gif.gif" width="600" />

  <u>Example of a default training parameters</u>
  <p float="left">
    <img src="submission_files/1st_round_train_params.png" width="600" />
  </p>

  <u>Example of 6th round parameters</u>
  <p float="left">
    <img src="submission_files/6th_round_train_params.png" width="500" />
  </p>

* Did you try any other changes that made things better or worse?

  I did not change most of the other params. I initially dabbled with changing `gamma` parameter. But realized that even with very small value changes, the model output was behaving differently (and unpredictably) for different layer sizes. Hence I decided to leave most other params unchanged, partly because of lack of intuition and partly because of large training times.

* Did they improve or degrade the model? Did you have a test run with 100% of the scores above 200?

  As per my observation, increasing the density layers had the most significant difference in performance and convergence time.

  However, it is interesting to note that round 5 of my training (`density_first_layer=64, density_second_layer=32, epsilon_min= 0.01, batch_size=64`) had almost same (if not better) training performance as compared to round 6 (`density_first_layer=256, density_second_layer=200, epsilon_min= 0.001, batch_size=128`).

  As you can tell from below, round 5 converged to a score of 200 in 505 training iterations, whereas round 6 converged to the same result in 474 iterations.

  But what is more interesting is that round 5 "test" scores were almost consistently better than those of round 8 (despite having denser layers).

  <u>Stacktrace of results</u>

  <u>5th round training</u>
  <p float="left">
    <img src="submission_files/6th_round_results.png" width="500" />
  </p>

  <u>6th round training</u>
  <p float="left">
    <img src="submission_files/8th_final_round_final_scores.png" width="500" />
  </p>


* Based on what you observed, what conclusions can you draw about the different parameters and their values?

  Increasing the variables in the first two layers increases the density of the neural network. The batch size also enhances the model performance by allowing more data to be processed in each iteration, leading to performance improvements.

  Here are some snapshots of the training parameters from various runs.

* What is the purpose of the epsilon value?

  Epsilon value indicates the method to balance exploration and exploitation by choosing between exploration and exploitation randomly.

  The epsilon values indicates to the algorithm the probability of choosing to explore (the algorithm exploits most of the time with a small chance of exploring).

  Over time the as the training progresses, we see that the epsilon goes down, indicating that the algorithm gets more confident in exploiting rather than exploring (a.k.a epsilon decay):


* Describe "Q-Learning".

  Q-learning is an off policy reinforcement learning algorithm that seeks to find the best action to take given the current state.

  It’s considered off-policy because the q-learning function learns from actions that are outside the current policy, like taking random actions, and therefore a policy isn’t needed. More specifically, q-learning seeks to learn a policy that maximizes the total reward.

  The ‘q’ in q-learning stands for quality. Quality in this case represents how useful a given action is in gaining some future reward.

  (courtsey: https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56#:~:text=Q%2Dlearning%20is%20an%20off,a%20policy%20isn't%20needed.)


Videos
------
  https://vebsbuck.s3.us-east.cloud-object-storage.appdomain.cloud/episode0_1st_round.mp4

  https://vebsbuck.s3.us-east.cloud-object-storage.appdomain.cloud/episode100_1st_round.mp4

  https://vebsbuck.s3.us-east.cloud-object-storage.appdomain.cloud/episode500_1st_round.mp4

  https://vebsbuck.s3.us-east.cloud-object-storage.appdomain.cloud/episode1000_1st_round.mp4

  https://vebsbuck.s3.us-east.cloud-object-storage.appdomain.cloud/episode1500_1st_round.mp4

  https://vebsbuck.s3.us-east.cloud-object-storage.appdomain.cloud/episode1580_1st_round.mp4
