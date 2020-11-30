#libs
library(tidyverse)
library(janitor)

contratar_df <- read_csv('contratar.csv') %>% 
  clean_names()



#parse monto

contratar_df <- contratar_df %>% 
  mutate(monto_1 = str_sub(monto, start = 1L, end = -3) %>% 
           str_remove_all('\\.') %>% 
           as.numeric(),
         monto_resto = (str_sub(monto, start = -2) %>% 
                          as.numeric())/100 ,
         monto = monto_1 + monto_resto) %>% 
  select(-monto_1, -monto_resto)

# adjudicados

adjudicados_df <- contratar_df %>% 
  filter(tramite_estado == 'Adjudicado')
