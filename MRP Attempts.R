library(rstanarm)
library(ggplot2)
library(dplyr)

ces19 <- read.csv('CES2019 MRP Frame (Nontemporal).csv')
trim <- c("age", "gender", "district", "vote")
ces19 <- ces19[trim]
hist(ces19[,'vote'])
ces19sam = sample_n(ces19, 500)

ces19bin <- read.csv('CEs2019 MRP Frame (Binary).csv')
ces19bin <- ces19bin[trim]
ces19sample = sample_n(ces19bin, 2000)

poststrat16 <- read.csv("2016 Poststratification Frame (By Districts, Simple Model) (age cap 15).csv")
trim2 <- c("age", "gender", "district", "Count")
poststrat16 <- poststrat16[trim2]


fit <- stan_glmer(vote ~ factor(gender)+factor(gender)*factor(age)+(1 | district) + (1 | age), family = gaussian, data = ces19sam)


fit5 <- stan_glmer(
  vote ~ factor(gender) + factor(gender) * factor(age) +
    (1 | district) + (1 | age),
  family = binomial(link = "logit"),
  data = ces19sample
)
