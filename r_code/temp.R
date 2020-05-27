library(ggplot2)
library(dplyr)
library(tidyr)


############################
#####   Temporal  #######
############################

#load raw ref data
temp_data = read.csv('/Users/forrestdavis/Projects/GardenPath/results/temp_raw.csv')

res.aov2 <- aov(RC_surp ~ model_type*target_type, data = ref_data)
summary(res.aov2)

TukeyHSD(res.aov2, which = "target_type")
TukeyHSD(res.aov2, which = "model_type")

shuff_u <- subset(x = temp_data,
                  subset = model_type == 'shuffled' & target_type == 'unreduced')
shuff_r <- subset(x = temp_data,
                  subset = model_type == 'shuffled' & target_type == 'reduced')

order_u <- subset(x = temp_data,
                  subset = model_type == 'ordered' & target_type == 'unreduced')
order_r <- subset(x = temp_data,
                  subset = model_type == 'ordered' & target_type == 'reduced')

mean <- c(mean(shuff_u$RC_surp), mean(shuff_r$RC_surp), mean(order_u$RC_surp), mean(order_r$RC_surp))
exp <- c('Shuffled', 'Shuffled', 'Ordered', 'Ordered')
stim <- c('unreduced', 'reduced', 'unreduced', 'reduced')
ci <- c(qnorm(0.95)*sd(shuff_u$RC_surp)/sqrt(length(shuff_u$RC_surp)), qnorm(0.95)*sd(shuff_r$RC_surp)/sqrt(length(shuff_r$RC_surp)), 
        qnorm(0.95)*sd(order_u$RC_surp)/sqrt(length(order_u$RC_surp)), qnorm(0.95)*sd(order_r$RC_surp)/sqrt(length(order_r$RC_surp)))

GP <- data.frame(exp, stim, mean, ci)

plt3 <- ggplot(GP, aes(x=exp, y=mean, fill=stim)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Reduced", "Unreduced")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(0, 40)

plt3 <- plt3 +labs(title="Surprisal of Reduced vs. Unreduced",
                   x ="Training Method", y = "Mean Surprisal (verb+by)")


###################################

#Differences by context
temp_data_context = read.csv('/Users/forrestdavis/Projects/GardenPath/results/temp_diff.csv')

shuff_reduced <- subset(x=temp_data_context, 
                        subset=model_type=='shuffled' & target_type=='reduced')
shuff_unreduced <- subset(x=temp_data_context, 
                          subset=model_type=='shuffled' & target_type=='unreduced')

order_reduced <- subset(x=temp_data_context, 
                        subset=model_type=='ordered' & target_type=='reduced')
order_unreduced <- subset(x=temp_data_context, 
                          subset=model_type=='ordered' & target_type=='unreduced')

# verb+by
t.test(shuff_reduced$verb_by_surp, order_reduced$verb_by_surp)
t.test(shuff_reduced$verb_by_surp, mu=0)
t.test(order_reduced$verb_by_surp, mu=0)

t.test(shuff_unreduced$verb_by_surp, order_unreduced$verb_by_surp)
t.test(shuff_unreduced$verb_by_surp, mu=0)
t.test(order_unreduced$verb_by_surp, mu=0)

# by
t.test(shuff_reduced$by_surp, order_reduced$by_surp)
t.test(shuff_reduced$by_surp, mu=0)
t.test(order_reduced$by_surp, mu=0)

t.test(shuff_unreduced$by_surp, order_unreduced$by_surp)
t.test(shuff_unreduced$by_surp, mu=0)
t.test(order_unreduced$by_surp, mu=0)

##np only
t.test(shuff_reduced$NP_surp, order_reduced$NP_surp)
t.test(shuff_reduced$NP_surp, mu=0)
t.test(order_reduced$NP_surp, mu=0)

t.test(shuff_unreduced$NP_surp, order_unreduced$NP_surp)
t.test(shuff_unreduced$NP_surp, mu=0)
t.test(order_unreduced$NP_surp, mu=0)

##main (can't use this since should be future tense -- mistake on my coding)
t.test(shuff_reduced$main_surp, order_reduced$main_surp)
t.test(shuff_reduced$main_surp, mu=0)
t.test(order_reduced$main_surp, mu=0)

t.test(shuff_unreduced$main_surp, order_unreduced$main_surp)
t.test(shuff_unreduced$main_surp, mu=0)
t.test(order_unreduced$main_surp, mu=0)

shuff_r <- shuff_reduced$by_surp
shuff_u <- shuff_unreduced$by_surp

order_r <- order_reduced$by_surp
order_u <- order_unreduced$by_surp

mean <- c(mean(shuff_r), mean(shuff_u), mean(order_r), mean(order_u))
exp <- c('Shuffled', 'Shuffled', 'Ordered', 'Ordered')
stim <- c('reduced', 'unreduced', 'reduced', 'unreduced')
ci <- c(qnorm(0.95)*sd(shuff_r)/sqrt(length(shuff_r)), 
        qnorm(0.95)*sd(shuff_u)/sqrt(length(shuff_u)), 
        qnorm(0.95)*sd(order_r)/sqrt(length(order_r)), 
        qnorm(0.95)*sd(order_u)/sqrt(length(order_u)))

Context <- data.frame(exp, stim, mean, ci)

plt2 <- ggplot(Context, aes(x=stim, y=mean, fill=exp)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9))

plt2 +labs(title="Surprisal of Garden Path between Contexts",
           x ="Training Method", y = "Surprisal of Past minus Future")
