library(grid)
library(gridExtra)
library(ggplot2)

#######################################
### MV/RR and NP/Z reduced/unreduced ##
#######################################

ref_data = read.csv('/Users/forrestdavis/Projects/GardenPath/results/ref_raw.csv')
temp_data = read.csv('/Users/forrestdavis/Projects/GardenPath/results/temp_raw.csv')

mv_rr <- rbind(ref_data, temp_data)

shuff_u <- subset(x = mv_rr,
                  subset = model_type == 'shuffled' & target_type == 'unreduced')
shuff_r <- subset(x = mv_rr,
                  subset = model_type == 'shuffled' & target_type == 'reduced')

order_u <- subset(x = mv_rr,
                  subset = model_type == 'ordered' & target_type == 'unreduced')
order_r <- subset(x = mv_rr,
                  subset = model_type == 'ordered' & target_type == 'reduced')

mean <- c(mean(shuff_u$RC_surp), mean(shuff_r$RC_surp), mean(order_u$RC_surp), mean(order_r$RC_surp))
exp <- c('Shuffled', 'Shuffled', 'Ordered', 'Ordered')
stim <- c('unreduced', 'reduced', 'unreduced', 'reduced')
ci <- c(qnorm(0.95)*sd(shuff_u$RC_surp)/sqrt(length(shuff_u$RC_surp)), qnorm(0.95)*sd(shuff_r$RC_surp)/sqrt(length(shuff_r$RC_surp)), 
        qnorm(0.95)*sd(order_u$RC_surp)/sqrt(length(order_u$RC_surp)), qnorm(0.95)*sd(order_r$RC_surp)/sqrt(length(order_r$RC_surp)))

GP <- data.frame(exp, stim, mean, ci)


