M = matrix( 
  +   c(11.5,26.5,12.5,.5,1.5,85,87,86,52,58), nrow=5, ncol=2)
M
cor(M)


fit <- lm(M[,2]~log(M[,1])+log(M[,1]*M[,1]))
summary(fit)
coef(fit)
plot(log(M[,1]),M[,2])
abline(fit)

x=M[,1]
y=predict(fit,newdata=list(x=M[,1]),interval="confidence")
matlines(x,y,lwd=2)
