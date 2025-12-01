library(dplyr)
library(stringr)
library(purrr)

df <- read.csv(
  "aoc/2025/day01/resources/input.txt",
  sep = ",",
  header = FALSE,
  stringsAsFactors = FALSE
) %>%
  rename(raw = V1) %>%                    
  mutate(
    value = str_extract(raw, "\\d+") |>    
              as.integer(),
    value = if_else(str_starts(raw, "L"), -value, value)  
  )

df <- df %>%
  mutate(folded = accumulate(value, `+`, .init = 50)[-1]) %>%
  mutate(folded.mod = accumulate(value, ~ (.x + .y) %% 100, .init = 50)[-1]) %>%
  mutate(folded.div = abs(((folded - value) %% 100 + value) %/% 100))

print(sum(df$folded.mod == 0))
print(sum(df$folded.div))

print(
    df %>% summarise(
        total.zerosa = sum(folded.mod == 0), 
        total.zerosb = sum(folded.div)
))
