rugby=read.csv("/Users/marcusthuillier/Desktop/Rugby/Scores.csv", header=T)
print(rugby)

rugby$Predicted <- rugby$AwayRanking - rugby$HomeRanking
rugby$AdjustedPredicted <- rugby$AwayRanking - rugby$HomeRanking
rugby$TrueMargin <- rugby$AwayScore - rugby$HomeScore

rugby$diff <- rugby$Predicted - rugby$TrueMargin
rugby$adjdiff <- rugby$AdjustedPredicted - rugby$TrueMargin
rugby

sum(rugby$diff, na.rm=TRUE)
sum(rugby$adjdiff, na.rm=TRUE)
sd(rugby$diff, na.rm=TRUE)
sd(rugby$adjdiff, na.rm=TRUE)

library(ggplot2)
library(dplyr)

ggplot(rugby, aes(TrueMargin, Predicted)) + geom_point()
ggplot(rugby, aes(TrueMargin, AdjustedPredicted)) + geom_point()
fit1=lm(rugby$Predicted ~ rugby$TrueMargin)
summary(fit1)
fit2=lm(rugby$AdjustedPredicted ~ rugby$TrueMargin)
summary(fit2)






#############################

data_frame(
  x = seq(-50, 50, 0.5),
  y = dnorm(seq(-50, 50, 0.5), mean = 9, sd = 11.36)
) %>%
  mutate(winner = ifelse(x <= 0, "South Africa", "New Zealand")) %>%
  ggplot() +
  geom_ribbon(aes(x = x, ymin = 0, ymax = y, fill = winner)) +
  labs(x = "away team's margin of victory")

pnorm(0, mean = -15, sd = 11.36, lower.tail = TRUE)




fit1=lm(rugby$Win...1 ~ rugby$Predicted.margin)
summary(fit1)
fit2=lm(rugby$Win...2 ~ rugby$Predicted.margin)
summary(fit2)

plot(rugby$Predicted.margin,fit1$resid,xlab="t",ylab="Residual",pch=16)
anova(fit1)
confint(fit1,"rugby$Predicted.margin",level=0.95)


