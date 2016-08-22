# Read & Compile the weather data from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
# July 2016

 # Load the data
setwd('/Users/ozimmer/Google Drive/Berkeley/W205/finalproject')
weather.files <- read.csv('name weather file.csv')

 # Create a schema based on http://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
weather.col <- vector()
weather.col <- c('ID', 'YEAR', 'MONTH', 'ELEMENT')
for (i in (1:31)){
  day <- c(paste0('VALUE', i), paste0('MFLAG', i), paste0('QFLAG', i), paste0('SFLAG', i))
  weather.col <- c(weather.col, day)
}

 # Write schema for big query
write.csv(data.frame(schema = weather.col), 'weather_schema.csv', row.names = FALSE)

 #Convert and filter the data
weather.all <- data.frame()
for (f in weather.files$filename){
  print(f)
  weather.f <- read.fwf(paste0('ghcnd_hcn/ghcnd_hcn/', f), 
                             widths = c(11, 4, 2, 4, rep(c(5, 1, 1, 1),31)))
  colnames(weather.f) <- weather.col
  weather$ELEMENT <- as.character(weather$ELEMENT)
  weather.f <- weather.f[weather.f$YEAR >= 1990,] #keeping most recent years
  weather.f <- weather.f[weather.f$ELEMENT %in% c('TMAX','TMIN'),] #Only pulling temperature data
  weather.all <- rbind(weather.all, weather.f)
}

write.csv(weather.all, 'weather_all.csv', row.names = FALSE)
summary(weather.all)
str(weather.all)
