library('skmeans')
x <- readCM('affinities.cm')
mat <- skmeans(x, 50, 'lihc')
#write(mat$cluster,file="clusters_file",ncolumns=1,append=FALSE,sep=" ")
mat$cluster
