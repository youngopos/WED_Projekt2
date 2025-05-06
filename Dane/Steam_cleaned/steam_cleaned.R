library(ggplot2)
library(dplyr)
library(tidyr)

####### WSTĘPNE PRZYGOTOWANIE DANYCH ###########

df <- read.csv('C:/Users/tomus/Desktop/Web_Scraping random/STEAM_final.csv')

df$Score <- as.numeric(gsub(",",".",df$Score))
df$S_recent <- as.numeric(gsub(',','.', df$S_recent))
df$Score_number <- as.numeric(gsub(',','.', df$Score_number))
df$S_recent_number <- as.numeric(gsub(',','.', df$S_recent_number))
df$Achievements <- as.numeric(gsub(',','.', df$Achievements))
df$Curators <- as.numeric(gsub(',','.',df$Curators))


write.csv(df, "cleaned_steam.csv", row.names = FALSE)



df_new <- read.csv('cleaned_steam.csv')










