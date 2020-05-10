rugby=read.csv("/Users/marcusthuillier/Desktop/Rugby/Additional_Plots.csv", header=T)
rugby

library(plotly)
data=as.matrix(rugby[,c(1,2,3)])
heatmap(data)

data=as.matrix(rugby[,c(1,2,4)])