plt1 <- ggplot(GP, aes(x=exp, y=mean, fill=stim)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Reduced", "Unreduced")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.1,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(0, 40)

plt1 <- plt1 +labs(x ="(a)", y = "Mean Surprisal at Critical Region") + theme(legend.position="none") 

#load raw def_data 
def_data = read.csv('/Users/forrestdavis/Projects/GardenPath/results/def_raw.csv')

shuff_u <- subset(x=def_data, 
                  subset = model_type == 'shuffled' & target_type == 'unreduced')
shuff_r <- subset(x=def_data, 
                  subset = model_type == 'shuffled' & target_type == 'reduced')

order_u <- subset(x=def_data, 
                  subset = model_type == 'ordered' & target_type == 'unreduced')
order_r <- subset(x=def_data, 
                  subset = model_type == 'ordered' & target_type == 'reduced')

mean <- c(mean(shuff_u$surp), mean(shuff_r$surp), mean(order_u$surp), mean(order_r$surp))
exp <- c('Shuffled', 'Shuffled', 'Ordered', 'Ordered')
stim <- c('unreduced', 'reduced', 'unreduced', 'reduced')
ci <- c(qnorm(0.95)*sd(shuff_u$surp)/sqrt(length(shuff_u$surp)), qnorm(0.95)*sd(shuff_r$surp)/sqrt(length(shuff_r$surp)), 
        qnorm(0.95)*sd(order_u$surp)/sqrt(length(order_u$surp)), qnorm(0.95)*sd(order_u$surp)/sqrt(length(order_r$surp)))

GP <- data.frame(exp, stim, mean, ci)

plt5 <- ggplot(GP, aes(x=exp, y=mean, fill=stim)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "", labels=c("Reduced", "Unreduced")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.1,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(0, 40)

plt5 <- plt5 +labs(x ="(b)", y = "")

blankPlot <- ggplot() + theme_void()

get_legend<-function(myggplot){
  tmp <- ggplot_gtable(ggplot_build(myggplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)
}

legend <- get_legend(plt5)

plt5 <- plt5 + theme(legend.position="none")


gp_plt <- grid.arrange(blankPlot, legend, plt1,plt5, top = textGrob("Surprisal of Reduced vs. Unreduced Targets", gp=gpar(fontsize=30,font=8)),
                       bottom = textGrob("Model Training Method\n", gp=gpar(fontsize=20,font=8)),
                       ncol=2, nrow=2, widths=c(2.7,2.7), heights = c(0.7,3))
#layout_matrix = matrix(c(1,2), ncol=2, byrow=TRUE))


############################
#####   Definite     #######
############################

######################################
#    Contexts
######################################

##New Indef - New Def
def_data_context = read.csv('/Users/forrestdavis/Projects/GardenPath/results/def_diff.csv')
#restrict to just reduced
def_data_context = subset(x=def_data_context, subset= target_type=='reduced')

indef_def_shuff <- subset(x = def_data_context, 
                          subset=model_type=='shuffled' & condition=='New_Indef_Def')
indef_def_ordered <- subset(x = def_data_context, 
                            subset=model_type=='ordered' & condition=='New_Indef_Def')

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
                position=position_dodge(.9)) + ylim(-0.5,2)

plt6 <- plt6 +labs(x ="(a)", y = "Surprisal of Indefinite minus Definite") +  theme(legend.position = "none")

## New Def - Old Def

new_old_shuff <- subset(x = def_data_context, 
                        subset=model_type=='shuffled' & condition=='New_Old_Def')
new_old_ordered <- subset(x = def_data_context, 
                          subset=model_type=='ordered' & condition=='New_Old_Def')

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
                position=position_dodge(.9)) + ylim(-0.5,2)

plt7 <- plt7 +labs(x ="(b)", y = "Surprisal of Discourse New minus Old") + theme(legend.position="none") 

def_plt <- grid.arrange(plt6,plt7, top = textGrob("Surprisal of Garden Path between Contexts\n", gp=gpar(fontsize=30,font=8)),
                             bottom = textGrob("Model Training Method\n", gp=gpar(fontsize=20,font=8)),
                             layout_matrix = matrix(c(1,2), ncol=2, byrow=TRUE))

############################
#####   Ref/Temp     #######
############################

######################################
#    Contexts
######################################

ref_data_context = read.csv('/Users/forrestdavis/Projects/GardenPath/results/ref_diff.csv')

shuff_reduced <- subset(x=ref_data_context, 
                        subset=model_type=='shuffled' & target_type=='reduced')
order_reduced <- subset(x=ref_data_context, 
                        subset=model_type=='ordered' & target_type=='reduced')

mean <- c(mean(shuff_reduced$by_surp), mean(order_reduced$by_surp))
exp <- c('Shuffled', 'Ordered')
stim <- c('reduced', 'reduced')
ci <- c(qnorm(0.95)*sd(shuff_reduced$by_surp)/sqrt(length(shuff_reduced$by_surp)), 
        qnorm(0.95)*sd(order_reduced$by_surp)/sqrt(length(order_reduced$by_surp)))

Context <- data.frame(exp, stim, mean, ci)

plt8 <- ggplot(Context, aes(x=exp, y=mean, fill=exp)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(-0.5,2)

plt8 <- plt8 +labs(x ="(a)", y = "Surprisal of One NP minus Two NP") +  theme(legend.position = "none")


#Differences by context temp
temp_data_context = read.csv('/Users/forrestdavis/Projects/GardenPath/results/temp_diff.csv')

shuff_reduced <- subset(x=temp_data_context, 
                        subset=model_type=='shuffled' & target_type=='reduced')
shuff_unreduced <- subset(x=temp_data_context, 
                          subset=model_type=='shuffled' & target_type=='unreduced')

order_reduced <- subset(x=temp_data_context, 
                        subset=model_type=='ordered' & target_type=='reduced')
order_unreduced <- subset(x=temp_data_context, 
                          subset=model_type=='ordered' & target_type=='unreduced')

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

plt9 <- ggplot(Context, aes(x=stim, y=mean, fill=exp)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(-0.5,2)

plt9 <- plt9 +labs(x ="(b)", y = "Surprisal of Past minus Future") #+ theme(legend.position="none") 

blankPlot <- ggplot() + theme_void()

legend <- get_legend(plt9)

plt9 <- plt9 + theme(legend.position="none")


ref_temp_plt <- grid.arrange(blankPlot, legend, plt8,plt9, top = textGrob("Surprisal of Garden Path between Contexts", gp=gpar(fontsize=30,font=8)),
                       bottom = textGrob("", gp=gpar(fontsize=20,font=8)),
                       ncol=2, nrow=2, widths=c(2.7,2.7), heights = c(0.7,3))

