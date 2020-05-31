library(ggplot2)
library(dplyr)
library(tidyr)

#Put your path here
PATH = '/Users/forrestdavis/Projects/GardenPath/'

############################
#####   Definite     #######
############################

#load raw def_data (to compare reduced vs unreduced)
def_data = read.csv(paste(PATH, "results/def_raw.csv", sep=''))

#effect of model type (shuffled|ordered) and target_type (reduced|unreduced)
res.aov2 <- aov(surp ~ model_type*target_type, data=def_data)
summary(res.aov2)
TukeyHSD(res.aov2, which = "target_type")

shuff_u <- subset(x=def_data, 
                  subset = model_type == 'shuffled' & target_type == 'unreduced')
shuff_r <- subset(x=def_data, 
                  subset = model_type == 'shuffled' & target_type == 'reduced')

order_u <- subset(x=def_data, 
                  subset = model_type == 'ordered' & target_type == 'unreduced')
order_r <- subset(x=def_data, 
                  subset = model_type == 'ordered' & target_type == 'reduced')

def_mean <- c(mean(shuff_u$surp), mean(shuff_r$surp), mean(order_u$surp), mean(order_r$surp))
exp <- c('Shuffled', 'Shuffled', 'Ordered', 'Ordered')
stim <- c('unreduced', 'reduced', 'unreduced', 'reduced')
ci <- c(qnorm(0.95)*sd(shuff_u$surp)/sqrt(length(shuff_u$surp)), qnorm(0.95)*sd(shuff_r$surp)/sqrt(length(shuff_r$surp)), 
        qnorm(0.95)*sd(order_u$surp)/sqrt(length(order_u$surp)), qnorm(0.95)*sd(order_u$surp)/sqrt(length(order_r$surp)))

GP <- data.frame(exp, stim, def_mean, ci)

#Plot reduced vs unreduced by model type
plt5 <- ggplot(GP, aes(x=exp, y=def_mean, fill=stim)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Reduced", "Unreduced")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=def_mean-ci, ymax=def_mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(0, 25)

plt5 <- plt5 +labs(title="Surprisal of Reduced vs. Unreduced",
                   x ="Training Method", y = "Mean Surprisal (disambiguating region)")

######################################
#    Contexts
######################################

##New Indef - New Def
def_data_context = read.csv(paste(PATH, "results/def_diff.csv", sep=''))
#restrict to just reduced
def_data_context = subset(x=def_data_context, subset= target_type=='reduced')

indef_def_shuff <- subset(x = def_data_context, 
                        subset=model_type=='shuffled' & condition=='New_Indef_Def')
indef_def_ordered <- subset(x = def_data_context, 
                        subset=model_type=='ordered' & condition=='New_Indef_Def')


t.test(indef_def_shuff$surp, indef_def_ordered$surp)
t.test(indef_def_ordered$surp,mu=0)
t.test(indef_def_shuff$surp,mu=0)

mean <- c(mean(indef_def_shuff$surp), mean(indef_def_ordered$surp))
exp <- c('Shuffled', 'Ordered')
stim <- c('reduced', 'reduced')
ci <- c(qnorm(0.95)*sd(indef_def_shuff$surp)/sqrt(length(indef_def_shuff$surp)), 
        qnorm(0.95)*sd(indef_def_ordered$surp)/sqrt(length(indef_def_ordered$surp)))

Context <- data.frame(exp, stim, mean, ci)

plt6 <- ggplot(Context, aes(x=exp, y=mean, fill=exp)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9))

plt6 <- plt6 +labs(title="Surprisal of Garden Path between Contexts",
                   x ="Training Method", y = "Surprisal of Indefinite minus Definite")


## New Def - Old Def
def_data_context = read.csv('/Users/forrestdavis/Projects/GardenPath/results/def_diff.csv')
#restrict to just reduced
def_data_context = subset(x=def_data_context, subset= target_type=='reduced')

new_old_shuff <- subset(x = def_data_context, 
                          subset=model_type=='shuffled' & condition=='New_Old_Def')
new_old_ordered <- subset(x = def_data_context, 
                            subset=model_type=='ordered' & condition=='New_Old_Def')


t.test(new_old_shuff$surp, new_old_ordered$surp)
t.test(new_old_ordered$surp,mu=0)
t.test(new_old_shuff$surp,mu=0)

mean <- c(mean(new_old_shuff$surp), mean(new_old_ordered$surp))
exp <- c('Shuffled', 'Ordered')
stim <- c('reduced', 'reduced')
ci <- c(qnorm(0.95)*sd(new_old_shuff$surp)/sqrt(length(new_old_shuff$surp)), 
        qnorm(0.95)*sd(new_old_ordered$surp)/sqrt(length(new_old_ordered$surp)))

Context <- data.frame(exp, stim, mean, ci)

plt7 <- ggplot(Context, aes(x=exp, y=mean, fill=exp)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9))

plt7 <- plt7 +labs(title="Surprisal of Garden Path between Contexts",
                   x ="Training Method", y = "Surprisal of Discourse New minus Old")
