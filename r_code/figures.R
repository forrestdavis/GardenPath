library(grid)
library(gridExtra)
library(ggplot2)

#######################################
### MV/RR reduced/unreduced ###########
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

SHUFF_RAND_Context = read.csv('/home/forrestdavis/CogSci2020/results/def/ORDERED_SHUFF_crit_Indef_Def.csv') 
SHUFF_RAND_Context = subset(x=SHUFF_RAND_Context, subset= Stim == 'reduced')

SHUFF_Context_R <- subset(x = SHUFF_RAND_Context,
                          subset = EXP == 'shuff' & Stim == 'reduced')
RAND_Context_R <- subset(x = SHUFF_RAND_Context,
                         subset = EXP == 'ordered' & Stim == 'reduced')


mean <- c(mean(SHUFF_Context_R$surp), mean(RAND_Context_R$surp))
exp <- c('Shuffled', 'Ordered')
stim <- c('reduced', 'reduced')
ci <- c(qnorm(0.975)*sd(SHUFF_Context_R$surp)/sqrt(length(SHUFF_Context_R$surp)), 
        qnorm(0.975)*sd(RAND_Context_R$surp)/sqrt(length(RAND_Context_R$surp)))

Context <- data.frame(exp, stim, mean, ci)

plt6 <- ggplot(Context, aes(x=exp, y=mean, fill=exp)) + 
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.1,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(-0.5,2)

plt6 <- plt6 +labs(x ="(a)", y = "Surprisal of Indefinite minus Definite") +  theme(legend.position = "none")


## New Old
SHUFF_RAND_Context = read.csv('/home/forrestdavis/CogSci2020/results/def/ORDERED_SHUFF_crit_New_Old.csv') 
SHUFF_RAND_Context = subset(x=SHUFF_RAND_Context, subset= Stim == 'reduced')


SHUFF_Context_R <- subset(x = SHUFF_RAND_Context,
                          subset = EXP == 'shuff' & Stim == 'reduced')
RAND_Context_R <- subset(x = SHUFF_RAND_Context,
                         subset = EXP == 'ordered' & Stim == 'reduced')

mean <- c(mean(SHUFF_Context_R$surp), mean(RAND_Context_R$surp))
exp <- c('Shuffled', 'Ordered')
stim <- c('reduced', 'reduced')
ci <- c(qnorm(0.975)*sd(SHUFF_Context_R$surp)/sqrt(length(SHUFF_Context_R$surp)), 
        qnorm(0.975)*sd(RAND_Context_R$surp)/sqrt(length(RAND_Context_R$surp)))

Context <- data.frame(exp, stim, mean, ci)

plt7 <- ggplot(Context, aes(x=exp, y=mean, fill=exp)) +
  geom_bar(position=position_dodge(), stat="identity", color='black') +
  scale_fill_manual(values = c("#999999", "white"), name= "Type", labels=c("Ordered", "Shuffled")) +
  theme(text = element_text(size=20))+
  geom_errorbar(aes(ymin=mean-ci, ymax=mean+ci),
                width=.1,                    # Width of the error bars
                position=position_dodge(.9)) + ylim(-0.5,2)

plt7 <- plt7 +labs(x ="(b)", y = "Surprisal of Discourse New minus Old") + theme(legend.position="none") 

def_plt <- grid.arrange(plt6,plt7, top = textGrob("Surprisal of Garden Path between Contexts\n", gp=gpar(fontsize=30,font=8)),
                             bottom = textGrob("Model Training Method\n", gp=gpar(fontsize=20,font=8)),
                             layout_matrix = matrix(c(1,2), ncol=2, byrow=TRUE))


