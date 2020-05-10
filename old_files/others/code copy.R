rugby=read.csv("/Users/marcusthuillier/Desktop/Rugby/Excel/Additional_Plots.csv", header=T)
rugby

library(plotly)

data=rugby[,c(1,2,4)]
p <- plot_ly(
  x = data$K_Factor, name = 'K Factor', y = data$Home_Advantage,
  z = data$Brier_Score, type = "heatmap", colorscale='Jet')
p

