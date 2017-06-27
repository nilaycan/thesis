

library(MASS) 
library(class)
library(cluster)
library(impute)



library(WGCNA)
options(stringsAsFactors=F)

dat0=read.csv(file.choose())

datSummary=dat0[,1:9]

datExpr = t(dat0[,10:64])
no.samples = dim(datExpr)[[1]]
dim(datExpr)
rm(dat0);gc() 


powers1=c(seq(1,10,by=1),seq(12,20,by=2))
RpowerTable=pickSoftThreshold(datExpr, powerVector=powers1)[[2]] 

gc()
cex1=0.7
par(mfrow=c(1,2))
plot(RpowerTable[,1], -sign(RpowerTable[,3])*RpowerTable[,2],xlab="
     Soft Threshold (power)",ylab="Scale Free Topology Model Fit,signed R^2",type="n")
text(RpowerTable[,1], -sign(RpowerTable[,3])*RpowerTable[,2],
     labels=powers1,cex=cex1,col="red")
abline(h=0.95,col="red")
plot(RpowerTable[,1], RpowerTable[,5],xlab="Soft Threshold (power)",ylab="Mean
     Connectivity", type="n")
text(RpowerTable[,1], RpowerTable[,5], labels=powers1, cex=cex1,col="red") 


beta1=6
Connectivity=softConnectivity(datExpr,power=beta1)-1 
par(mfrow=c(1,1))
scaleFreePlot(Connectivity, main=paste("soft threshold, power=",beta1), truncated=F); 

ConnectivityCut = 3600 
ConnectivityRank = rank(-Connectivity)
restConnectivity = ConnectivityRank <= ConnectivityCut
sum(restConnectivity)
ADJ= adjacency(datExpr[,restConnectivity],power=beta1)
gc()
dissTOM=TOMdist(ADJ)
gc() 

hierTOM = hclust(as.dist(dissTOM),method="average");
par(mfrow=c(1,1))
plot(hierTOM,labels=F) 

colorh1= cutreeStaticColor(hierTOM,cutHeight = 0.94, minSize = 125)
par(mfrow=c(2,1),mar=c(2,4,1,1))
plot(hierTOM, main="Cluster Dendrogram", labels=F, xlab="", sub="");
plotColorUnderTree(hierTOM,colors=data.frame(module=colorh1))
title("Module (branch) color") 


TOMplot(dissTOM , hierTOM, colorh1) #cok kas??yor. bi daha ??al????t??rma

cmd1=cmdscale(as.dist(dissTOM),2)
par(mfrow=c(1,1))
plot(cmd1, col=as.character(colorh1), main="MDS plot",xlab="Scaling Dimension
     1",ylab="Scaling Dimension 2") 


GeneSignificanceALL=-log10(datSummary$pCox)
GeneSignificance=GeneSignificanceALL[restConnectivity]
par(mfrow=c(1,1))
verboseBarplot(GeneSignificance,colorh1,main="Module Significance ",
               col=levels(factor(colorh1)) ,xlab="Module" ) 


datME=moduleEigengenes(datExpr[,restConnectivity],colorh1)[[1]] 
dissimME=1-(t(cor(datME, method="p")))/2
hclustdatME=hclust(as.dist(dissimME), method="average" )
par(mfrow=c(1,1))
plot(hclustdatME, main="Clustering tree based on the module eigengenes of modules")

signif(cor(datME, use="p"), 2) 
datMEordered=datME[,hclustdatME$order]
pairs( datMEordered, upper.panel = panel.smooth, lower.panel = panel.corr,
       diag.panel=panel.hist ,main="Relation between module eigengenes") 
#ERROR in pairs.default(datMEordered, upper.panel = panel.smooth, lower.panel = panel.cor,  : 
object 'panel.cor' not found


mean1=function(x) mean(x,na.rm=T)
var1=function(x) var(x,na.rm=T)
meanExpr=apply( datExpr[,restConnectivity],2,mean1)
varExpr=apply( datExpr[,restConnectivity],2,var1)
par(mfrow=c(1,2))
plot(Connectivity[restConnectivity],meanExpr, col=as.character(colorh1),
     main="Mean(Expression) vs K",xlab="Connectivity")
plot (Connectivity[restConnectivity],varExpr, col= as.character(colorh1), main="Var(Expression)
      vs K" ,xlab="Connectivity") 


par(mfrow=c(2,1), mar=c(1, 2, 4, 1))
    ClusterSamples=hclust(dist(datExpr),method="average")
     for the first (turquoise) module we use
    which.module="turquoise"
    plotMat(t(scale(datExpr[ClusterSamples$order,1:ncol(datExpr)][,dynamicColors==which.module ]) ),
       nrgcols=30,rlabels=T,clabels=T,rcols=which.module,
       main=which.module, cex.main=2)
     for the second (blue) module we use
    which.module="blue"
    plotMat(t(scale(datExpr[ClusterSamples$order,1:ncol(datExpr)][,dynamicColors==which.module ]) ),
       nrgcols=30,rlabels=T,clabels=T,rcols=which.module,
       main=which.module, cex.main=2)
  
plotMEpairs(datME[,1:5])

color1=rep("grey",dim(datExpr)[[2]])
color1[restConnectivity]=as.character(colorh1)
ConnectivityMeasures=intramodularConnectivity(ADJ,colors=colorh1)
names(ConnectivityMeasures) 


colorlevels=levels(factor(colorh1))
par(mfrow=c(2,3),mar=c(5, 4, 4, 2) + 0.1)
for (i in c(1:length(colorlevels) ) ) {
  whichmodule=colorlevels[[i]];restrict1=colorh1==whichmodule
  verboseScatterplot(ConnectivityMeasures$kWithin[restrict1],
                     GeneSignificance[restrict1],col=colorh1[restrict1],main= paste("set I,",
                                                                                    whichmodule),ylab="Gene Significance",xlab="Intramodular k")
} 


datKME=signedKME(datExpr, datME)
names(datKME) 
dim(datKME) 
attach(datKME) 


whichmodule="brown"
restrictGenes= colorh1== whichmodule
par(mfrow=c(1,1))
verboseScatterplot(ConnectivityMeasures$kWithin[ restrictGenes],
                   (datKME$kMEbrown[restConnectivity][restrictGenes])^beta1 ,xlab="kIN",ylab="kME^power",
                   col=whichmodule,main="Relation between two measures of intramodular k, ") 


attach(datKME)
FilterGenes= GeneSignificanceALL > -log10(0.05) & abs(kMEbrown)>.85
table(FilterGenes)
datSummary[FilterGenes,] 

FilterGenes= GeneSignificanceALL> -log10(0.05) & -kMEbrown> .5 # notice the red minus sign!
table(FilterGenes)
datSummary[FilterGenes,] 




FilterGenes= GeneSignificanceALL > -log10(0.05) & abs(kMEbrown)>.5 & abs(kMEgreen)>.5
table(FilterGenes)
datSummary[FilterGenes,] 



FilterGenes= GeneSignificanceALL > -log10(0.05) & abs(kMEbrown)>.6 & abs(kMEyellow)<.3
table(FilterGenes) 

datout=data.frame(datSummary, colorNEW=color1, ConnectivityNew=Connectivity,datKME )
write.table(datout, file="OutputCancerNetwork.csv", sep=",", row.names=F) 


corhelp=cor(datExpr[,restConnectivity],use="pairwise.complete.obs")
whichmodule="brown"
datconnectivitiesSoft=data.frame(matrix(666,nrow=sum(colorh1==whichmodule),ncol=length(pow
                                                                                       ers1)))
names(datconnectivitiesSoft)=paste("kWithinPower",powers1,sep="")
for (i in c(1:length(powers1)) ) {
  datconnectivitiesSoft[,i]=apply(abs(corhelp[colorh1==whichmodule,
                                              colorh1==whichmodule])^powers1[i],1,sum)}
SpearmanCorrelationsSoft=signif(cor(GeneSignificance[ colorh1==whichmodule],
                                    datconnectivitiesSoft, method="s",use="p")) 



datKTOM.IN=data.frame(matrix(666,nrow=sum(colorh1==whichmodule),ncol=length(powers1)))
names(datKTOM.IN)=paste("omegaWithinPower",powers1,sep="")
for (i in c(1:length(powers1)) ) {
  datconnectivitiesSoft[,i]=apply(
    1-TOMdist(abs(corhelp[colorh1==whichmodule, colorh1==whichmodule])^powers1[i])
    ,1,sum)}
SpearmanCorrelationskTOMSoft=as.vector(signif(cor(GeneSignificance[ colorh1==whichmodule],
                                                  datconnectivitiesSoft, method="s",use="p")))
par(mfrow=c(1,1), mar=c(5, 4, 4, 2) +0.1)
plot(powers1, SpearmanCorrelationsSoft, main="Cor(Connectivity,Gene Significance) vs Soft
     Thresholds(powers)",ylab="Spearman Correlation(Gene Significance,k.in)",xlab="Power
     beta",type="n",ylim=range(c(SpearmanCorrelationsSoft,
                                 SpearmanCorrelationskTOMSoft),na.rm=T)
     )
text(powers1, SpearmanCorrelationsSoft,labels=powers1,col="red")
abline(v=6,col="red") 
points(powers1, SpearmanCorrelationskTOMSoft, type="n")
text(powers1, SpearmanCorrelationskTOMSoft,labels=powers1,col="orange") 



datCCinSoft=data.frame(matrix(666,nrow=sum(colorh1==whichmodule),ncol=length(powers1)))
names(datCCinSoft)=paste("CCinSoft",powers1,sep="")
for (i in c(1:length(powers1)) ) {
  datCCinSoft[,i]= clusterCoef(abs(corhelp[colorh1==whichmodule,
                                           colorh1==whichmodule])^powers1[i])
}
SpearmanCorrelationsCCinSoft=as.vector(signif(cor(GeneSignificance[ colorh1==whichmodule],
                                                  datCCinSoft, method="s",use="p")))
dathelpSoft=data.frame(signedRsquared=-sign(RpowerTable[,3])*RpowerTable[,2], corGSkINSoft
                       =as.vector(SpearmanCorrelationsSoft), corGSwINSoft=
                         as.vector(SpearmanCorrelationskTOMSoft),corGSCCSoft=as.vector(SpearmanCorrelationsCCinSo
                                                                                       ft))
matplot(powers1,dathelpSoft,type="l",lty=1,lwd=3,col=c("black","red","blue","green"),ylab="",xla
        b="beta")
abline(v=6,col="red")
legend(13,0.5, c("signed R^2","r(GS,k.IN)","r(GS,kTOM.IN)","r(GS,cc.in)"),
       col=c("black","red","blue","green"), lty=1,lwd=3,ncol = 1, cex=1)












