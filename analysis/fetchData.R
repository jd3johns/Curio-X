##'
##' Fetch datasets
##' ==============
##' 
##' Import all csv datafiles and merge into one dataset.
##'
##' Good to have scripts focused on one task ("do one thing really
##' well").
source('options.R')

logs <- read.csv("data/logs.csv") %>% tbl_df() ## Converts into a dataframe table (dplyr)
results <- read.csv("data/results.csv") %>% tbl_df()
gold <- read.csv("data/goldstandard.csv") %>% tbl_df()
timg <- read.csv("data/testimages.csv") %>% tbl_df()
eng <- read.csv("data/engagement.csv") %>% tbl_df()

##' Check datasets
logs
results
gold
timg
eng

##' Check the names contained within each dataset.
names(logs)
names(results)
names(gold)
names(timg)
names(eng)

##'
##' Merge datasets together
##' =======================
##' 
##' Jon: These names are already the same are they not? What if they
##' aren't the same?  This is generally bad practice to do.  There are
##' better ways around this. :)
##names(gold) == names(results)

##' A dplyr solution. This accomplishes what you were trying to do below.
df <- full_join(results, gold) %>%
  mutate(class = ifelse(User == 'RobJon', 'gold', 'userResult') %>%
           as.factor())
##' Generally, I find that the default why of doing R (like you are
##' doing below) is messy and ugly. dplyr on the other hand is really
##' nice to look at... :P
## all$class[all$User == "RobJon"] <- "gold"
## all$class[all$User != "RobJon"] <- "userResult"
## all$class <- as.factor(all$class)

##' Output the merged data into a single RData file.
save(df, file = 'data/mergedData.RData')
